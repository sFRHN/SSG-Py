import unittest

from ssg.leaf_node import LeafNode
from ssg.parent_node import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multi_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_nested_parentnodes(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        inner = ParentNode("div", [leaf1, leaf2])
        outer = ParentNode("section", [inner, leaf1])
        self.assertEqual(
            outer.to_html(),
            "<section><div><b>bold</b><i>italic</i></div><b>bold</b></section>",
        )

    def test_to_html_deep_nesting(self):
        leaf = LeafNode("em", "deep")
        node3 = ParentNode("c", [leaf])
        node2 = ParentNode("b", [node3])
        node1 = ParentNode("a", [node2])
        self.assertEqual(node1.to_html(), "<a><b><c><em>deep</em></c></b></a>")

    def test_to_html_leaf_with_props(self):
        child = LeafNode("a", "link", {"href": "google.com"})
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), '<p><a href="google.com">link</a></p>')

    def test_to_html_parent_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>child</span></div>',
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode("", [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_tag_raises(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_children_required(self):
        with self.assertRaises(TypeError):
            ParentNode("div")

    def test_parent_eq(self):
        node1 = ParentNode("div", [LeafNode("span", "child")])
        node2 = ParentNode("div", [LeafNode("span", "child")])
        self.assertEqual(node1, node2)

    def test_parent_neq_tag(self):
        node1 = ParentNode("div", [LeafNode("span", "child")])
        node2 = ParentNode("section", [LeafNode("span", "child")])
        self.assertNotEqual(node1, node2)

    def test_parent_neq_children(self):
        node1 = ParentNode("div", [LeafNode("span", "child")])
        node2 = ParentNode("div", [LeafNode("span", "other")])
        self.assertNotEqual(node1, node2)

    def test_parent_neq_props(self):
        node1 = ParentNode("div", [LeafNode("span", "child")], {"class": "a"})
        node2 = ParentNode("div", [LeafNode("span", "child")], {"class": "b"})
        self.assertNotEqual(node1, node2)
