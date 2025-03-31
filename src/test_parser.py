import unittest

from parser import extract_markdown_images, split_nodes_delimiter
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

if __name__ == "__main__":
    _ = unittest.main()
