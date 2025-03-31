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

def extract_markdown_images(text:str) -> list[tuple[str,str]]:
    re_pattern = re.compile(r"\!\[(?P<alt>.+?)\]\((?P<url>.+?)\)")
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
