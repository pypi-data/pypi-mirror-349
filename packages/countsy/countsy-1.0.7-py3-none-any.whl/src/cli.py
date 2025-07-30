import glob
import os
import argparse
from tqdm import tqdm

# TODO: more programming languages

def return_all_files_in_folder(folder_path: str) -> list or str:
	"""
	Returns all Python-Files in a given folder that have been found recursively if folder_path is valid
	:param folder_path:
	:return: all_python_files:
	"""
	if os.path.isfile(folder_path):
		return [folder_path]
	if not os.path.isdir(folder_path):
		return f"{folder_path} is not a valid folder path or you lack permission to access the folder."
	return glob.glob(folder_path + '/**/*.py', recursive=True)


def return_lines_of_uncommented_code(file: list) -> int:
	ctr = 0
	multiline_comment_flag = False
	for el in file:
		stripped = el.strip()
		if stripped.startswith('#'):
			continue
		if stripped.startswith("\"\"\"") or (multiline_comment_flag and stripped.endswith("\"\"\"")):
			multiline_comment_flag = not multiline_comment_flag
			continue
		if multiline_comment_flag:
			continue
		ctr += 1
	return ctr


def return_lines_of_non_blank_code(file: list) -> int:
	ctr = 0
	multiline_comment_flag = False
	for el in file:
		stripped = el.strip()
		if stripped != "":
			ctr += 1
	return ctr


def return_lines_of_non_blank_uncommented_code(file: list) -> int:
	ctr = 0
	multiline_comment_flag = False
	for el in file:
		stripped = el.strip()
		if stripped.startswith('#'):
			continue
		# Check for multiline comment start/end
		if stripped.startswith('"""') or (multiline_comment_flag and stripped.endswith('"""')):
			multiline_comment_flag = not multiline_comment_flag
			continue
		# Skip if inside multiline comment
		if multiline_comment_flag:
			continue
		# Check if line is non-blank
		if stripped != "":
			ctr += 1
	return ctr
	

def return_lines_of_code(filename: str, args) -> int:
	"""
	Returns the line length of a given file. Does not ignore blank lines or comments.
	:param filename:
	:param args: arg parser arguments
	:return: file_length:
	"""
	ignore_blank_lines = args.ignore_blank_lines
	ignore_comments = args.ignore_comments
	
	with open(filename) as f:
		file = f.read().split('\n')
		if not ignore_blank_lines and not ignore_comments:
			return len(file)
		elif ignore_blank_lines and not ignore_comments:
			return return_lines_of_non_blank_code(file)
		elif not ignore_blank_lines and ignore_comments:
			return return_lines_of_uncommented_code(file)
		elif ignore_blank_lines and ignore_comments:
			return return_lines_of_non_blank_uncommented_code(file)
		return 0


def return_sum_of_lines_in_folder(list_of_files, args):
	"""
	Returns the sum of all single lengths of code
	:param list_of_files:
	:param args: arg parser arguments
	:return:
	"""
	use_tqdm = args.tqdm
	
	if len(list_of_files) == 1:
		return return_lines_of_code(list_of_files[0], args)
	if use_tqdm:
		return sum([return_lines_of_code(el, args) for el in tqdm(list_of_files)])
	else:
		return sum([return_lines_of_code(el, args) for el in list_of_files])


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
		default="./"
	)
	parser.add_argument(
		"--tqdm",
		help="Includes progress bar",
		action="store_true",
		default=False
	)
	parser.add_argument(
		"--ignore-comments",
		help="Ignores counting comments.",
		action="store_true",
		default=False
	)
	parser.add_argument(
		"--ignore-blank-lines",
		help="Ignores counting blank lines.",
		action="store_true",
		default=False
	)
	parser.add_argument(
		"--ignore-blank-lines-in-comments",
		help="Ignores counting all blank lines.",
		action="store_true",
		default=False
	)
	
	parser.add_argument(
		"--ignore",
		help="Ignores both comments and blank lines (eq. to 'countsy --ignore-blank-lines --ignore-comments",
		action="store_true",
		default=False
	)
	
	args = parser.parse_args()
	
	if args.ignore:
		args.ignore_blank_lines = True
		args.ignore_comments = True

	return args


def main():
	args = init_parser()
	
	all_python_files = return_all_files_in_folder(args.folder_path)
	
	# If returned element is a list, the folder_path was valid
	if isinstance(all_python_files, list):
		# If returned list is empty, no Python-Files have been found
		if not all_python_files:
			print(f"There are no Python-Files in {args.folder_path}")
		else:
			if len(all_python_files) == 1:
				print("Total lines of Python-Code in file: ")
			else:
				print("Total Python-Files: ", len(all_python_files))
				print("Total lines of Python-Code in folder: ", end=" ")
			print(return_sum_of_lines_in_folder(all_python_files, args))
	else:
		print(all_python_files)
	