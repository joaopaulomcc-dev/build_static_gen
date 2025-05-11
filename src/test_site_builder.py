import unittest
from pathlib import Path

from site_builder import extract_title


class TestSiteBuilder(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title(Path("content/index.md"))
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_exception(self):
        with self.assertRaises(ValueError):
            title = extract_title(Path("template.html"))
