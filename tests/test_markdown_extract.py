import unittest

from ssg.markdown_extract import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images_basic(self):
        matches = extract_markdown_images("Text with ![alt](https://img.com/a.png)")
        self.assertEqual(matches, [("alt", "https://img.com/a.png")])

    def test_extract_images_multiple(self):
        text = "Text with ![image1](https://img.com/a.png) and ![image2](b.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [("image1", "https://img.com/a.png"), ("image2", "b.png")],
        )

    def test_extract_images_alt_with_spaces(self):
        matches = extract_markdown_images("Here ![alt with spaces](https://img.com/a.png)")
        self.assertEqual(matches, [("alt with spaces", "https://img.com/a.png")])

    def test_extract_images_none(self):
        matches = extract_markdown_images("This text has no images")
        self.assertEqual(matches, [])

    def test_extract_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertEqual(matches, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links_basic(self):
        matches = extract_markdown_links("Text with [link](https://site.com)")
        self.assertEqual(matches, [("link", "https://site.com")])

    def test_extract_links_multiple(self):
        text = "[first](https://one.com) and [second](https://two.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [("first", "https://one.com"), ("second", "https://two.com")],
        )

    def test_extract_links_text_with_spaces(self):
        matches = extract_markdown_links("Here [a link text](https://site.com)")
        self.assertEqual(matches, [("a link text", "https://site.com")])

    def test_extract_links_none(self):
        matches = extract_markdown_links("This text has no links")
        self.assertEqual(matches, [])

    def test_extract_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertEqual(matches, [])