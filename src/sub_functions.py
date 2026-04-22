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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_list = extract_markdown_images(node.text)

        if len(image_list) == 0:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        
        sections = []
        left_over_text = node.text
        for alt, url in image_list:
            sections = left_over_text.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            left_over_text = sections[1]
        
        if left_over_text != "":
            new_nodes.append(TextNode(left_over_text, TextType.TEXT))
        
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_list = extract_markdown_links(node.text)

        if len(link_list) == 0:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        
        sections = []
        left_over_text = node.text
        for alt, url in link_list:
            sections = left_over_text.split(f"[{alt}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            left_over_text = sections[1]

        if left_over_text != "":
            new_nodes.append(TextNode(left_over_text, TextType.TEXT))
        
    return new_nodes


