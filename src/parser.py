import re

from blocks import BlockType
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


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


def markdown_to_blocks(markdown: str) -> list[str]:
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


def block_to_block_type(markdown: str):
    heading_pattern = re.compile(r"^#{1,6} .+")
    lines = markdown.splitlines()

    if re.match(heading_pattern, markdown):
        return BlockType.HEADING

    if (len(markdown) > 3) and (markdown[:3] == "```") and (markdown[-3:] == "```"):
        return BlockType.CODE

    if all([line[0] == ">" for line in lines]):
        return BlockType.QUOTE

    if all([line[:2] == "- " for line in lines]):
        return BlockType.UNORDERED_LIST

    if all(
        [
            line.split()[0] == f"{i}."
            for i, line in enumerate(lines, start=1)
            if len(line.splitlines()) > 0
        ]
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(markdown: str):
    text_nodes = text_to_textnodes(markdown)
    html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]

    return html_nodes


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    blocks_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                n_hash = block.split()[0].count("#")
                n_hash = n_hash if n_hash <= 6 else 6

                children = text_to_children(block)
                block_node = ParentNode(tag=f"h{n_hash}", children=[children])

            case BlockType.CODE:
                code_text_node = TextNode(
                    text=block.replace("```", "").lstrip(), text_type=TextType.CODE
                )
                code_html_node = text_node_to_html_node(code_text_node)
                block_node = ParentNode(tag="pre", children=[code_html_node])

            case BlockType.QUOTE:
                children = text_to_children(block)
                block_node = ParentNode(tag="blockquote", children=[children])

            case BlockType.UNORDERED_LIST:
                children = []
                for line in block.splitlines():
                    line_nodes = text_to_children(line)
                    line_node = ParentNode(tag="li", children=line_nodes)
                    children.append(line_node)

                block_node = ParentNode(tag="ul", children=children)

            case BlockType.ORDERED_LIST:
                children = []
                for line in block.splitlines():
                    line_nodes = text_to_children(line)
                    line_node = ParentNode(tag="li", children=line_nodes)
                    children.append(line_node)

                block_node = ParentNode(tag="ol", children=children)

            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                block_node = ParentNode(tag="p", children=children)

        blocks_nodes.append(block_node)

    return ParentNode(tag="div", children=blocks_nodes)
