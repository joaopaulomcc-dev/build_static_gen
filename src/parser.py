import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split = node.text.split(delimiter)

        if node.text.find(delimiter) == 0:
            active_node_type = text_type
            alt_node_type = TextType.TEXT

        else:
            active_node_type = TextType.TEXT
            alt_node_type = text_type

        for item in split:
            if item == "":
                continue

            new_nodes.append(TextNode(text=item, text_type=active_node_type))
            active_node_type, alt_node_type = alt_node_type, active_node_type

    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
