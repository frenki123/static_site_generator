import unittest

from parser import split_nodes_delimiter
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



if __name__ == "__main__":
    _ = unittest.main()
