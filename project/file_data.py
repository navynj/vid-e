import json, os, glob, shutil
from file_path import get_path, get_file_path

# save & load data
def save_data(id, data):
    data_path = get_file_path(f"{id}.json")
    with open(data_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def load_data(id):
    data_path = get_file_path(f"{id}.json")
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

# load data list
def load_data_list(key):
    data_list = []
    target = get_path("**", "*.json")
    path_list = glob.glob(target)
    for path in path_list :
        with open(path) as json_file:
            data = json.load(json_file)
            data_list.append(data[key])
    return data_list

# save & load to temp dir (dir named video id)
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