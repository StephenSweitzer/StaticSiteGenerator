from textnode import TextNode, TextType, BlockType, text_to_textnodes, block_to_block_type, markdown_to_blocks

class HTMLNode:

	def __init__(self,tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
		super().__init__()

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		return_value = ""
		if self.props == None or len(self.props) == 0:
			return ""
		for prop in self.props:
			return_value = return_value + " " + prop + "=\"" + self.props[prop] + "\""
		return return_value

	def __repr__(self):
		return f"HTMLNode: ({self.tag},{self.value},{self.children}, {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		self.tag = tag
		self.value = value
		self.props = props
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value == None or self.value == "":
			raise ValueError("all leaf nodes must have a value")
		if self.tag == None:
			return self.value
		return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"

	def __repr__(self):
		return f"LeafNode: ({self.tag},{self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self,tag, children, props=None):
		self.tag = tag
		self.children = children
		self.props = props
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag == None or self.tag == "":
			raise ValueError("all parent nodes must have a tag")
		if self.children == None or self.children == "" or len(self.children) == 0:
			raise ValueError("all parent nodes must have children")
		return_value = "<" + self.tag + ">"
		for child in self.children:
			child_html = child.to_html()
			return_value = return_value + child_html
		return_value = return_value + "</" + self.tag + ">"
		return return_value

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
		return_value = LeafNode("img", text_node.text, {'src': text_node.url, 'alt': text_node.text})
	else:
		raise Exception("Unknown type")
	return return_value

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	return_value = ParentNode('div', [])
	for block in blocks:
		blocktype = block_to_block_type(block)
		if blocktype == BlockType.PARAGRAPH:
			block = block.replace('\n',' ')
			children_htmlnodes = text_to_children(block)
			block_parent = ParentNode('p', children_htmlnodes)
		elif blocktype == BlockType.CODE:
			children_htmlnodes = []
			block = block[3:-3]
			if block[:1] == "\n":
				block = block[1:]
			if block[1:] == "\n":
				block = block[:1]
			textnode = TextNode(block,TextType.CODE)
			children_htmlnodes.append(text_node_to_html_node(textnode))
			block_parent = ParentNode('pre', children_htmlnodes)
		elif blocktype == BlockType.QUOTE:
			lines = block.split('\n')
			new_block = []
			for line in lines:
				new_block.append(line[2:])
			block = "\n".join(new_block)
			block_parent = LeafNode('blockquote',block)
		elif blocktype == BlockType.UNORDERED_LIST:
			lines = block.split('\n')
			blocklines = []
			for line in lines:
				line = line[1:].strip()
				nodes = text_to_children(line.strip())
				linenodes = []
				for node in nodes:
					linenodes.append(node)
				listitem_htmlnodes = ParentNode('li',linenodes)
				blocklines.append(listitem_htmlnodes)
			block_parent = ParentNode('ul', blocklines)
		elif blocktype == BlockType.ORDERED_LIST:
			lines = block.split('\n')
			blocklines = []
			for line in lines:
				splitline = line.split('.', 1)
				nodes = text_to_children(splitline[1].strip())
				linenodes = []
				for node in nodes:
					linenodes.append(node)
				listitem_htmlnodes = ParentNode('li',linenodes)
				blocklines.append(listitem_htmlnodes)
			block_parent = ParentNode('ol', blocklines)
		elif blocktype == BlockType.HEADING:
			children_htmlnodes = []
			heading_count = len(block) - len(block.lstrip('#'))
			heading_level = "h" + str(heading_count)
			children_htmlnodes = text_to_children(block.lstrip('#').strip())
			block_parent = ParentNode(heading_level, children_htmlnodes)
		else:
			raise Exception('Unknown BlockType')
		return_value.children.append(block_parent)
	return return_value

def text_to_children(block):
	children_nodes = []
	textnodes = text_to_textnodes(block)
	for textnode in textnodes:
		children_nodes.append(text_node_to_html_node(textnode))
	return children_nodes
