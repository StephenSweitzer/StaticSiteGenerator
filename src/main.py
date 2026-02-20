import re
from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
	node = TextNode("Test","text","https://bootdev.com")
	print(f"{node.__repr__()}")

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT:
		return_value = LeafNode(None, text_node.text)
	elif text_node.text_type == TextType.BOLD:
		return_value = LeafNode("b", text_node.text)
	elif text_node.text_type == TextType.ITALIC:
		return_value = LeafNode("i", text_node.text)
	elif text_node.text_type == TextType.CODE:
		return_value = LeafNode("code", text_node.text)
	elif text_node.text_type == TextType.LINK:
		return_value = LeafNode("a", text_node.text, {'href': text_node.url})
	elif text_node.text_type == TextType.IMAGE:
		return_value = LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
	else:
		raise Exception("Unknown type")
	return return_value

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






main()