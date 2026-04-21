import re
from textnode import TextNode, TextType



def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_str = node.text.split(delimiter)
        if len(split_str) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        text = True
        for split in split_str:
            if text:
                new_nodes.append(TextNode(split, TextType.TEXT))
                text = False
            else:
                new_nodes.append(TextNode(split, text_type))
                text = True
    return new_nodes