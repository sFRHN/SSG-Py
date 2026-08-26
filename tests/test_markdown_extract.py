import unittest

from ssg.markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
)


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
        matches = extract_markdown_images(
            "Here ![alt with spaces](https://img.com/a.png)"
        )
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


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        blocks = markdown_to_blocks("just one block")
        self.assertEqual(blocks, ["just one block"])

    def test_no_double_newline(self):
        blocks = markdown_to_blocks("line one\nline two")
        self.assertEqual(blocks, ["line one\nline two"])

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

    def test_surrounding_blank_lines(self):
        blocks = markdown_to_blocks("\n\npara\n\n")
        self.assertEqual(blocks, ["para"])

    def test_leading_blank_line(self):
        blocks = markdown_to_blocks("\n\npara")
        self.assertEqual(blocks, ["para"])

    def test_consecutive_blank_lines(self):
        blocks = markdown_to_blocks("para1\n\n\n\npara2")
        self.assertEqual(blocks, ["para1", "para2"])

    def test_multiple_blank_lines(self):
        blocks = markdown_to_blocks("para1\n\n\npara2")
        self.assertEqual(blocks, ["para1", "para2"])

    def test_whitespace_only_block(self):
        blocks = markdown_to_blocks("para\n\n   \n\nother")
        self.assertEqual(blocks, ["para", "other"])

    def test_blocks_stripped_of_whitespace(self):
        blocks = markdown_to_blocks("  para1  \n\n  para2  ")
        self.assertEqual(blocks, ["para1", "para2"])

