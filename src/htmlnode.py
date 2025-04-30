from typing import Self


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[Self] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is not None:
            key_values = [f'{key}="{value}"' for key, value in self.props.items()]
            return " " + " ".join(key_values)
        else:
            return ""

    def __repr__(self):
        print(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError()

        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError()

        if self.children is None:
            raise ValueError()

        children_str = "".join([child.to_html() for child in self.children])

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
