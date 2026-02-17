import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		node = HTMLNode("p", "Paragraph content", None, {"href": "https://boot.dev"})
		result = node.props_to_html()
		expectedresult = " href=\"https://boot.dev\""
		self.assertEqual(result, expectedresult)

	def test_props_to_html2(self):
		node = HTMLNode("p", "Paragraph content", None, {"href": "https://boot.dev", "alt": "BootDev website"})
		result = node.props_to_html()
		expectedresult = " href=\"https://boot.dev\" alt=\"BootDev website\""
		self.assertEqual(result, expectedresult)

	def test_props_to_html3(self):
		node = HTMLNode("p", "Paragraph content")
		result = node.props_to_html()
		expectedresult = ""
		self.assertEqual(result, expectedresult)