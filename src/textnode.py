import re
from enum import Enum

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold text"
	ITALIC = "italic text"
	CODE = "code text"
	LINK = "link"
	IMAGE = "image"

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

class TextNode:

	def __init__(self,text,text_type,url=None):
		self.text = text
		self.text_type = TextType(text_type)
		self.url = url
		super().__init__()

	def __eq__(self,other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
		return False

	def __repr__(self):
		return f"TextNode({self.text},{self.text_type.value},{self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	return_list = []
	for node in old_nodes:
		new_nodes = []
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			split_nodes = node.text.split(delimiter)
			if len(split_nodes) % 2 == 0:
				raise Exception("invalid Markdown syntax")
			next_node = TextType.TEXT
			for split_node in split_nodes:
				new_nodes.append(TextNode(split_node,next_node))
				if next_node == TextType.TEXT:
					next_node = text_type
				else:
					next_node = TextType.TEXT
		return_list.extend(new_nodes)
	return return_list

def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
	return matches

def split_nodes_image(old_nodes):
	return_list = []
	for node in old_nodes:
		new_nodes = []
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			images = extract_markdown_images(node.text)
			if len(images) == 0:
				new_nodes.append(node)
			else:
				for image in images:
					split_node = node.text.split(f"![{image[0]}]({image[1]})", 1)
					if len(split_node[0]) > 0:
						new_nodes.append(TextNode(split_node[0],TextType.TEXT))
					new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
					if len(split_node) > 1:
						node.text = split_node[1]
					else:
						node.text = ""
				if len(node.text) > 0:
					new_nodes.append(node)
		return_list.extend(new_nodes)
	return return_list

def split_nodes_link(old_nodes):
	return_list = []
	for node in old_nodes:
		new_nodes = []
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		else:
			links = extract_markdown_links(node.text)
			if len(links) == 0:
				new_nodes.append(node)
			else:
				for link in links:
					split_node = node.text.split(f"[{link[0]}]({link[1]})", 1)
					if len(split_node[0]) > 0:
						new_nodes.append(TextNode(split_node[0],TextType.TEXT))
					new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
					if len(split_node) > 1:
						node.text = split_node[1]
					else:
						node.text = ""
				if len(node.text) > 0:
					new_nodes.append(node)
		return_list.extend(new_nodes)
	return return_list

def block_to_block_type(markdown_block):
	lines = len(markdown_block.strip().splitlines())
	if len(re.findall(r"^#{1,6}\s",markdown_block)) > 0:
		return BlockType.HEADING
	elif markdown_block.startswith("```") and markdown_block.endswith("```"):
		return BlockType.CODE
	elif len(re.findall(r"^>",markdown_block,re.MULTILINE)) == lines:
		return BlockType.QUOTE
	elif len(re.findall(r"^- ",markdown_block,re.MULTILINE)) == lines:
		return BlockType.UNORDERED_LIST
	elif len(re.findall(r"^\d+\. ",markdown_block,re.MULTILINE)) == lines:
		counter = 1
		for line in markdown_block.strip().splitlines():
			char = 0
			num = ""
			while line[char] != ".":
				num = num + line[char]
				char += 1
			if int(num) != counter:
				return BlockType.PARAGRAPH
			counter += 1
		return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH

def text_to_textnodes(text):
	old_nodes = [TextNode(text,TextType.TEXT)]
	new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
	new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
	new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
	new_nodes = split_nodes_image(new_nodes)
	new_nodes = split_nodes_link(new_nodes)
	return new_nodes

def markdown_to_blocks(markdown):
	blocks = []
	split_markdown = markdown.split('\n\n')
	for block in split_markdown:
		block = block.strip()
		if block != "":
			blocks.append(block)
	return blocks