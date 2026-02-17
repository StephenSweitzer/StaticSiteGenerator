from textnode import TextNode

def main():
	node = TextNode("Test","text","https://bootdev.com")
	print(f"{node.__repr__()}")

main()