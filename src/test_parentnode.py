import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):

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