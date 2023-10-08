import os

def get_relative_directory(current_file, relative_path):
    dirname = os.path.dirname(current_file)
    return os.path.join(dirname, relative_path)