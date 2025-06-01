from htmlnode import LeafNode
from textnode import TextType, TextNode
import re

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text })

        case _:
            raise Exception("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_node_list.append(node)
        else:
            split_text_list = node.text.split(delimiter)
            if len(split_text_list) % 2 == 0:
                raise Exception("Markdown had no closing delimiter")
            
            for i  in range(len(split_text_list)):
                if len(split_text_list[i]) == 0:
                    continue
                elif i % 2 == 0:
                    new_delimiter_node = TextNode(split_text_list[i], TextType.TEXT)
                    new_node_list.append(new_delimiter_node)
                else:
                    new_text_node = TextNode(split_text_list[i], text_type)
                    new_node_list.append(new_text_node)
            
    return new_node_list


def extract_markdown_images(text):
    extracted_list = []
    matches = re.findall(r"!\[.*?]\(.*?\)", text)
    for match in matches:
        image_link = re.findall(r"\(.*?\)", match)
        pure_image_link = image_link[0].replace('(', '').replace(')','')
        alt_text = re.findall(r"\[.*?\]", match)
        pure_alt_text = alt_text[0].replace('[', '').replace(']', '')
        extracted_list.append((pure_alt_text, pure_image_link))

    return extracted_list


def extract_markdown_links(text):
    extracted_list = []
    matches = re.findall(r"\[.*?]\(.*?\)", text)
    for match in matches:
        link = re.findall(r"\(.*?\)", match)
        pure_link = link[0].replace('(', '').replace(')','')
        alt_text = re.findall(r"\[.*?\]", match)
        pure_alt_text = alt_text[0].replace('[', '').replace(']', '')
        extracted_list.append((pure_alt_text, pure_link))

    return extracted_list

def split_nodes_link(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            currect_node_text = node.text
            matches = re.findall(r"\[.*?]\(.*?\)", currect_node_text)

            sections = re.split(r'(\[[^\]]+\]\([^)]+\))', currect_node_text)
            
            for section in sections:
                if section in matches:
                    abstracted_link = extract_markdown_links(section)
                    final_list.append(TextNode(abstracted_link[0][0], TextType.LINK, abstracted_link[0][1]))
                elif section.strip() == "":
                    continue
                else:
                    final_list.append(TextNode(section, TextType.TEXT))
    
    return final_list

def split_nodes_image(old_nodes):
    final_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_list.append(node)
        else:
            currect_node_text = node.text
            matches = re.findall(r"!\[.*?]\(.*?\)", currect_node_text)

            sections = re.split(r'(!\[[^\]]+\]\([^)]+\))', currect_node_text)
            for section in sections:
                if section in matches:
                    abstracted_image = extract_markdown_images(section)
                    final_list.append(TextNode(abstracted_image[0][0], TextType.IMAGE, abstracted_image[0][1]))
                elif section.strip() == "":
                    continue
                else:
                    final_list.append(TextNode(section, TextType.TEXT))
            
    return final_list


def text_to_textnodes(text):
    initial_node_list = [TextNode(text, TextType.TEXT)]

    extracted_by_bold = split_nodes_delimiter(initial_node_list, '**', TextType.BOLD)
    extracted_by_code = split_nodes_delimiter(extracted_by_bold, '`', TextType.CODE)
    extracted_by_italic = split_nodes_delimiter(extracted_by_code, '_', TextType.ITALIC)
    extracted_by_image = split_nodes_image(extracted_by_italic)
    extracted_by_link = split_nodes_link(extracted_by_image)

    return extracted_by_link

