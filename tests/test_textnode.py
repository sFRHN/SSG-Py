import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()
