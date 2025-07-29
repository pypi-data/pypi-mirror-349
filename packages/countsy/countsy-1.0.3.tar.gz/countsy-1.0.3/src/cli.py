import glob
import os
import argparse

# TODO: Ignore blank lines, ignore comments

def return_all_files_in_folder(folder_path: str) -> list or str:
	"""
	Returns all Python-Files in a given folder that have been found recursively if folder_path is valid
	:param folder_path:
	:return: all_python_files:
	"""
	if not os.path.isdir(folder_path):
		return f"{folder_path} is not a valid folder path or you lack permission to access the folder."
	return glob.glob(folder_path + '/**/*.py', recursive=True)


def return_lines_of_code(filename: str) -> int:
	"""
	Returns the line length of a given file. Does not ignore blank lines or comments.
	:param filename:
	:return: file_length:
	"""
	with open(filename) as f:
		return len(f.read().split('\n'))


def return_sum_of_lines_in_folder(list_of_files):
	"""
	Returns the sum of all single lengths of code
	:param list_of_files:
	:return:
	"""
	return sum([return_lines_of_code(el) for el in list_of_files])


def init_parser():
	"""
	Initializes parser and returns the folder path
	:return: folder_path
	"""
	parser = argparse.ArgumentParser(description="Count total lines of Python code in a folder.")
	parser.add_argument(
		"folder_path",
		help="Path to the folder containing Python files",
		nargs='?',
		default=None
	)
	args = parser.parse_args()
	
	if args.folder_path is None:
		parser.print_help()
		parser.exit()
		
	return args.folder_path


def main():
	folder_path = init_parser()
	all_python_files = return_all_files_in_folder(folder_path)
	
	# If returned element is a list, the folder_path was valid
	if isinstance(all_python_files, list):
		# If returned list is empty, no Python-Files have been found
		if not all_python_files:
			print(f"There are no Python-Files in {folder_path}")
		else:
			print("Total lines of Python-Code in folder: ", return_sum_of_lines_in_folder(all_python_files))
	# Prints error message
	else:
		print(all_python_files)
	