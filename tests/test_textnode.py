import unittest

from ssg.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a test", TextType.BOLD, "test.com")
        node2 = TextNode("This is a test", TextType.BOLD, "test.com")
        self.assertEqual(node1, node2)

    def test_uneq(self):
        node1 = TextNode("This is a test", TextType.BOLD, "test.com")
        node2 = TextNode("This is another test", TextType.ITALIC, "Test.com")
        self.assertNotEqual(node1, node2)

    def test_notext(self):
        node1 = TextNode("This is a test", TextType.BOLD, "test.com")
        node2 = TextNode("", TextType.BOLD, "")
        self.assertNotEqual(node1, node2)
    
    def test_diff_type(self):
        node1 = TextNode("This is a test", TextType.BOLD, "test.com")
        node2 = TextNode("This is a test", TextType.ITALIC, "test.com")
        self.assertNotEqual(node1, node2)
    
    def test_nourl(self):
        node1 = TextNode("This is a test", TextType.BOLD, "test.com")
        node2 = TextNode("This is a test", TextType.BOLD, "")
        self.assertNotEqual(node1, node2)

    def test_textToHTML_TEXT(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textToHTML_BOLD(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_textToHTML_ITALIC(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_textToHTML_CODE(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_textToHTML_LINK(self):
        node = TextNode("Click me", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_textToHTML_IMAGE(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://img.com/pic.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://img.com/pic.png", "alt": "Alt text"}
        )

    def test_textToHTML_invalid(self):
        node = TextNode("Text", "not-a-valid-type")
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
