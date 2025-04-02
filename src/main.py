from parser import *
from textnode import TextNode, TextType


def test_split_images():
    node = TextNode(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [image](https://i.imgur.com/zjjcJKZ.png))",
        TextType.TEXT,
    )
    new_nodes = split_nodes_by_type([node],extract_markdown_links)
    print(new_nodes)
    res = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(")", TextType.TEXT),
        ]
    print(res)

test_split_images()
