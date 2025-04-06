from typing import Callable
from textnode import TextNode, TextType
import re


def split_nodes_delimiter(nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes:list[TextNode] = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            values = node.text.split(delimiter)
            if len(values) == 0:
                new_nodes.append(node)
            if len(values) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i, val in enumerate(values):
                if i % 2 == 0:
                    new_nodes.append(TextNode(val, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(val, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

type extractor = Callable[[str], list[tuple[str,str]]]

def extract_markdown_images(text:str) -> list[tuple[str,str]]:
    re_pattern = re.compile(r"\!\[(?P<alt>.*?)\]\((?P<url>.*?)\)")
    matches:list[tuple[str,str]] = []
    for m in re.finditer(re_pattern, text):
        alt = m.group("alt")
        if not isinstance(alt, str):
            raise Exception("Invalid image syntax: missing alt text")
        url = m.group("url")
        if not isinstance(url, str):
            raise Exception("Invalid image syntax: missing url")
        matches.append((alt, url))
    return matches

def extract_markdown_links(text:str) -> list[tuple[str,str]]:
    re_pattern = re.compile(r"\[(?P<text>.*?)\]\((?P<url>.*?)\)")
    matches:list[tuple[str,str]] = []
    for m in re.finditer(re_pattern, text):
        txt = m.group("text")
        if not isinstance(txt, str):
            raise Exception("Invalid link syntax")
        url = m.group("url")
        if not isinstance(url, str):
            raise Exception("Invalid link syntax")
        matches.append((txt, url))
    return matches

def split_nodes_by_type(nodes:list[TextNode], extract:extractor):
    types = {str(extract_markdown_images):TextType.IMAGE,
             str(extract_markdown_links):TextType.LINK}
    text_type = types.get(str(extract))
    if text_type is None:
        raise Exception("Unsupported extractor")
    new_nodes:list[TextNode] = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            imgs = extract(text)
            if len(imgs) == 0:
                if node.text != "":
                    new_nodes.append(node)
                continue
            alt, url = imgs[0]
            spliter = f"[{alt}]({url})"
            if text_type == TextType.IMAGE:
                spliter = f"![{alt}]({url})"
            values = text.split(spliter,1)
            new_nodes.append(TextNode(values[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, text_type, url))
            if len(values) < 2:
                continue
            if values[1] != "":
                rest_nodes = split_nodes_by_type([TextNode(values[1], TextType.TEXT)],
                                                 extract)
                new_nodes.extend(rest_nodes)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_node(text:str) -> list[TextNode]:
    n = TextNode(text, TextType.TEXT)
    res_nodes = split_nodes_by_type([n], extract_markdown_images)
    res_nodes = split_nodes_by_type(res_nodes, extract_markdown_links)
    res_nodes = split_nodes_delimiter(res_nodes, "`", TextType.CODE)
    res_nodes = split_nodes_delimiter(res_nodes, "**", TextType.BOLD)
    res_nodes = split_nodes_delimiter(res_nodes, "_", TextType.ITALIC)
    return res_nodes

def markdown_to_blocks(markdown:str) -> list[str]:
    temp_blocks = markdown.split("\n\n")
    blocks: list[str] = []
    for block in temp_blocks:
        blocks.append(block.strip())
    return blocks

def extract_title(markdown:str) -> str:
    blocks = markdown_to_blocks(markdown)
    if len(blocks) < 1:
        raise Exception("No title")
    title = blocks[0]
    if not title.startswith("# "):
        raise Exception("No title")
    return title.lstrip("# ")
