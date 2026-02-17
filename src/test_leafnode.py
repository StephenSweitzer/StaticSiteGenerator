import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_a(self):
		node = LeafNode("a", "Click Here",{"href": "https://boot.dev"})
		self.assertEqual(node.to_html(), "<a href=\"https://boot.dev\">Click Here</a>")

	def test_leaf_to_html_h1(self):
		node = LeafNode("h1", "Heading1")
		self.assertEqual(node.to_html(), "<h1>Heading1</h1>")

	def test_leaf_to_html_img(self):
		node = LeafNode("img", "Alt text",{"src": "https://boot.dev/image.jpg", "alt": "Alt text"})
		self.assertEqual(node.to_html(), "<img src=\"https://boot.dev/image.jpg\" alt=\"Alt text\">Alt text</img>")