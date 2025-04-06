from block import BlockType, text_to_blocktype
from htmlnode import HTMLNode, LeafNode, ParentNode
from parser import markdown_to_blocks, text_to_node


def markdown_to_html_node(markdown:str) -> HTMLNode:
    children:list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match text_to_blocktype(block):
            case BlockType.PARAGRAPH:
                children.append(_paragraph_to_htmlnode(block))
            case BlockType.HEADING:
                children.append(_heading_to_htmlnode(block))
            case BlockType.CODE:
                children.append(_code_to_htmlnode(block))
            case BlockType.QUOTE:
                children.append(_quote_to_htmlnode(block))
            case BlockType.UNORDERD_LIST:
                children.append(_unorderd_list_to_htmlnode(block))
            case BlockType.ORDERD_LIST:
                children.append(_orderd_list_to_htmlnode(block))
    node = ParentNode("div", children)
    return node

def _paragraph_to_htmlnode(text:str) -> HTMLNode:
    clean_text = text.replace("\n", " ")
    nodes = text_to_node(clean_text)
    if len(nodes) > 0:
        children:list[HTMLNode] = [n.to_html_node() for n in nodes]
        node = ParentNode("p", children)
        return node
    return LeafNode("p", "")

def _heading_to_htmlnode(text:str) -> HTMLNode:
    h = "h1"
    if text.startswith("## "):
        h = "h2"
        clean_text = text.lstrip("## ")
    elif text.startswith("### "):
        h = "h3"
        clean_text = text.lstrip("### ")
    elif text.startswith("#### "):
        h = "h4"
        clean_text = text.lstrip("#### ")
    elif text.startswith("##### "):
        h = "h5"
        clean_text = text.lstrip("##### ")
    elif text.startswith("###### "):
        h = "h6"
        clean_text = text.lstrip("###### ")
    else:
        clean_text = text.lstrip("# ")
    nodes = text_to_node(clean_text)
    if len(nodes) > 0:
        children:list[HTMLNode] = [n.to_html_node() for n in nodes]
        node = ParentNode(h, children)
        return node
    return LeafNode(h, "")

def _code_to_htmlnode(text:str) -> HTMLNode:
    clean_text = text.strip("```")
    node = ParentNode("pre", [LeafNode("code", clean_text)])
    return node

def _quote_to_htmlnode(text:str) -> HTMLNode:
    node = ParentNode("blockquote", [])
    node.children = []
    lines = text.split("\n")
    for line in lines:
        line_nodes = text_to_node(line.lstrip("> "))
        html_nodes = [n.to_html_node() for n in line_nodes]
        node.children.extend(html_nodes)
    return node

def _unorderd_list_to_htmlnode(text:str) -> HTMLNode:
    node = ParentNode("ul", [])
    lines = text.split("\n")
    node.children = []
    for line in lines:
        line_node = ParentNode("li", [])
        nodes = text_to_node(line.lstrip("- "))
        if len(nodes) > 0:
            line_node.children = [n.to_html_node() for n in nodes]
        node.children.append(line_node)
    return node

def _orderd_list_to_htmlnode(text:str) -> HTMLNode:
    node = ParentNode("ol",[])
    lines = text.split("\n")
    node.children = []
    for line in lines:
        line_node = ParentNode("li",[])
        clean_texts = line.split(".",1)
        if len(clean_texts) < 1:
            raise Exception("Invalid orderd list")
        clean_text = clean_texts[1]
        nodes = text_to_node(clean_text.lstrip())
        if len(nodes) > 0:
            line_node.children = [n.to_html_node() for n in nodes]
        node.children.append(line_node)
    return node
