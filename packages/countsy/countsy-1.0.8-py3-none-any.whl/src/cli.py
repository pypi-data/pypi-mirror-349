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


def return_lines_of_uncommented_code(file: list) -> [int, int]:
	ctr_code = 0
	ctr_comments = 0
	
	multiline_comment_flag = False
	
	for el in file:
		stripped = el.strip()
		if stripped.startswith('#'):
			ctr_comments += 1
			continue
		if stripped.startswith("\"\"\"") or (multiline_comment_flag and stripped.endswith("\"\"\"")):
			ctr_comments += 1
			multiline_comment_flag = not multiline_comment_flag
			continue
		if multiline_comment_flag:
			ctr_comments += 1
			continue
		ctr_code += 1
	return {"code": ctr_code, "comments": ctr_comments}


def return_lines_of_non_blank_code(file: list) -> [int, int]:
	ctr_code = 0
	ctr_blanks = 0
	
	for el in file:
		stripped = el.strip()
		if stripped != "":
			ctr_code += 1
		else:
			ctr_blanks += 1
			
	return {"code": ctr_code, "blanks": ctr_blanks}
	

def return_lines_of_non_blank_uncommented_code(file: list) -> [int, int, int]:
	ctr_code = 0
	ctr_blanks = 0
	ctr_comments = 0
	
	multiline_comment_flag = False
	for el in file:
		stripped = el.strip()
		if stripped.startswith('#'):
			ctr_comments += 1
			continue
			
		# Check for multiline comment start/end
		if stripped.startswith('"""') or (multiline_comment_flag and stripped.endswith('"""')):
			ctr_comments += 1
			multiline_comment_flag = not multiline_comment_flag
			continue
		# Skip if inside multiline comment
		if multiline_comment_flag:
			ctr_comments += 1
			continue
		# Check if line is non-blank
		if stripped != "":
			ctr_code += 1
		else:
			ctr_blanks += 1
			
	return {"code": ctr_code, "blanks": ctr_blanks, "comments": ctr_comments}
	

def return_lines_of_code(filename: str, args) -> dict:
	"""
	Returns the line length of a given file. Does not ignore blank lines or comments.
	:param filename:
	:param args: arg parser arguments
	:return: file_length:
	"""
	ignore_blank_lines = args.ignore_blank_lines
	ignore_comments = args.ignore_comments
	try:
		with open(filename) as f:
				file = f.read().split('\n')
				if not ignore_blank_lines and not ignore_comments:
					return {"no_ignore": len(file)}
				elif ignore_blank_lines and not ignore_comments:
					return {"ignore_blanks": return_lines_of_non_blank_code(file)}
				elif not ignore_blank_lines and ignore_comments:
					return {"ignore_comments": return_lines_of_uncommented_code(file)}
				elif ignore_blank_lines and ignore_comments:
					return {"ignore_both": return_lines_of_non_blank_uncommented_code(file)}
			
	except Exception as e:
		return {"error": e}


def sum_per_keyword(raw_output, args):
	key, value = next(iter(raw_output.items()))
	if key == "error":
		return raw_output


def return_sum_of_lines_in_folder(list_of_files, args):
	"""
	Returns the sum of all single lengths of code with proper error handling
	:param list_of_files: List of file paths to process
	:param args: arg parser arguments
	:return: Dictionary with totals and any errors encountered
	"""
	use_tqdm = args.tqdm
	ignore_blank_lines = args.ignore_blank_lines
	ignore_comments = args.ignore_comments
	
	# Initialize totals
	total_code = 0
	total_comments = 0
	total_blanks = 0
	total_lines = 0
	errors = []
	
	# Handle single file case
	if len(list_of_files) == 1:
		result = return_lines_of_code(list_of_files[0], args)
		if "error" in result:
			return {"error": result["error"]}
		return result
	
	# Process multiple files
	iterator = tqdm(list_of_files) if use_tqdm else list_of_files
	
	result = None
	
	for file_path in iterator:
		file_result = return_lines_of_code(file_path, args)
		
		# Handle errors
		if "error" in file_result:
			errors.append(f"Error in {file_path}: {file_result['error']}")
			continue
		
		# Aggregate results based on what was counted
		if "no_ignore" in file_result:
			total_lines += file_result["no_ignore"]
		
		elif "ignore_blanks" in file_result:
			data = file_result["ignore_blanks"]
			total_code += data["code"]
			total_blanks += data["blanks"]
		
		elif "ignore_comments" in file_result:
			data = file_result["ignore_comments"]
			total_code += data["code"]
			total_comments += data["comments"]
		
		elif "ignore_both" in file_result:
			data = file_result["ignore_both"]
			total_code += data["code"]
			total_comments += data["comments"]
			total_blanks += data["blanks"]
	
	if not ignore_blank_lines and not ignore_comments:
		result = {"no_ignore": total_lines}
	elif ignore_blank_lines and not ignore_comments:
		result = {"ignore_blanks": {"code": total_code, "blanks": total_blanks}}
	elif not ignore_blank_lines and ignore_comments:
		result = {"ignore_comments": {"code": total_code, "comments": total_comments}}
	elif ignore_blank_lines and ignore_comments:
		result = {"ignore_both": {"code": total_code, "comments": total_comments, "blanks": total_blanks}}
	
	if errors:
		result = {"errors": errors}
	
	# TODO: Find out what error this could be
	if result is None:
		print("Unknown error occurred")
		sys.exit(1)
		
	return result


def format_output(raw_output, all_python_files, args):
	"""
	Format and print the output results
	:param raw_output: Results from return_sum_of_lines_in_folder
	:param all_python_files: List of all Python files processed
	"""
	# Handle errors first
	if "errors" in raw_output:
		print("Errors encountered:")
		for error in raw_output["errors"]:
			print(f"  - {error}")
		print()  # Add blank line
	
	# Handle main results
	key = next(k for k in raw_output.keys() if k != "errors")
	value = raw_output[key]
	
	if len(all_python_files) == 1:
		print("  Total lines of Python-Code in file: ", all_python_files[0], ":\n")
		if key == "no_ignore":
			print(f"  Total lines: {value}")
		elif key == "ignore_blanks":
			print(f"  Code lines: {value['code']}")
			print(f"  Blank lines: {value['blanks']}")
			print(f"  Total lines in file: {value['code'] + value['blanks']}")
		elif key == "ignore_comments":
			print(f"  Code lines: {value['code']}")
			print(f"  Comment lines: {value['comments']}")
			print(f"  Total lines in file: {value['code'] + value['comments']}")
		elif key == "ignore_both":
			print(f"  Code lines: {value['code']}")
			print(f"  Comment lines: {value['comments']}")
			print(f"  Blank lines: {value['blanks']}")
			print(f"  Total lines in file: {value['code'] + value['comments'] + value['blanks']}")
	else:
		if args.folder_path == "./":
			print("  Total Python-Files in current directory: ", end="")
		else:
			print("  Total lines of Python-Code in folder: ", args.folder_path, ": ", end=" ")
		print(len(all_python_files))
		
		if key == "no_ignore":
			print("  Total lines in folder: ", value)
			
		elif key == "ignore_blanks":
			total_lines = value['code'] + value['blanks']
			print(f"  Total lines of Python-Code in folder: {value['code']}")
			print(f"  Total blank lines in Python-Files in folder: {value['blanks']}")
			print(f"  Total lines in folder: {total_lines}")
		elif key == "ignore_comments":
			total_lines = value['code'] + value['comments']
			print(f"  Total lines of Python-Code in folder: {value['code']}")
			print(f"  Total comments in Python-Files in folder: {value['comments']}")
			print(f"  Total lines in folder: {total_lines}")
		elif key == "ignore_both":
			total_lines = value['code'] + value['blanks'] + value['comments']
			print(f"  Total lines of Python-Code in folder: {value['code']}")
			print(f"  Total blank lines in Python-Files in folder: {value['blanks']}")
			print(f"  Total comments in Python-Files in folder: {value['comments']}")
			print(f"  Total lines in folder: {total_lines}")
			
		
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
			sys.exit(1)
		raw_output = return_sum_of_lines_in_folder(all_python_files, args)
		
		format_output(raw_output, all_python_files, args)
		
	else:
		print(all_python_files)
	