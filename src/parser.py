from textnode import TextNode, TextType


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
