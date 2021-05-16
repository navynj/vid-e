import os, glob, json
from app import UPLOAD_FOLDER

def get_path(id, path):
    return os.path.join(UPLOAD_FOLDER, id, path)

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

def get_video_list():
    vid_target_file = r"static/storage/**/*.mp4"
    json_target_file = r"static/storage/**/*.json"

    # video list from storage
    video_list = glob.glob(vid_target_file)
    json_list = glob.glob(json_target_file)
    
    vid_title_list = []
    json_time = []

    for i in video_list:
        v_title = i.split('/')
        vid_title_list.append(v_title[2])

    for j in json_list :
        with open(j) as json_file:
            json_data = json.load(json_file)
            json_time.append(json_data['video']['time'])

    return vid_title_list, video_list, json_time

# def get_file_time():
#     json_target_file = r"static/storage/**/*.json"
#     # video list from storage
#     json_list = glob.glob(json_target_file)
#     json_time = []

#     for i in json_list :
#         with open(json_list) as json_file:
#             json_data = json.load(json_file)
#             json_time.append(json_data['video']['time'])
#     return json_time