import unittest

from parser import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multiple_node_types(self):
        code_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        italic_node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        bold_node = TextNode("This is text with a **bold** word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([code_node, italic_node, bold_node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
                TextNode("This is text with an _italic_ word", TextType.TEXT),
                TextNode("This is text with a **bold** word", TextType.TEXT),
            ],
        )

    def test_delimiter_at_the_start(self):
        bold_node = TextNode("**This** is text with a **bold** word", TextType.TEXT)

        new_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delimiter_at_the_end(self):
        bold_node = TextNode("**This** is text with a **bold word**", TextType.TEXT)

        new_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is text with a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
            ],
        )


if __name__ == "__main__":
    unittest.main()
