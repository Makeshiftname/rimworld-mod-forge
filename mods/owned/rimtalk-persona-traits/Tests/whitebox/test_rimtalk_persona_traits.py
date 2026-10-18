import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


MOD_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = MOD_ROOT.parents[2]
sys.path.insert(0, str(REPO_ROOT / "shared" / "tests"))

from check_mod import check_mod  # noqa: E402


class RimTalkPersonaTraitsTests(unittest.TestCase):
    def test_static_checks(self) -> None:
        self.assertEqual([], check_mod(MOD_ROOT))

    def test_identity(self) -> None:
        root = ET.parse(MOD_ROOT / "About" / "About.xml").getroot()
        self.assertEqual("Makeshiftname.RimTalkPersonaTraits", root.findtext("packageId"))
        self.assertEqual("Makeshiftname", root.findtext("author"))

    def test_only_16_is_declared(self) -> None:
        root = ET.parse(MOD_ROOT / "About" / "About.xml").getroot()
        versions = [node.text for node in root.findall("./supportedVersions/li")]
        self.assertEqual(["1.6"], versions)
        self.assertFalse((MOD_ROOT / "1.7").exists())

    def test_traits_and_translations_match(self) -> None:
        traits = ET.parse(MOD_ROOT / "1.6" / "Defs" / "Traits.xml").getroot()
        def_names = [node.text for node in traits.iter("defName")]
        self.assertEqual(10, len(def_names))
        self.assertEqual(len(def_names), len(set(def_names)))

        translations = ET.parse(
            MOD_ROOT
            / "Languages"
            / "ChineseSimplified"
            / "DefInjected"
            / "TraitDef"
            / "Traits.xml"
        ).getroot()
        keys = {node.tag for node in translations}
        for def_name in def_names:
            self.assertIn(f"{def_name}.label", keys)
            self.assertIn(f"{def_name}.description", keys)

    def test_conflicting_traits_reference_existing_defs(self) -> None:
        traits = ET.parse(MOD_ROOT / "1.6" / "Defs" / "Traits.xml").getroot()
        def_names = {node.text for node in traits.iter("defName")}
        for conflict in traits.iter("conflictingTraits"):
            for node in conflict.findall("li"):
                self.assertIn(node.text, def_names)

    def test_no_old_owner_namespace(self) -> None:
        about = (MOD_ROOT / "About" / "About.xml").read_text(encoding="utf-8")
        self.assertNotIn("RunningBugs", about)


if __name__ == "__main__":
    unittest.main()
