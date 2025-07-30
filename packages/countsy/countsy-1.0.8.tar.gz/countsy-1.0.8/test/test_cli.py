from unittest import TestCase
from argparse import Namespace


class Test(TestCase):
	def test_return_sum_of_lines_in_folder(self):
		from src.cli import return_sum_of_lines_in_folder, return_all_files_in_folder
		
		test_dir_path = 'test_dir/'
		test_dir = return_all_files_in_folder(test_dir_path)
		
		test_file_1 = test_dir_path + 'test_file_1.py'
		test_file_2 = test_dir_path + 'test_file_2.py'
		test_file_3 = test_dir_path + 'test_file_3.py'
		
		self.assertEqual(sorted(test_dir),
		                 ['test_dir/test_file_1.py', 'test_dir/test_file_2.py', 'test_dir/test_file_3.py'])
		
		def make_args(tqdm=False, ignore_comments=False, ignore_blank_lines=False):
			return Namespace(
				tqdm=tqdm,
				ignore_comments=ignore_comments,
				ignore_blank_lines=ignore_blank_lines,
				ignore=False,
				folder_path=None
			)
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args()), {'no_ignore': 31})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args(ignore_comments=True)), {'ignore_comments': {'code': 20, 'comments': 11}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args(ignore_blank_lines=True)), {'ignore_blanks': {'blanks': 12, 'code': 19}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args(ignore_comments=True, ignore_blank_lines=True)), {'ignore_both': {'blanks': 12, 'code': 8, 'comments': 11}})
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args()), {'no_ignore': 30})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args(ignore_comments=True)), {'ignore_comments': {'code': 25, 'comments': 5}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args(ignore_blank_lines=True)), {'ignore_blanks': {'blanks': 25, 'code': 5}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args(ignore_comments=True, ignore_blank_lines=True)), {'ignore_both': {'blanks': 25, 'code': 0, 'comments': 5}})
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args()), {'no_ignore': 9})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args(ignore_comments=True)), {'ignore_comments': {'code': 7, 'comments': 2}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args(ignore_blank_lines=True)), {'ignore_blanks': {'blanks': 1, 'code': 8}})
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args(ignore_comments=True, ignore_blank_lines=True)), {'ignore_both': {'blanks': 1, 'code': 6, 'comments': 2}})
		
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args()), {'no_ignore': 70})
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args(ignore_comments=True)), {'ignore_comments': {'code': 52, 'comments': 18}})
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args(ignore_blank_lines=True)), {'ignore_blanks': {'blanks': 38, 'code': 32}})
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args(ignore_comments=True, ignore_blank_lines=True)), {'ignore_both': {'blanks': 38, 'code': 14, 'comments': 18}})