from pathlib import Path
from unittest import TestCase

from src.compare_results import Comparator

TEST_FILE_1_PATH = Path("assets/test_folder/benchmark_bit_no_30.fixed.txt")
TEST_FILE_2_PATH = Path("assets/test_folder/benchmark_bit_no_30.float.txt")
RESULT_OUTPUT_HEADING =

TEST_FOLDER_PATH = Path("./assets/test_folder")
CONTROL_FILE_PATH = Path("assets/test_folder/benchmark.float.txt")
FIXED_POINT_NO_FAULT_INJECTED_PATH = Path("assets/test_folder/benchmark.fixed.txt")

class Test(TestCase):

    def test_should_calculate_average_difference_between_control_and_fault_injected_files_for_a_single_benchmark(self):
        results = self.calculate_test_results()
        file_2_diff = abs(float(TEST_FILE_2_PATH.read_text()) - float(CONTROL_FILE_PATH.read_text()))
        file_1_diff = abs(float(TEST_FILE_1_PATH.read_text()) - float(CONTROL_FILE_PATH.read_text()))
        self.assertEqual(file_2_diff, results.get_difference_from_control(TEST_FILE_2_PATH))
        self.assertEqual(file_1_diff, results.get_difference_from_control(TEST_FILE_1_PATH))

    def test_should_print_results_with_file_names_in_first_column_in_all_rows_except_heading(self):
        result = self.calculate_test_results()
        results_string_representation = result.to_string()
        results_string_representation_lines = results_string_representation.split("\n")
        expected_file_names =[path.name for path in TEST_FOLDER_PATH.glob("*.txt")]
        # ignore header row
        actual_file_names = []
        heading = results_string_representation_lines[1]
        for line in results_string_representation_lines[1:]:
            if len(line)>0:
                filename = line.split()[0]
                actual_file_names.append(filename)
        self.assertListEqual(expected_file_names, actual_file_names)
        self.assertEqual(heading, RESULT_OUTPUT_HEADING)

    # no time to implement :(
    def test_should_not_accept_filenames_in_the_wrong_format(self):
        pass

    def test_should_compare_float_and_fixed_results_for_the_same_injected_bit(self):
        results = self.calculate_test_results()
        actual_alternative_implementation_results = results.get_alternative_implementation_results(TEST_FILE_1_PATH)
        expected_alternative_implementation_results = results.get_difference_from_control(TEST_FILE_2_PATH)
        self.assertEqual(actual_alternative_implementation_results, expected_alternative_implementation_results)
        actual_alternative_implementation_results = results.get_alternative_implementation_results(CONTROL_FILE_PATH)
        expected_alternative_implementation_results = results.get_difference_from_control(FIXED_POINT_NO_FAULT_INJECTED_PATH)
        self.assertEqual(actual_alternative_implementation_results, expected_alternative_implementation_results)

    def calculate_test_results(self):
        comparator = Comparator(control_data_path=CONTROL_FILE_PATH, data_folder_path=TEST_FOLDER_PATH)
        comparator.compare()
        result = comparator.get_results()
        return result

