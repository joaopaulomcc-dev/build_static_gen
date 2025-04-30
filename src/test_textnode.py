import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
