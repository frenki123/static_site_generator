import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )   

    def test_err(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("tag", None, None) # pyright: ignore[reportArgumentType]
            _ = node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a children")

        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode(None, "ERROR")], None) # pyright: ignore[reportArgumentType]
            _ = node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test1(self):
        c1 = LeafNode("span", "child")
        c2 = LeafNode("b", "child")
        p1 = ParentNode("p", [c1,c2])
        p2 = ParentNode("p", [p1])
        x1 = ParentNode("x", [p2])
        c3 = LeafNode(None, "text")
        parent_node = ParentNode("div", [c1,c2,x1,c3,p1])
        self.assertEqual(parent_node.to_html(), 
        "<div><span>child</span><b>child</b><x><p><p><span>child</span><b>child</b></p></p></x>text<p><span>child</span><b>child</b></p></div>")

    def test2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), 
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    _ = unittest.main()
