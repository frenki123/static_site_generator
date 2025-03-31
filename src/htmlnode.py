from __future__ import annotations
from typing import override

class HTMLNode:
    def __init__(self, tag:str|None=None, value:str|None=None,
                 children:list[HTMLNode]|None=None, props:dict[str,str]|None=None):
        self.tag:str|None = tag
        self.value:str|None = value
        self.children:list[HTMLNode]|None = children
        self.props:dict[str,str]|None = props

    @override
    def __repr__(self) -> str:
        return f"HTMLNode(tag:{self.tag} value:{self.value} children:{self.children} props:{self.props}"

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        res:list[str] = []
        for key, value in self.props.items():
            res.append(f"{key}=\"{value}\"")
        return " ".join(res)

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str,  props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str,str]|None=None):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have a children")
        res:list[str] = [] 
        for child in self.children:
            res.append(child.to_html())
        return f'<{self.tag}>{"".join(res)}</{self.tag}>'
