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
    video_target = os.path.join(UPLOAD_FOLDER, "**/*.mp4")
    json_target = os.path.join(UPLOAD_FOLDER, "**/*.json")

    # video list from storage
    video_path_list = glob.glob(video_target)
    json_path_list = glob.glob(json_target)
    
    src_list = [ get_src(video_path) for video_path in video_path_list ]
    title_list = []
    date_list = []
    time_list = []
    
    for json_path in json_path_list :
        with open(json_path) as json_file:
            data = json.load(json_file)
            date_list.append(data['video']['date'])
            time_list.append(data['video']['time'])
            title_list.append(data['video']['id'])
    return [title_list, src_list, date_list, time_list]
    # return [['ptsd_lecture'], ['static/storage/ptsd_lecture/ptsd_lecture.mp4'], ['2021-05-16 01:30:06.986065']]

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