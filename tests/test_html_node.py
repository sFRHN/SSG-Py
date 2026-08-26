import unittest

from ssg.html_node import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.tag, "p")

    def test_values(self):
        node = HTMLNode(value="test")
        self.assertEqual(node.value, "test")

    def test_children(self):
        child = HTMLNode()
        node = HTMLNode(children=[child])
        self.assertEqual(node.children, [child])

    def test_props(self):
        test_props: dict = {"href": "test.com"}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props, test_props)

    def test_EmptyNodes(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_EqTags(self):
        node1 = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        self.assertEqual(node1, node2)

    def test_EqValues(self):
        node1 = HTMLNode(value="test")
        node2 = HTMLNode(value="test")
        self.assertEqual(node1, node2)

    def test_EqChildren(self):
        child = HTMLNode()
        node1 = HTMLNode(children=[child])
        node2 = HTMLNode(children=[child])
        self.assertEqual(node1, node2)

    def test_EqProps(self):
        test_props: dict = {"href": "test"}
        node1 = HTMLNode(props=test_props)
        node2 = HTMLNode(props=test_props)
        self.assertEqual(node1, node2)

    def test_DiffTags(self):
        node1 = HTMLNode("p")
        node2 = HTMLNode("a")
        self.assertNotEqual(node1, node2)

    def test_DiffValues(self):
        node1 = HTMLNode(value="val1")
        node2 = HTMLNode(value="val2")
        self.assertNotEqual(node1, node2)

    def test_DiffChildren(self):
        child1 = HTMLNode(tag="p")
        node1 = HTMLNode(children=[child1])
        child2 = HTMLNode(tag="a")
        node2 = HTMLNode(children=[child2])
        self.assertNotEqual(node1, node2)

    def test_DiffProps(self):
        test_props1: dict = {"href": "test1"}
        node1 = HTMLNode(props=test_props1)

        test_props2: dict = {"href": "test2"}
        node2 = HTMLNode(props=test_props2)
        self.assertNotEqual(node1, node2)
