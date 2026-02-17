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
