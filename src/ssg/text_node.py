from enum import Enum

from ssg.leaf_node import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(textnode: TextNode) -> LeafNode:

    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=textnode.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=textnode.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=textnode.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=textnode.text)
        case TextType.LINK:
            if textnode.url == None:
                raise ValueError("LINK text node requires a url")
            return LeafNode(tag="a", value=textnode.text, props = {"href": textnode.url})
        case TextType.IMAGE:
            if textnode.url == None:
                raise ValueError("IMAGE text node requires a url")
            return LeafNode(tag="img", value="", props = { "src": textnode.url, "alt": textnode.text})
        case _:
            raise TypeError("TextNode - Invalid Type")
        
