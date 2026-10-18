#!/usr/bin/env python3
"""Static checks for mods in this repository.

This intentionally does not instantiate RimWorld runtime objects. It checks
metadata, XML structure, version directories, translation keys, dependency
declarations, and machine-specific paths.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ALLOWED_PACKAGE_PREFIX = "Makeshiftname."
ABSOLUTE_PATH_RE = re.compile(r"(?i)(?:[a-z]:\\|/home/|/Users/|\$HOME)")


def _text(root: ET.Element, tag: str, default: str = "") -> str:
    node = root.find(tag)
    return (node.text or "").strip() if node is not None else default


def _all_xml(mod_root: Path) -> list[Path]:
    return sorted(path for path in mod_root.rglob("*.xml") if path.is_file())


def _parse_xml(path: Path, errors: list[str]) -> ET.Element | None:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{path}: XML parse error: {exc}")
        return None


def _find_repo_root(mod_root: Path) -> Path | None:
    for parent in mod_root.parents:
        if (parent / "mods").is_dir() and (parent / "shared").is_dir():
            return parent
    return None


def _duplicate_package_ids(mod_root: Path, package_id: str) -> list[str]:
    repo_root = _find_repo_root(mod_root)
    if repo_root is None:
        return []

    matches: list[Path] = []
    for about in (repo_root / "mods").rglob("About/About.xml"):
        root = _parse_xml(about, [])
        if root is not None and _text(root, "packageId") == package_id:
            matches.append(about)
    return [str(path) for path in matches if path.parent.parent != mod_root]


def _check_about(mod_root: Path, errors: list[str]) -> dict[str, object]:
    about = mod_root / "About" / "About.xml"
    if not about.is_file():
        errors.append(f"{about}: missing")
        return {}

    root = _parse_xml(about, errors)
    if root is None:
        return {}
    if root.tag != "ModMetaData":
        errors.append(f"{about}: root must be ModMetaData, got {root.tag}")

    package_id = _text(root, "packageId")
    name = _text(root, "name")
    author = _text(root, "author")
    if not package_id:
        errors.append(f"{about}: packageId is empty")
    elif not package_id.startswith(ALLOWED_PACKAGE_PREFIX):
        errors.append(
            f"{about}: packageId must start with {ALLOWED_PACKAGE_PREFIX!r}: {package_id!r}"
        )
    if not name:
        errors.append(f"{about}: name is empty")
    if not author:
        errors.append(f"{about}: author is empty")
    elif author != "Makeshiftname":
        errors.append(f"{about}: author should be Makeshiftname, got {author!r}")

    versions = [
        (node.text or "").strip()
        for node in root.findall("./supportedVersions/li")
        if (node.text or "").strip()
    ]
    if not versions:
        errors.append(f"{about}: supportedVersions is empty")
    for version in versions:
        version_dir = mod_root / version
        if not version_dir.is_dir():
            errors.append(f"{mod_root}: supported version {version} has no directory")

    version_dirs = {
        path.name
        for path in mod_root.iterdir()
        if path.is_dir() and re.fullmatch(r"\d+\.\d+", path.name)
    }
    for version in sorted(version_dirs - set(versions)):
        errors.append(f"{mod_root}: version directory {version} is not declared")

    for dependency in root.findall("./modDependencies/li"):
        dep_id = _text(dependency, "packageId")
        if not dep_id:
            errors.append(f"{about}: modDependencies entry has no packageId")

    for dep in root.findall("./loadAfter/li"):
        if not (dep.text or "").strip():
            errors.append(f"{about}: loadAfter entry is empty")

    duplicates = _duplicate_package_ids(mod_root, package_id) if package_id else []
    if duplicates:
        errors.append(f"{about}: duplicate packageId also used by {duplicates}")

    return {
        "package_id": package_id,
        "name": name,
        "author": author,
        "versions": versions,
    }


def _translation_keys(mod_root: Path, errors: list[str]) -> set[str]:
    keys: set[str] = set()
    language_roots = [mod_root / "Languages", mod_root / "Common" / "Languages"]
    for language_root in language_roots:
        if not language_root.is_dir():
            continue
        for path in sorted(language_root.rglob("*.xml")):
            root = _parse_xml(path, errors)
            if root is None:
                continue
            for node in root:
                if node.tag:
                    keys.add(node.tag)
    return keys


def _def_names(mod_root: Path, errors: list[str]) -> set[str]:
    names: set[str] = set()
    common_defs = mod_root / "Common" / "Defs"
    for path in sorted(common_defs.rglob("*.xml")) if common_defs.is_dir() else []:
        root = _parse_xml(path, errors)
        if root is not None:
            names.update(
                (node.text or "").strip()
                for node in root.iter("defName")
                if (node.text or "").strip()
            )
    for version_dir in _version_dirs(mod_root):
        defs = version_dir / "Defs"
        if not defs.is_dir():
            continue
        for path in sorted(defs.rglob("*.xml")):
            root = _parse_xml(path, errors)
            if root is not None:
                names.update(
                    (node.text or "").strip()
                    for node in root.iter("defName")
                    if (node.text or "").strip()
                )
    return names


def _version_dirs(mod_root: Path) -> list[Path]:
    return sorted(
        path
        for path in mod_root.iterdir()
        if path.is_dir() and re.fullmatch(r"\d+\.\d+", path.name)
    )


def _check_translations(mod_root: Path, errors: list[str]) -> None:
    keys = _translation_keys(mod_root, errors)
    if not keys:
        return
    for def_name in sorted(_def_names(mod_root, errors)):
        if f"{def_name}.label" not in keys:
            errors.append(f"{mod_root}: translation missing {def_name}.label")
        if f"{def_name}.description" not in keys:
            errors.append(f"{mod_root}: translation missing {def_name}.description")


def _check_absolute_paths(mod_root: Path, errors: list[str]) -> None:
    for path in sorted(mod_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".xml", ".cs", ".csproj", ".props", ".targets"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        if ABSOLUTE_PATH_RE.search(text):
            errors.append(f"{path}: contains a machine-specific absolute path")


def check_mod(mod_root: Path) -> list[str]:
    mod_root = mod_root.resolve()
    errors: list[str] = []
    if not mod_root.is_dir():
        return [f"{mod_root}: not a directory"]
    _check_about(mod_root, errors)
    for path in _all_xml(mod_root):
        _parse_xml(path, errors)
    _check_translations(mod_root, errors)
    _check_absolute_paths(mod_root, errors)
    return errors


def _default_mods() -> list[Path]:
    repo_root = Path(__file__).resolve().parents[2]
    roots = [repo_root / "mods" / "owned", repo_root / "mods" / "patches"]
    return sorted(
        path
        for root in roots
        if root.is_dir()
        for path in root.iterdir()
        if path.is_dir()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mods", nargs="*", type=Path)
    parser.add_argument("--json", action="store_true", help="print machine-readable results")
    args = parser.parse_args()

    mods = args.mods or _default_mods()
    results: dict[str, list[str]] = {}
    for mod in mods:
        results[str(mod)] = check_mod(mod)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for mod, errors in results.items():
            if errors:
                print(f"FAIL {mod}")
                for error in errors:
                    print(f"  - {error}")
            else:
                print(f"OK   {mod}")

    return 1 if any(results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
