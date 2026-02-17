from htmlnode import HTMLNode

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