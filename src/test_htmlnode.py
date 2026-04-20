import unittest

from htmlnode import HTMLNode


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
        node2 = HTMLNode("This is tag", "This is value", "This is a children")
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')


if __name__ == "__main__":
    unittest.main()