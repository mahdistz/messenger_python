import csv


class File:
    def __init__(self, path):
        self.path = path

    def read_file(self, delimeter=','):
        data = []
        with open(self.path, "r") as file:
            for line in file:
                line = line.strip()
                temp = line.split(delimeter)  # or some other preprocessing
                data.append(temp)
        return data

    def read_file_csv(self):
        with open(self.path, 'r') as csvfile:
            rows = []
            fields = []
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row)
        return fields, rows

    def read_csvfile_as_dictionary(self):
        with open(self.path, 'r') as csvfile:
            rows = []
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                rows.append(dict(row))
            return rows

    def write(self, item_dict):
        with open(self.path, 'a', newline='') as file:
            fields = list(item_dict.keys())
            writer = csv.DictWriter(file, fieldnames=fields)

            # writing headers (field names)
            if file.tell() == 0:
                writer.writeheader()

            # writing data rows
            writer.writerow(item_dict)
            file.close()

    def delete_specific_row(self, item_list):
        with open(self.path, 'r') as inp:
            reader = csv.reader(inp)
            rows = []
            for row in reader:
                if row != item_list:
                    rows.append(row)
        with open(self.path, 'w', newline='') as out:
            writer = csv.writer(out)
            for row in rows:
                writer.writerow(row)

    def edit_file(self, prev_dic, new_dic):
        with open(self.path, 'r') as csvfile:
            rows = []
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                rows.append(dict(row))

        for i, j in enumerate(rows):
            for k, v in prev_dic.items():
                if j[k] == v:
                    for k2, v2 in new_dic.items():
                        rows[i][k2] = v2

        keys = rows[0].keys()
        with open(self.path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(rows)
