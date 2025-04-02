import unittest

from parser import extract_markdown_images, extract_markdown_links, markdown_to_blocks, split_nodes_by_type, split_nodes_delimiter, text_to_node
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        n = TextNode("This is **bold** text", TextType.TEXT)
        res = split_nodes_delimiter([n], "**", TextType.BOLD)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text, "This is ")
        self.assertEqual(res[1].text, "bold")
        self.assertEqual(res[1].text_type, TextType.BOLD)
        self.assertEqual(res[2].text, " text")
        self.assertEqual(res[2].text_type, TextType.TEXT)

    def test_italic(self):
        n = TextNode("This is **bold** _text_", TextType.TEXT)
        res = split_nodes_delimiter([n], "_", TextType.ITALIC)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text, "This is **bold** ")
        self.assertEqual(res[1].text, "text")
        self.assertEqual(res[1].text_type, TextType.ITALIC)
        self.assertEqual(res[2].text, "")
        self.assertEqual(res[2].text_type, TextType.TEXT)

    def test_code(self):
        n = TextNode("`This` is **bold** _text_", TextType.TEXT)
        res = split_nodes_delimiter([n], "`", TextType.CODE)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text, "")
        self.assertEqual(res[1].text, "This")
        self.assertEqual(res[1].text_type, TextType.CODE)
        self.assertEqual(res[2].text, " is **bold** _text_")
        self.assertEqual(res[2].text_type, TextType.TEXT)

    def test_err(self):
        n = TextNode("wrong `codee", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            _ = split_nodes_delimiter([n], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "invalid markdown syntax")

class TestExtractMarkdownImages(unittest.TestCase):
    def test_1(self):
        txt = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_images(txt)
        alt = res[0][0]
        url = res[0][1]
        self.assertEqual(len(res), 1)
        self.assertEqual(alt, "rick roll")
        self.assertEqual(url, "https://i.imgur.com/aKaOqIh.gif")

    def test_2(self):
        txt = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(txt)
        self.assertEqual(len(res), 2)
        alt1 = res[0][0]
        url1 = res[0][1]
        self.assertEqual(alt1, "rick roll")
        self.assertEqual(url1, "https://i.imgur.com/aKaOqIh.gif")
        alt2 = res[1][0]
        url2 = res[1][1]
        self.assertEqual(alt2, "obi wan")
        self.assertEqual(url2, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_empty(self):
        txt = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![obi wan]() [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_images(txt)
        self.assertEqual(len(res), 2)
        alt1 = res[0][0]
        self.assertEqual(alt1, "")
        url2 = res[1][1]
        self.assertEqual(url2, "")

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_1(self):
        txt = "[rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_links(txt)
        alt = res[0][0]
        url = res[0][1]
        self.assertEqual(len(res), 1)
        self.assertEqual(alt, "rick roll")
        self.assertEqual(url, "https://i.imgur.com/aKaOqIh.gif")

    def test_2(self):
        txt = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_links(txt)
        self.assertEqual(len(res), 2)
        alt1 = res[0][0]
        url1 = res[0][1]
        self.assertEqual(alt1, "rick roll")
        self.assertEqual(url1, "https://i.imgur.com/aKaOqIh.gif")
        alt2 = res[1][0]
        url2 = res[1][1]
        self.assertEqual(alt2, "obi wan")
        self.assertEqual(url2, "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_empty(self):
        txt = "This is text with a [](https://i.imgur.com/aKaOqIh.gif) and [obi wan]() ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_links(txt)
        self.assertEqual(len(res), 3)
        alt1 = res[0][0]
        self.assertEqual(alt1, "")
        url2 = res[1][1]
        self.assertEqual(url2, "")

    # [image](https://i.imgur.com/zjjcJKZ.png))
    def test_double_bracket(self):
        txt = "[image](https://i.imgur.com/zjjcJKZ.png))"
        res = extract_markdown_links(txt)
        self.assertEqual(len(res), 1)
        alt1 = res[0][0]
        url1 = res[0][1]
        self.assertEqual(alt1, "image")
        self.assertEqual(url1, "https://i.imgur.com/zjjcJKZ.png")


    def no_extraction(self):
        txt = "This is some text"
        res = extract_markdown_links(txt)
        self.assertEqual(len(res), 0)

class TestSplitImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_by_type([node],extract_markdown_images)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_two_same(self):
        node = TextNode(
            "This ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png))",
            TextType.TEXT,
        )
        new_nodes = split_nodes_by_type([node],extract_markdown_images)
        self.assertListEqual(
            [
                TextNode("This ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(")", TextType.TEXT),
            ],
            new_nodes,
        )

class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_by_type([node],extract_markdown_links)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_two_same_links(self):
        node = TextNode(
            "This [image](https://i.imgur.com/zjjcJKZ.png) and another [image](https://i.imgur.com/zjjcJKZ.png))",
            TextType.TEXT,
        )
        new_nodes = split_nodes_by_type([node],extract_markdown_links)
        self.assertListEqual(
            [
                TextNode("This ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(")", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToNode(unittest.TestCase):
    def test1(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_node(text)
        self.assertEqual(res,
        [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    _ = unittest.main()
