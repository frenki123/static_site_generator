import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_repl(self):
        n1 = HTMLNode("<a1>", "text")
        self.assertEqual(str(n1),
                         "HTMLNode(tag:<a1> value:text children:None props:None")
    def test_property(self):
        n1 = HTMLNode("","",None,{
           "href": "https://www.google.com",
            "target": "_blank",})
        self.assertEqual(n1.props_to_html(),
                         'href="https://www.google.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test1(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), 
                         '<a href="https://www.google.com">Click me!</a>')
    def test3(self):
        node = LeafNode(None, "This is a text.")
        self.assertEqual(node.to_html(), "This is a text.")

    def test4(self):
        with self.assertRaises(ValueError) as context:
            node = LeafNode(None, None) # pyright: ignore[reportArgumentType]
            _ = node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value")
if __name__ == "__main__":
    _ = unittest.main()
