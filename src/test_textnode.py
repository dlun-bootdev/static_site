import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from sub_functions import split_nodes_delimiter


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

class TextTextNodeToHtml(unittest.TestCase):
    def test_text_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TextSplitNodesDelimiter(unittest.TestCase):
    def test_split_eq_CODE(self):
        node = TextNode("This is a `text` node", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_eq_ITALIC(self):
        node = TextNode("This is a text node _and something_ else", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is a text node ", TextType.TEXT),
            TextNode("and something", TextType.ITALIC),
            TextNode(" else", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_eq_ITALIC_two(self):
        node = TextNode("This is _a_ text node _and something_ else", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a", TextType.ITALIC),
            TextNode(" text node ", TextType.TEXT),
            TextNode("and something", TextType.ITALIC),
            TextNode(" else", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
    