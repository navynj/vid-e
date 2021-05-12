import json, os, shutil
from file_path import get_path, get_file_path

# data save & load
def save_data(id, data):
    data_path = get_file_path(f"{id}.json")
    with open(data_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def load_data(id):
    data_path = get_file_path(f"{id}.json")
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def save_temp(root, dirname, file_name, data):
    data_path = get_path(root, os.path.join(dirname, file_name))
    with open(data_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def load_temp(root, dir_name, file_name):
    data_path = get_path(root, os.path.join(dir_name, file_name))
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def temp_exists(root, dir_name, file_name):
    data_path = get_path(root, os.path.join(dir_name, file_name))
    return os.path.isfile(data_path)

def remove_temp(root, dir_name):
    dir_path = get_path(root, dir_name)
    shutil.rmtree(dir_path)