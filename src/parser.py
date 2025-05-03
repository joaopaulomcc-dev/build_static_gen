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
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        temp_nodes = [node]

        for img_data in images:
            img_nodes = []
            alt_text = img_data[0]
            src = img_data[1]
            img_str = f"![{alt_text}]({src})"

            for temp_node in temp_nodes:
                if node.text_type is not TextType.TEXT:
                    img_nodes.append(temp_node)
                    continue

                if img_str not in temp_node.text:
                    img_nodes.append(temp_node)
                    continue

                split_text = temp_node.text.split(img_str)

                for i, split in enumerate(split_text):
                    if split == "":
                        img_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=src))

                    elif i < len(split_text) - 1 and split_text[i + 1] != "":
                        img_nodes.append(TextNode(text=split, text_type=TextType.TEXT))
                        img_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=src))

                    else:
                        img_nodes.append(TextNode(text=split, text_type=TextType.TEXT))

            temp_nodes = img_nodes

        new_nodes.extend(temp_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        temp_nodes = [node]

        for link_data in links:
            link_nodes = []
            anchor_text = link_data[0]
            href = link_data[1]
            link_str = f"[{anchor_text}]({href})"

            for temp_node in temp_nodes:
                if node.text_type is not TextType.TEXT:
                    link_nodes.append(temp_node)
                    continue

                if link_str not in temp_node.text:
                    link_nodes.append(temp_node)
                    continue

                split_text = temp_node.text.split(link_str)

                for i, split in enumerate(split_text):
                    if split == "":
                        link_nodes.append(
                            TextNode(text=anchor_text, text_type=TextType.LINK, url=href)
                        )

                    elif i < len(split_text) - 1 and split_text[i + 1] != "":
                        link_nodes.append(TextNode(text=split, text_type=TextType.TEXT))
                        link_nodes.append(
                            TextNode(text=anchor_text, text_type=TextType.LINK, url=href)
                        )

                    else:
                        link_nodes.append(TextNode(text=split, text_type=TextType.TEXT))

            temp_nodes = link_nodes

        new_nodes.extend(temp_nodes)

    return new_nodes


def text_to_textnodes(text: str):
    text_node = TextNode(text=text, text_type=TextType.TEXT)

    # extract bold
    nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)

    # extract italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # extract code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # extract image
    nodes = split_nodes_image(nodes)

    # extract links
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown: str):
    original_blocks = markdown.split("\n\n")

    blocks = []

    for block in original_blocks:
        lines = block.split("\n")

        for line in lines:
            if line.strip() != "":
                block = "\n".join([line.strip() for line in lines if line.strip() != ""])

        if block != "":
            blocks.append(block)

    return blocks
