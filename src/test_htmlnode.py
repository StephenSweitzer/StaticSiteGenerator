import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html_node, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, 'b')
		self.assertEqual(html_node.value, "This is a bold node")

	def test_italic(self):
		node = TextNode("This is an italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, 'i')
		self.assertEqual(html_node.value, "This is an italic node")

	def test_code(self):
		node = TextNode("This is a code node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, 'code')
		self.assertEqual(html_node.value, "This is a code node")

	def test_link(self):
		node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, 'a')
		self.assertEqual(html_node.value, "This is a link node")
		self.assertEqual(html_node.props, {"href": "https://boot.dev"})

	def test_image(self):
		node = TextNode("This is an image node", TextType.IMAGE, "https://boot.dev")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, 'img')
		self.assertEqual(html_node.props, {"src": "https://boot.dev", "alt": "This is an image node"})

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

	def test_to_html_with_children(self):
	    child_node = LeafNode("span", "child")
	    parent_node = ParentNode("div", [child_node])
	    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
	    grandchild_node = LeafNode("b", "grandchild")
	    child_node = ParentNode("span", [grandchild_node])
	    parent_node = ParentNode("div", [child_node])
	    self.assertEqual(
	        parent_node.to_html(),
	        "<div><span><b>grandchild</b></span></div>",
	    )

	def test_to_html_with_many_children(self):
	    child_node = LeafNode("span", "child")
	    child_node2 = LeafNode("p", "another child")
	    child_node3 = LeafNode("a", "anchor child", {"href": "https://boot.dev"})
	    parent_node = ParentNode("div", [child_node,child_node2,child_node3])
	    self.assertEqual(parent_node.to_html(), "<div><span>child</span><p>another child</p><a href=\"https://boot.dev\">anchor child</a></div>")

	def test_to_html_with_many_grandchildren(self):
	    grandchild_node = LeafNode("b", "grandchild")
	    grandchild_node2 = LeafNode("i", "italics grandchild")
	    grandchild_node3 = LeafNode("div", "div grandchild")
	    child_node = ParentNode("span", [grandchild_node,grandchild_node2,grandchild_node3])
	    parent_node = ParentNode("div", [child_node])
	    self.assertEqual(
	        parent_node.to_html(),
	        "<div><span><b>grandchild</b><i>italics grandchild</i><div>div grandchild</div></span></div>",
	    )

	def test_paragraphs(self):
		md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
			)

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
			)

	def test_quoteblock(self):
		md = """
> quote line 1
> quote line 2
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>quote line 1\nquote line 2</blockquote></div>",
			)

	def test_unorderedlistblock(self):
		md = """
- Unordered list 1
- Unordered list 2
- Unordered list 3
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>Unordered list 1</li><li>Unordered list 2</li><li>Unordered list 3</li></ul></div>",
			)

	def test_orderedlistblock(self):
		md = """
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
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>Ordered list 1</li><li>Ordered list 2</li><li>Ordered list 3</li><li>Ordered list 4</li><li>Ordered list 5</li><li>Ordered list 6</li><li>Ordered list 7</li><li>Ordered list 8</li><li>Ordered list 9</li><li>Ordered list 10</li></ol></div>",
			)

	def test_headingblock(self):
		md = """
##### Heading 5
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h5>Heading 5</h5></div>",
			)