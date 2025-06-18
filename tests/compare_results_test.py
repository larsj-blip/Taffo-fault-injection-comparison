from pathlib import Path
from unittest import TestCase

from src.compare_results import read_folder_contents, Comparator

TEST_FILE_2_CONTENT_LIST = [200]
TEST_FILE_1_CONTENT_LIST = [100]
TEST_FILE_1_PATH= Path("./assets/test_folder/testfile1.txt")
TEST_FILE_2_PATH= Path("./assets/test_folder/testfile2.txt")
TEST_FOLDER_FILE_CONTENT = [TEST_FILE_1_CONTENT_LIST, TEST_FILE_2_CONTENT_LIST]

TEST_FOLDER_PATH= Path("./assets/test_folder")
CONTROL_FILE_PATH = Path("./assets/test_folder/control.txt")

class Test(TestCase):

    def test_should_read_file_contents_into_multiple_lists(self):
        folder_contents = read_folder_contents(TEST_FOLDER_PATH)
        self.assertIn(TEST_FILE_1_CONTENT_LIST, folder_contents)
        self.assertIn(TEST_FILE_2_CONTENT_LIST, folder_contents)

    def test_should_calculate_average_difference_between_control_and_fault_injected_files(self):
        comparator = Comparator(control_data_path=CONTROL_FILE_PATH, data_folder_path=TEST_FOLDER_PATH)
        comparator.compare()
        results = comparator.get_results()
        self.assertEqual(100, results.get_difference(TEST_FILE_2_PATH))
        self.assertEqual(0, results.get_difference(TEST_FILE_1_PATH))