import unittest

from ssg.textnode import TextNode, TextType
from ssg.textsplit import split_nodes_delimiter, split_nodes_image, split_nodes_links


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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_single(self):
        node = TextNode("text ![alt](https://img.com/a.png) more", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("text ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://img.com/a.png"),
                TextNode(" more", TextType.TEXT),
            ],
        )

    def test_split_image_multiple(self):
        node = TextNode("![a](x.png) and ![b](y.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.IMAGE, "x.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "y.png"),
            ],
        )

    def test_split_image_at_start(self):
        node = TextNode("![alt](x.png) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("alt", TextType.IMAGE, "x.png"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_split_image_at_end(self):
        node = TextNode("before ![alt](x.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "x.png"),
            ],
        )

    def test_split_image_only(self):
        node = TextNode("![alt](x.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("alt", TextType.IMAGE, "x.png")])

    def test_split_image_alt_with_spaces(self):
        node = TextNode("![alt text here](x.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes, [TextNode("alt text here", TextType.IMAGE, "x.png")]
        )

    def test_split_image_no_image(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_split_image_link_is_not_image(self):
        node = TextNode("a [link](x.com) here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("a [link](x.com) here", TextType.TEXT)])

    def test_split_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

    def test_split_image_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_split_image_mixed_nodes(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("text ![a](x.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("text ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "x.png"),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_single(self):
        node = TextNode("text [link](https://site.com) more", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://site.com"),
                TextNode(" more", TextType.TEXT),
            ],
        )

    def test_split_link_multiple(self):
        node = TextNode("[a](x.com) and [b](y.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.LINK, "x.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.LINK, "y.com"),
            ],
        )

    def test_split_link_at_start(self):
        node = TextNode("[link](x.com) after", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "x.com"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_split_link_at_end(self):
        node = TextNode("before [link](x.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "x.com"),
            ],
        )

    def test_split_link_only(self):
        node = TextNode("[link](x.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("link", TextType.LINK, "x.com")])

    def test_split_link_text_with_spaces(self):
        node = TextNode("[a link text](x.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes, [TextNode("a link text", TextType.LINK, "x.com")]
        )

    def test_split_link_no_link(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_split_link_image_excluded(self):
        node = TextNode("![alt](img.png)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("![alt](img.png)", TextType.TEXT)])

    def test_split_link_mixed_image_and_link(self):
        node = TextNode("![img](a.png) and [link](b.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("![img](a.png) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "b.com"),
            ],
        )

    def test_split_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

    def test_split_link_non_text_passthrough(self):
        node = TextNode("already code", TextType.CODE)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("already code", TextType.CODE)])

    def test_split_link_mixed_nodes(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("a [l](x.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_links(nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("a ", TextType.TEXT),
                TextNode("l", TextType.LINK, "x.com"),
            ],
        )