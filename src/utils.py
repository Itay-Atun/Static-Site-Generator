from htmlnode import LeafNode
from textnode import TextType, TextNode


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
