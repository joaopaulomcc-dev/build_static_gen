import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_a = TextNode("This is a text node", TextType.BOLD)
        node_b = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node_a, node_b)

    def test_noteq(self):
        node_a = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")
        node_b = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node_a, node_b)

    def test_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIs(node.url, None)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://www.boot.dev/")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "https://www.boot.dev/")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "This is an image node")


if __name__ == "__main__":
    unittest.main()
