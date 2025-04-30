import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTML(unittest.TestCase):
    def test_creation(self):
        node = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph.")
        self.assertIs(node.children, None)
        self.assertIs(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="link",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_to_html(self):
        node = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


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

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(
            parent_node.to_html(),
            "<div></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", children=None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, children=None)
        self.assertRaises(ValueError, parent_node.to_html)


if __name__ == "__main__":
    unittest.main()
