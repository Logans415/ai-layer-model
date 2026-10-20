"""Behavioral checks for release boundaries and archive metadata. MIT."""

import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from scripts.package_release import ZIP_TIMESTAMP, build_archives
from scripts.validate_release import PUBLIC_FILES, ROOT, release_paths, validate_release


class ReleaseToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "source"
        for name in PUBLIC_FILES:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def test_missing_and_additional_paths_are_rejected(self):
        (self.root / "extra.bin").write_bytes(b"test fixture")
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            release_paths(self.root)
        other = self.base / "missing"
        shutil.copytree(self.root, other)
        (other / "README.md").unlink()
        (other / "extra.bin").unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            release_paths(other)

    def test_metadata_is_not_read_and_model_drift_is_rejected(self):
        (self.root / ".git").write_text("metadata fixture", encoding="utf-8")
        self.assertEqual(len(release_paths(self.root)), len(PUBLIC_FILES))
        path = self.root / "skills/map-ai-stack/references/layers.json"
        path.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "drifted"):
            validate_release(self.root)

    def test_junction_source_is_rejected(self):
        original = Path.is_junction

        def junction_fixture(path):
            return path == self.root / "docs" or original(path)

        with mock.patch.object(Path, "is_junction", junction_fixture):
            with self.assertRaisesRegex(ValueError, "regular"):
                release_paths(self.root)

    def test_linked_source_is_rejected(self):
        target = self.base / "target.txt"
        target.write_text("fixture", encoding="utf-8")
        try:
            (self.root / "linked.txt").symlink_to(target)
        except OSError:
            self.skipTest("Symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "regular"):
            release_paths(self.root)

    def test_archives_are_deterministic_and_cannot_replace_outputs(self):
        first = build_archives(self.base / "first", self.root)
        for name in PUBLIC_FILES:
            os.utime(self.root / name, (1700000000, 1700000000))
        second = build_archives(self.base / "second", self.root)
        self.assertEqual(
            [p.read_bytes() for p in first], [p.read_bytes() for p in second]
        )
        for path, count in zip(first[:2], (len(PUBLIC_FILES), 5), strict=True):
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(len(archive.infolist()), count)
                self.assertEqual(
                    {i.date_time for i in archive.infolist()}, {ZIP_TIMESTAMP}
                )
                self.assertIsNone(archive.testzip())
        with self.assertRaises(FileExistsError):
            build_archives(self.base / "first", self.root)
        with self.assertRaisesRegex(ValueError, "outside"):
            build_archives(self.root / "output", self.root)


if __name__ == "__main__":
    unittest.main()
