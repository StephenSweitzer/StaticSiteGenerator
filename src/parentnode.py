from htmlnode import HTMLNode

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
