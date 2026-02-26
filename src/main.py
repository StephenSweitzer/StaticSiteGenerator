import re
import os
import shutil

def main():
	copy_static_to_public()

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


main()