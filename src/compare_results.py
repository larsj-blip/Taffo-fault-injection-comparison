#!/usr/bin/env python3

import sys
from pathlib import Path

class Comparator:
    def __init__(self, control_data_path:Path, data_folder_path:Path):
        self.control_data_path = control_data_path
        self.data_folder_path = data_folder_path
        self.control_data = []
        self.results = {}

    def compare(self):
        with open(self.control_data_path) as control:
            string_data_representation = control.read().strip().split()
            self.control_data = self.cast_string_data_to_float(string_data_representation)
        for file in self.data_folder_path.iterdir():
            with open(file) as file_object:
                file_data = file_object.read().strip().split()
                data = self.cast_string_data_to_float(file_data)
                total_difference = 0
                for index, value in enumerate(data):
                    total_difference += abs(value - self.control_data[index])
                self.results[file.name] = total_difference / len(data)

    def cast_string_data_to_float(self, string_data_representation):
        return [float(value) for value in string_data_representation]

    def get_results(self):
        if len(self.results) == 0:
            return Result({})
        return Result(self.results)



class Result:
    def __init__(self, data:dict):
        self.data = data

    def get_difference(self, path:Path):
        return self.data[str(path.name)]

    def to_string(self):
        table_heading = ["Filename" , "Difference"]
        row_header_lengths = [len(key) for key in self.data.keys()] + [len(table_heading[0])]
        longest_filename = max(row_header_lengths)
        longest_result_string = max([len(result) for result in self.data.items()] + [len(table_heading[1])])
        formattable_string = '{0}\t{1}\n'
        output_string = formattable_string.format(table_heading[0], table_heading[1])
        for filename, difference in self.data.items():
            formatted_filename = filename.rjust(longest_filename)
            formatted_string = formattable_string.format(formatted_filename, difference)
            output_string += formatted_string
        return output_string


if __name__ == '__main__':
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: compare_results <control_data_file_path> <data_folder_path>')
    else:
        comparator = Comparator(Path(sys.argv[1]), Path(sys.argv[2]))
        comparator.compare()
        print(comparator.get_results().to_string())
