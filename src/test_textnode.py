import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node= TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text nodeww", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_type_eq(self):
        node= TextNode("This is a text node", TextType.BOLD)
        node2= TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.text_type.value, node2.text_type.value)

    def test_url_not_eq(self):
        node= TextNode("This is a text node", TextType.BOLD, "https://haha.com")
        node2= TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node.url, node2.url)

if __name__ == "__main__":
    unittest.main()
    