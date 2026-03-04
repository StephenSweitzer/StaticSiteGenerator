import re
import os
import shutil
from htmlnode import HTMLNode, markdown_to_html_node

def main():
	print("Running...")
	copy_static_to_public()
	generate_pages_recursive("./content", "./template.html", "./public")

def copy_static_to_public():
	if not os.path.exists('./public'):
		raise Exception("public directory cannot be found")
	print("public directory found")
	shutil.rmtree('./public')
	print("deleted public directory")
	os.mkdir('./public')
	print("recreated public directory")
	copy_contents('./static', './public')
	print("copied contents to public directory")

def copy_contents(source, destination):
	print(f"copying: {source} to {destination}")
	if not os.path.exists(source) and not os.path.isfile(source):
		raise Exception("could not find source directory")
	if not os.path.exists(destination) and not os.path.isfile(destination):
		raise Exception("could not find destination directory")
	files = os.listdir(source)
	print(f"files found: {files}")
	for file in files:
		if not os.path.isfile(os.path.join(source, file)):
			print(f"found directory: {os.path.join(source, file)}")
			os.mkdir(os.path.join(destination, file))
			print(f"recursive call: {os.path.join(source, file)} to {os.path.join(destination, file)}")
			copy_contents(os.path.join(source, file), os.path.join(destination, file))
		else:
			print(f"attempting to copy {os.path.join(source, file)}")
			shutil.copy(os.path.join(source, file), os.path.join(destination, file))

def extract_title(markdown):
	lines = markdown.split('\n')
	for line in lines:
		if line.startswith('# '):
			title = line[2:].strip()
			return title
	raise Exception("no heading 1 in content for title")

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	if not os.path.exists(from_path):
		raise Exception(f"{from_path} cannot be found")
	with open(from_path) as f:
		markdown = f.read()
	if not os.path.exists(template_path):
		raise Exception(f"{template_path} cannot be found")
	with open(template_path) as f:
		template = f.read()
	htmlnode = markdown_to_html_node(markdown)
	html = htmlnode.to_html()
	title = extract_title(markdown)
	template = template.replace("{{ Title }}", title).replace("{{ Content }}",html)
	print(f"HTML Page: {template}")
	try:
		os.makedirs(os.path.dirname(dest_path), exist_ok=True)
		with open(dest_path, "w") as f:
			f.write(template)
	except Exception as e:
		print(f"Error: an error occurred when writing the file contents: {e}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	print(f"Scanning content directory: {dir_path_content}")
	if not os.path.exists(dir_path_content) or os.path.isfile(dir_path_content):
		raise Exception("could not find directory {dir_path_content}")
	if not os.path.exists(template_path):
		raise Exception(f"{template_path} cannot be found")
	files = os.listdir(dir_path_content)
	for file in files:
		if not os.path.isfile(os.path.join(dir_path_content, file)):
			print(f"Found directory: {file}")
			generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
		elif file[0] != ".":
			sourcename = os.path.join(dir_path_content, file)
			destinationname = os.path.join(dest_dir_path, file[:-2] + "html")
			generate_page(sourcename, template_path, destinationname)

main()