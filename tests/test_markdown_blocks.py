import unittest

from ssg.markdown_blocks import BlockType, block_to_blocktype, markdown_to_blocks


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

class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        block = "this is a pargraph"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_heading1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_heading2(self):
        block = "## This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
    
    def test_heading3(self):
        block = "### This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
    
    def test_heading4(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
    
    def test_heading5(self):
        block = "##### This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
    
    def test_heading6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)

    def test_incorrect_heading(self):
        block = "#This is not a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_seven_hashes_is_paragraph(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_heading_without_text(self):
        block = "#"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_code_block_empty_content(self):
        block = "```\n\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_code_block_with_language(self):
        block = "```python\ncode here\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_code_block_unclosed(self):
        block = "```\ncode here"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_code_block_extra_trailing_text(self):
        block = "```\ncode here\n``` extra"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_quote_basic(self):
        block = "> This is a quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_quote_no_space(self):
        block = ">This is a quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_quote_multiline(self):
        block = "> line one\n> line two\n> line three"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_quote_empty_marker(self):
        block = ">"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_quote_mixed_line(self):
        block = "> line one\nnot a quote"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_unordered_list_basic(self):
        block = "- item one"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiline(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space(self):
        block = "-item"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_unordered_list_dash_only(self):
        block = "-"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_line(self):
        block = "- one\nnot a list"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_asterisk_is_not_unordered_list(self):
        block = "* item"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_basic(self):
        block = "1. item one"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiline(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one(self):
        block = "2. two\n3. three"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_not_incrementing(self):
        block = "1. one\n3. three"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        block = "1.item"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_mixed_line(self):
        block = "1. one\ntwo"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_two_digit_number(self):
        block = "1. one\n10. ten"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_starting_at_zero(self):
        block = "0. zero"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_whitespace_only_block(self):
        block = "   "
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_newline_only_block(self):
        block = "\n"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_code_block_fence_only(self):
        block = "```"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_code_block_multiline_content(self):
        block = "```\ncode one\n\ncode two\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)

    def test_quote_empty_line_inside(self):
        block = "> line one\n\n> line two"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_quote_mixed_spacing(self):
        block = "> line one\n>line two"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)

    def test_unordered_double_space_after_dash(self):
        block = "- one\n-  two"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_long_sequence(self):
        block = (
            "1. one\n2. two\n3. three\n4. four\n5. five\n"
            "6. six\n7. seven\n8. eight\n9. nine\n10. ten"
        )
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)

    def test_ordered_list_period_only(self):
        block = "1."
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

    def test_ordered_list_non_numeric_start(self):
        block = "a. one"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)
