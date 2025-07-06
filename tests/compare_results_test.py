from pathlib import Path
from unittest import TestCase

from src.compare_results import Comparator

TEST_FILE_1_PATH = Path("./assets/test_folder/testfile1.txt")
TEST_FILE_2_PATH = Path("./assets/test_folder/testfile2.txt")

TEST_FOLDER_PATH = Path("./assets/test_folder")
CONTROL_FILE_PATH = Path("./assets/test_folder/control.txt")


class Test(TestCase):

    def test_should_calculate_average_difference_between_control_and_fault_injected_files(self):
        results = self.calculate_test_results()
        file_2_diff = abs(float(TEST_FILE_2_PATH.read_text()) - float(CONTROL_FILE_PATH.read_text()))
        file_1_diff = abs(float(TEST_FILE_1_PATH.read_text()) - float(CONTROL_FILE_PATH.read_text()))
        self.assertEqual(file_2_diff, results.get_difference(TEST_FILE_2_PATH))
        self.assertEqual(file_1_diff, results.get_difference(TEST_FILE_1_PATH))

    def test_should_print_results_with_file_names_in_first_column_in_all_rows_except_heading(self):
        result = self.calculate_test_results()
        results_string_representation = result.to_string()
        results_string_representation_lines = results_string_representation.split("\n")
        expected_file_names =[path.name for path in TEST_FOLDER_PATH.glob("*.txt")]
        # ignore header row
        actual_file_names = []
        for line in results_string_representation_lines[1:]:
            if len(line)>0:
                filename = line.split()[0]
                actual_file_names.append(filename)
        self.assertListEqual(expected_file_names, actual_file_names)

    def calculate_test_results(self):
        comparator = Comparator(control_data_path=CONTROL_FILE_PATH, data_folder_path=TEST_FOLDER_PATH)
        comparator.compare()
        result = comparator.get_results()
        return result

