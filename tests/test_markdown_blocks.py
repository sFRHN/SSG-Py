import unittest

from ssg.markdown_blocks import markdown_to_blocks


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
