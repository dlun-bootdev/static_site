import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is tag", "This is value", "This is a children")
        node2 = HTMLNode("This is tag", "This is value", "This is a children")
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_not_eq(self):
        node= HTMLNode("This is tag", "This is value", "This is a children", {"href": "https://www.google.com",
        "target": "_blank",})
        node2 = HTMLNode("This is a tag", "This is value", "This is a children")
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())
    
    def test_eq2(self):
        node = HTMLNode("This is tag", "This is value", "This is a children", {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click this link!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click this link!</a>')

    def test_leaf_to_html_p_not_eq(self):
        node = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<a>Hello, world!</p>")

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

if __name__ == "__main__":
    unittest.main()