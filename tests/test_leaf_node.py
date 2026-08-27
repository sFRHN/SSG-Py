import unittest

from ssg.leaf_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "link", {"href": "google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">link</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.children, None)

    def test_leaf_no_children_param(self):
        with self.assertRaises(TypeError):
            LeafNode("p", "Hello, world!", None, {"href": "test.com"})

    def test_leaf_requires_tag_and_value(self):
        with self.assertRaises(TypeError):
            LeafNode()

    def test_leaf_eq(self):
        node1 = LeafNode("a", "link", {"href": "google.com"})
        node2 = LeafNode("a", "link", {"href": "google.com"})
        self.assertEqual(node1, node2)

    def test_leaf_neq_tag(self):
        node1 = LeafNode("a", "link")
        node2 = LeafNode("p", "link")
        self.assertNotEqual(node1, node2)

    def test_leaf_neq_value(self):
        node1 = LeafNode("a", "link1")
        node2 = LeafNode("a", "link2")
        self.assertNotEqual(node1, node2)

    def test_leaf_neq_props(self):
        node1 = LeafNode("a", "link", {"href": "google.com"})
        node2 = LeafNode("a", "link", {"href": "test.com"})
        self.assertNotEqual(node1, node2)
