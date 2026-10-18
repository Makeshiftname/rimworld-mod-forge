import sys
import unittest
from pathlib import Path


MOD_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = MOD_ROOT.parents[2]
sys.path.insert(0, str(REPO_ROOT / "shared" / "tests"))

from check_mod import check_mod  # noqa: E402


class StaticChecks(unittest.TestCase):
    def test_mod_metadata(self) -> None:
        issues = check_mod(MOD_ROOT)
        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
