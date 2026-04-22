import re
from textnode import *
from htmlnode import *


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


def text_to_textnodes(text):
    new_list = []
    new_list = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    new_list = split_nodes_delimiter(new_list, "_", TextType.ITALIC)
    new_list = split_nodes_delimiter(new_list, "`", TextType.CODE)
    new_list = split_nodes_image(new_list)
    new_list = split_nodes_link(new_list)
    return new_list


def markdown_to_blocks(markdown):
    temp_blocks = markdown.split("\n\n")
    blocks = []
    for block in temp_blocks:
        clear = block.strip()
        if clear != "":
            blocks.append(clear)
    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)