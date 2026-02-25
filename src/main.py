import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
	node = TextNode("Test","text","https://bootdev.com")
	print(f"{node.__repr__()}")

main()