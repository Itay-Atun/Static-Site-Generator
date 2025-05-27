from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import split_nodes_delimiter


def main():
    node = TextNode("This is text with a **code block** word", TextType.TEXT)
    node2 = TextNode("**code block**", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node2], "**", TextType.BOLD)

    print(new_nodes)


if __name__ == "__main__":
    main()
