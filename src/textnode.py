from __future__ import annotations
from enum import Enum
from typing import override

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str|None = None):
        self.text:str = text
        self.text_type:TextType = text_type
        self.url:str|None = url

    @override
    def __eq__(self, other:object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD:
                return LeafNode("b", self.text)
            case TextType.ITALIC:
                return LeafNode("i", self.text)
            case TextType.CODE:
                return LeafNode("code", self.text)
            case TextType.LINK:
                url = "#"
                if self.url is not None:
                    url = self.url
                return LeafNode("a", self.text, {"href":url})
            case TextType.IMAGE:
                url = "#"
                if self.url is not None:
                    url = self.url
                return LeafNode("img", "", {"src":url,"alt":self.text})

