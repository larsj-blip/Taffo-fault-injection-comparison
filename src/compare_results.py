from pathlib import Path


def read_folder_contents(folder:Path):
    files = [file for file in folder.iterdir()]
    file_contents = [file.read_text() for file in files]
    file_contents = [file_text.strip().split() for file_text in file_contents]
    file_contents_int = [ [int(file_element) for file_element in file_content_list] for file_content_list in file_contents]
    return file_contents_int

class Comparator:
    def __init__(self, control_data_path:Path, data_folder_path:Path):
        self.control_data_path = control_data_path
        self.data_folder_path = data_folder_path
        self.control_data = []
        self.results = {}

    def compare(self):
        with open(self.control_data_path) as control:
            string_data_representation = control.read().strip().split()
            self.control_data = self.cast_string_data_to_int(string_data_representation)
        for file in self.iterate_through_all_data_except_control():
            with open(file) as file_object:
                file_data = file_object.read().strip().split()
                data = self.cast_string_data_to_int(file_data)
                total_difference = 0
                for index, value in enumerate(data):
                    total_difference += abs(value - self.control_data[index])
                self.results[file.name] = total_difference

    def cast_string_data_to_int(self, string_data_representation):
        return [int(value) for value in string_data_representation]

    def iterate_through_all_data_except_control(self):
        return filter(lambda file: file.name != self.control_data_path.name, self.data_folder_path.iterdir())

    def get_results(self):
        if len(self.results) == 0:
            return Result({})
        return Result(self.results)



class Result:
    def __init__(self, data:dict):
        self.data = data

    def get_difference(self, path:Path):
        return self.data[str(path.name)]