import unittest

from block import BlockType, text_to_blocktype

class TestTextToBlock(unittest.TestCase):
    def test_heading(self):
        h1 = "# asd"
        h3 = "### asd"
        self.assertEqual(text_to_blocktype(h1), BlockType.HEADING)
        self.assertEqual(text_to_blocktype(h3), BlockType.HEADING)

    def test_code(self):
        code = "```asdsadasdsda```"
        self.assertEqual(text_to_blocktype(code), BlockType.CODE)

    def test_paragraph(self):
        p1 = "sdasd"
        self.assertEqual(text_to_blocktype(p1), BlockType.PARAGRAPH)
        p2 = "-asdasd"
        self.assertEqual(text_to_blocktype(p2), BlockType.PARAGRAPH)
        p3 = """1. Par1
2. Par2
5. Par5"""
        self.assertEqual(text_to_blocktype(p3), BlockType.PARAGRAPH)

    def test_quote(self):
        q = """>asdasdsdasd
>asdasddas"""
        self.assertEqual(text_to_blocktype(q), BlockType.QUOTE)

    def test_unorderd(self):
        l = """- Unorderd1
- Unorderd2"""
        self.assertEqual(text_to_blocktype(l), BlockType.UNORDERD_LIST)

    def test_orderd(self):
        l = """1. Prvi
2. Drugi
3. Treci"""
        self.assertEqual(text_to_blocktype(l), BlockType.ORDERD_LIST)
