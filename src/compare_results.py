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

    @staticmethod
    def cast_string_data_to_float(string_data_representation):
        return [float(value) for value in string_data_representation]

    def get_results(self):
        if len(self.results) == 0:
            return Result({})
        return Result(self.results)



class Result:

    OUTPUT_COLUMN_HEADERS = ["Filename", "Average Difference From Control"]
    FORMATTABLE_STRING = '{0}\t{1}\n'

    def __init__(self, data:dict):
        self.data = data
        self.longest_filename = max([len(key) for key in self.data.keys()] + [len(self.OUTPUT_COLUMN_HEADERS[0])])
        self.longest_result_string = max([len(result) for result in self.data.items()] + [len(self.OUTPUT_COLUMN_HEADERS[1])])

    def get_alternative_implementation_results(self, path:Path):
        input_filename = path.name
        # implicitly requiring the format of the files to be benchmark_bit_no_30[.fixed|.float| ].txt
        # should ideally be in the tests
        input_injected_bit =  self.get_injected_bit_from_filename(input_filename)
        for key in self.data:
            injected_bit = self.get_injected_bit_from_filename(key)
            if injected_bit == input_injected_bit and input_filename != key:
                return self.data[key]
        return "no data found"

    @staticmethod
    def get_injected_bit_from_filename(filename):
        split_on_underscore = filename.split("_")
        if len(split_on_underscore) == 1:
            #implied that if there is no underscore = no fault injected
            return None
        split_on_period = split_on_underscore[3].split(".")
        return split_on_period[0]

    def get_difference_from_control(self, path:Path):
        return self.data[str(path.name)]

    def to_string(self):
        output_string = self.get_output_string_heading()
        for filename, difference in self.data.items():
            formatted_string = self.FORMATTABLE_STRING.format(filename.ljust(self.longest_filename), str(difference).ljust(self.longest_result_string))
            output_string += formatted_string
        return output_string

    def get_output_string_heading(self):
        return self.FORMATTABLE_STRING.format(self.OUTPUT_COLUMN_HEADERS[0].ljust(self.longest_filename),
                                              self.OUTPUT_COLUMN_HEADERS[1].ljust(self.longest_result_string))


if __name__ == '__main__':
    if sys.argv[1] == '-h' or sys.argv[1] == '--help' or sys.argv[1] == '':
        print('Usage: compare_results <control_data_file_path> <data_folder_path>')
    else:
        comparator = Comparator(Path(sys.argv[1]), Path(sys.argv[2]))
        comparator.compare()
        print(comparator.get_results().to_string())
