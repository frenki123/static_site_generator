import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "someurl")
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        txt = TextNode("some text", TextType.TEXT)
        n = txt.to_html_node()
        self.assertEqual(n.tag, None)
        self.assertEqual(n.value, "some text")

    def test_bold(self):
        txt = TextNode("some text", TextType.BOLD)
        n = txt.to_html_node()
        self.assertEqual(n.tag, "b")
        self.assertEqual(n.value, "some text")

    def test_italic(self):
        txt = TextNode("some text", TextType.ITALIC)
        n = txt.to_html_node()
        self.assertEqual(n.tag, "i")
        self.assertEqual(n.value, "some text")

    def test_code(self):
        txt = TextNode("some text", TextType.CODE)
        n = txt.to_html_node()
        self.assertEqual(n.tag, "code")
        self.assertEqual(n.value, "some text")

    def test_link(self):
        txt = TextNode("some text", TextType.LINK, "someurl")
        n = txt.to_html_node()
        self.assertEqual(n.tag, "a")
        self.assertEqual(n.value, "some text")
        self.assertEqual(n.props, {"href":"someurl"})

    def test_link_no_url(self):
        txt = TextNode("some text", TextType.LINK)
        n = txt.to_html_node()
        self.assertEqual(n.tag, "a")
        self.assertEqual(n.value, "some text")
        self.assertEqual(n.props, {"href":"#"})

    def test_img(self):
        txt = TextNode("image", TextType.IMAGE, "someurl")
        n = txt.to_html_node()
        self.assertEqual(n.tag, "img")
        self.assertEqual(n.value, "")
        self.assertEqual(n.props, {"alt":"image", "src":"someurl"})

if __name__ == "__main__":
    _ = unittest.main()
