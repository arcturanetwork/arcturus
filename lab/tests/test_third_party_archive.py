from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from assessments.third_party_archive import audit_zip


class ThirdPartyArchiveTests(unittest.TestCase):
    def test_archive_audit_counts_sources_weights_and_license(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "study.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("study/README.md", "| 1 | Domain | 60% | 1 |\n| 2 | Other | 40% | 1 |")
                archive.writestr("study/Domain/a.md", "## Sources\nhttps://docs.nvidia.com/a")
                archive.writestr("study/Other/b.md", "No source")
                archive.writestr("study/LICENSE", "MIT")
            report = audit_zip(path)
            self.assertTrue(report["path_safe"]); self.assertEqual(report["markdown_topic_notes"], 2)
            self.assertEqual(report["notes_with_sources"], 1); self.assertEqual(report["readme_weight_total"], 100)
            self.assertTrue(report["content_reuse_allowed"])

    def test_zip_slip_is_reported(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "unsafe.zip"
            with ZipFile(path, "w") as archive:
                archive.writestr("study/README.md", "readme")
                archive.writestr("../escape.md", "bad")
            with self.assertRaisesRegex(ValueError, "one top-level"):
                audit_zip(path)


if __name__ == "__main__": unittest.main()
