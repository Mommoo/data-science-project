import os

class FileHandler:
    def __init__(self, dir_path, file_name) -> None:
        self.__dir_path = dir_path
        self.__file_path = dir_path + "\\" + file_name
        self.__file = None

    def create_file_if_absent(self) -> None:

        def create_file():
            self.file_open()
            self.__file.close()

        if os.path.isdir(self.__dir_path) is False:
            os.makedirs(self.__dir_path)
            create_file()

        elif os.path.isfile(self.__file_path) is False:
            create_file()

    def file_open(self) -> None:
        self.__file = open(self.__file_path, "w+", encoding='UTF8')

    def is_open(self) -> bool:
        if self.__file is None:
            return False

        return self.__file.closed is False

    def file_close(self)-> None:
        if self.__file.closed is False:
            self.__file.close()

    def write(self, string) -> None:
        self.__file.writelines(string)
        # self.__file.flush()

    def write_new_line(self, string) -> None:
        self.write("\n" + string)

    def write_first_line(self, string: str, over_wrapping=False) -> None:
        self.__file.seek(0)
        if over_wrapping is False:
            contents = self.__file.readlines()
            contents.insert(0, string)
            string = "".join(contents)
            self.__file.seek(0)
        self.write(string)
        self.__file.seek(0, 2)  # go to end line


class CSVFileRepository:
    def __init__(self, dir_path, file_name) -> None:
        self.__file_handler = FileHandler(dir_path, file_name)
        self.__file_handler.create_file_if_absent()

    def open(self):
        if self.__file_handler.is_open() is False:
            self.__file_handler.file_open()

    def close(self):
        if self.__file_handler.is_open():
            self.__file_handler.file_close()

    def set_column(self, column_list: list) -> None:
        self.__file_handler.write_first_line(",".join(column_list))

    def add_row_list(self, row_data_list: list) -> None:
        for row_data in row_data_list:
            self.add_row(row_data)

    def add_row(self, row_data: list) -> None:
        flat_list = []

        for item in row_data:
            flat_list.append(CSVFileRepository.__convert_flat_string_data(item))

        self.__file_handler.write_new_line(",".join(flat_list))

    @classmethod
    def __convert_flat_string_data(cls, item) -> str:

        def wrapping_data(data: str) -> str:
            return '"' + str(data) + '"'

        if type(item) is list:
            return wrapping_data(','.join(item))

        elif type(item) is dict:
            dict_list = []
            for key in item.keys():
                dict_list.append("%s(%s)" % (str(key), str(item[key])))

            return wrapping_data(','.join(dict_list))

        else:
            return wrapping_data(item)