import os, json
from app import UPLOAD_FOLDER

def get_path(*args):
    return os.path.join(UPLOAD_FOLDER, *args)

def get_file_path(file_name, dir_exits=True):
    """ path for save & load """
    id = file_name.split('.')[0]
    path = get_path(id, file_name)
    if not dir_exits:
        os.makedirs(os.path.dirname(path), exist_ok=True) # 파일 경로에 폴더 없을 경우 만들기 (비디오 id 폴더 신규 생성 고려)
    return path

def get_src(absolute_path, root="storage"):
    """ src for html tag """
    path_list = absolute_path.split(os.path.sep)
    i = path_list.index(root)
    return '/'.join(path_list[i:])