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
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args()), 31)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args(ignore_comments=True)), 20)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_1], make_args(ignore_blank_lines=True)), 19)
		self.assertEqual(
			return_sum_of_lines_in_folder([test_file_1], make_args(ignore_comments=True, ignore_blank_lines=True)), 8)
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args()), 30)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args(ignore_comments=True)), 25)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_2], make_args(ignore_blank_lines=True)), 5)
		self.assertEqual(
			return_sum_of_lines_in_folder([test_file_2], make_args(ignore_comments=True, ignore_blank_lines=True)), 0)
		
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args()), 9)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args(ignore_comments=True)), 7)
		self.assertEqual(return_sum_of_lines_in_folder([test_file_3], make_args(ignore_blank_lines=True)), 8)
		self.assertEqual(
			return_sum_of_lines_in_folder([test_file_3], make_args(ignore_comments=True, ignore_blank_lines=True)), 6)
		
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args()), 70)
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args(ignore_comments=True)), 52)
		self.assertEqual(return_sum_of_lines_in_folder(test_dir, make_args(ignore_blank_lines=True)), 32)
		self.assertEqual(
			return_sum_of_lines_in_folder(test_dir, make_args(ignore_comments=True, ignore_blank_lines=True)), 14)