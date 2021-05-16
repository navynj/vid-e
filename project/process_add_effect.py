import os
import ffmpeg
import pandas as pd
import json
import numpy as np
from app import UPLOAD_FOLDER

long_effect = [['긴_띠링_01.mp3', '긴_띠링_02.mp3'], # 휙
                ['긴_별가루_01.mp3', '긴_별가루_02.mp3'], # 띵
                ['긴_뾰롱_01.mp3', '긴_뾰롱_02.mp3'], # 뾱
                ['긴_휙_01.mp3', '긴_휙_02.mp3'] # 별가루~
                ]
short_effect = [['짧은_띵_01.mp3', '짧은_띵_02.mp3'], # 휙
                ['짧은_별가루_01.mp3', '짧은_별가루_02.mp3'], # 띵
                ['짧은_뿅_01.mp3', '짧은_뿅_02.mp3'], # 뾱
                ['짧은_휙_01.mp3', '짧은_휙_02.mp3'] # 별가루~
                ]

def get_effect_list():
    long_effect_file, short_effect_file = long_effect, short_effect
    return long_effect, short_effect

def export(video_name, data):
    n_list, e_list = data
    num = len(n_list)
    
    input_video = ffmpeg.input(os.path.join(UPLOAD_FOLDER, video_name))
    added_audio = input_video.audio

    for j in range(num):
        a = ffmpeg.input(os.path.join(UPLOAD_FOLDER, e_list[j]).audio.filter('adelay', f"{n_list[j]}|{n_list[j]}"))
        added_audio = ffmpeg.filter([added_audio, a], 'amix')

    (
        ffmpeg
        .concat(input_video, added_audio, v=1, a=1)
        .output(os.path.join(UPLOAD_FOLDER, video_name))
        .run(overwrite_output=True)
    )
    return os.path.join(UPLOAD_FOLDER, video_name)