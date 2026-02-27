import unittest
from main import extract_title

class TestTextNode(unittest.TestCase):

	def test_extract_title(self):
		md = """
# Heading 1

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		title = extract_title(md)
		self.assertEqual(
			title,
			"Heading 1")
