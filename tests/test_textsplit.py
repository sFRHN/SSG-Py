import unittest

from ssg.textnode import TextNode, TextType
from ssg.textsplit import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_basic_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_basic_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimiters(self):
        node = TextNode("**bold** and **more**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ],
        )

    def test_delimiter_at_end(self):
        node = TextNode("end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("end ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_only_delimiter(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("bold", TextType.BOLD)])

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_non_text_node_passed_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_text_and_non_text(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("with **bold**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_multiple_text_nodes(self):
        nodes = [
            TextNode("a **b**", TextType.TEXT),
            TextNode("c **d**", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode("c ", TextType.TEXT),
                TextNode("d", TextType.BOLD),
            ],
        )

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])