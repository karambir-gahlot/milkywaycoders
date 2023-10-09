import os
import csv
import json

def get_relative_directory(current_file, relative_path):
    dirname = os.path.dirname(current_file)
    return os.path.join(dirname, relative_path)

def load_json_file(current_file, relative_path):
    with open(get_relative_directory(current_file, relative_path)) as f:
        return json.load(f)

def load_csv(current_file, relative_path):
    with open(get_relative_directory(current_file, relative_path)) as csvfile:
        reader = csv.DictReader(csvfile)
        return [r for r in reader]