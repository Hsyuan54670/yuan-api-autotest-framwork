import csv
import yaml

def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # collect non-empty rows (skip fully empty lines)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
        # if there's a header, drop the first row
        if rows:
            rows = rows[1:]
        # convert numeric-looking cells to int, leave others as stripped strings
        for r_index, row in enumerate(rows):
            for i in range(len(row)):
                cell = row[i].strip()
                try:
                    rows[r_index][i] = int(cell)
                except ValueError:
                    rows[r_index][i] = cell
        return rows

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        s = f.read()
        data = yaml.safe_load(s)
        return data

def read_yaml_list(file_path):
    return list(read_yaml(file_path).values())

def extract_yaml(key,value):
    with open("config/extract.yaml", 'a+', encoding='utf-8') as f:
        data = {key:value}
        yaml.dump(data,f,allow_unicode=True)

def clear_extract_yaml():
    with open("config/extract.yaml", 'w', encoding='utf-8') as f:
        f.write("")