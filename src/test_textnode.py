import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_noteq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is another text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_eqwithurl(self):
		node = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
		node2 = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
		self.assertEqual(node, node2)

	def test_noteqwithurl(self):
		node = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
		node2 = TextNode("This is a text node", TextType.ITALIC, "https://google.com")
		self.assertNotEqual(node, node2)

if __name__ == "__main__":
	unittest.main()
