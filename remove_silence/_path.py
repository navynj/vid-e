from data import get_path

# data save & load
def save_data(id, data):
    data_path = get_path(f"{id}.json")
    with open(data_path, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return True

def load_data(id):
    data_path = get_path(f"{id}.json")
    with open(data_path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data