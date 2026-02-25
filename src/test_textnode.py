import unittest

from textnode import TextNode, TextType, BlockType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, block_to_block_type, markdown_to_blocks, text_to_textnodes

class TestTextNode(unittest.TestCase):

	def test_split_nodes_code(self):
		old_nodes = []
		old_nodes.append(TextNode("This is text with a `code block` word", TextType.TEXT))
		self.assertEqual(split_nodes_delimiter(old_nodes,"`",TextType.CODE),[TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),])

	def test_split_nodes_bold(self):
		old_nodes = []
		old_nodes.append(TextNode("This is text with two **bolded** words in **bold**.", TextType.TEXT))
		self.assertEqual(split_nodes_delimiter(old_nodes,"**",TextType.BOLD),[TextNode("This is text with two ", TextType.TEXT),
			TextNode("bolded", TextType.BOLD),
			TextNode(" words in ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(".", TextType.TEXT)])

	def test_split_nodes_italic(self):
		old_nodes = []
		old_nodes.append(TextNode("This is text with an _italic block_ word", TextType.TEXT))
		self.assertEqual(split_nodes_delimiter(old_nodes,"_",TextType.ITALIC),[TextNode("This is text with an ", TextType.TEXT),
			TextNode("italic block", TextType.ITALIC),
			TextNode(" word", TextType.TEXT),])

	def test_split_nodes_invalidmarkdown(self):
		old_nodes = [TextNode("This is text with an invalid `markdown` section `in it", TextType.TEXT)]
		with self.assertRaisesRegex(Exception, "invalid Markdown syntax"):
			split_nodes_delimiter(old_nodes, "`", TextType.CODE)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
			)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
			)
		self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
			)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
			TextNode("This is text with an ", TextType.TEXT),
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" and another ", TextType.TEXT),
			TextNode(
				"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
			)

	def test_split_images2(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png) image at start of text",
			TextType.TEXT,
			)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" image at start of text", TextType.TEXT),
			],
			new_nodes,
			)

	def test_split_images3(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png) image at start of text and a link at the end [to boot dev](https://www.boot.dev)",
			TextType.TEXT,
			)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" image at start of text and a link at the end [to boot dev](https://www.boot.dev)", TextType.TEXT),
			],
			new_nodes,
			)

	def test_split_links(self):
		node = TextNode(
			"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
			TextType.TEXT,
			)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
			TextNode("This is text with a link ", TextType.TEXT),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT),
			TextNode(
				"to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
				),
			],
			new_nodes,
			)

	def test_split_links2(self):
		node = TextNode(
			"[to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com/@bootdotdev)",
			TextType.TEXT,
			)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and another ", TextType.TEXT),
			TextNode(
				"to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
				),
			],
			new_nodes,
			)

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

	def test_block_to_block_type_heading(self):
		blocktype = block_to_block_type("### Heading content")
		self.assertEqual(BlockType.HEADING, blocktype)

	def test_block_to_block_type_pcode(self):
		blocktype = block_to_block_type("```code block```")
		self.assertEqual(BlockType.CODE, blocktype)

	def test_block_to_block_type_pcode(self):
		ml = """
> quote line 1
> quote line 2
"""
		blocktype = block_to_block_type(ml)
		self.assertEqual(BlockType.QUOTE, blocktype)

	def test_block_to_block_type_pcode(self):
		ml = """
- Unordered list 1
- Unordered list 2
- Unordered list 3
"""
		blocktype = block_to_block_type(ml)
		self.assertEqual(BlockType.UNORDERED_LIST, blocktype)

	def test_block_to_block_type_pcode(self):
		ml = """
1. Ordered list 1
2. Ordered list 2
3. Ordered list 3
4. Ordered list 4
5. Ordered list 5
6. Ordered list 6
7. Ordered list 7
8. Ordered list 8
9. Ordered list 9
10. Ordered list 10
"""
		blocktype = block_to_block_type(ml)
		self.assertEqual(BlockType.ORDERED_LIST, blocktype)

	def test_block_to_block_type_paragraph(self):
		blocktype = block_to_block_type("paragraph content")
		self.assertEqual(BlockType.PARAGRAPH, blocktype)

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		new_nodes = text_to_textnodes(text)
		self.assertListEqual(
			[
			TextNode("This is ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev")
			],
			new_nodes,
			)

	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
			"This is **bolded** paragraph",
			"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
			"- This is a list\n- with items",
			],
			)

if __name__ == "__main__":
	unittest.main()
