import csv
import os
import logging


class FileHandler:
    def __init__(self, file_path='csv_file'):
        self.file_path = file_path

    def read_file(self):

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as my_file:
                reader = csv.DictReader(my_file)
                return list(reader)
        else:
            return "path is incorrect"

    def write_file(self, info, mode="a"):

        if isinstance(info, dict):

            if self.check_unique_id(info["id"]):
                return "id already exists"
            fieldnames = info.keys()
            info = [info]

        elif isinstance(info, list):
            fieldnames = info[0].keys()

        with open(self.file_path, mode) as my_file:
            writer = csv.DictWriter(my_file, fieldnames=fieldnames)
            if my_file.tell() == 0:
                writer.writeheader()
            writer.writerows(info)

    def edit_row(self, new_info):

        all_rows = self.read_file()
        final_rows = []

        for row in all_rows:
            if row["id"] == str(new_info["id"]):
                row = new_info
            final_rows.append(row)
        self.write_file(final_rows, mode="w")

    def check_unique_id(self, id):

        all_rows = self.read_file()
        for row in all_rows:
            if row["id"] == str(id):
                return True
        return False

    def delete_row(self, id):
        all_rows = self.read_file()
        final_rows = []
        for row in all_rows:
            if row["id"] == str(id):
                continue
            final_rows.append(row)
        self.write_file(final_rows, mode="w")
