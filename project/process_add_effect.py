import os
import ffmpeg
import pandas as pd
import json
import numpy as np
from app import UPLOAD_FOLDER, EFFECT_FOLDER
from file_path import get_src

effect_data = {

    "뾱" : [
        {
            "name" : "짧은 뾱",
            "src" : "짧은_뾱.mp3",
            "index" : 0
        },
        {
            "name" : "물방울 뾱",
            "src" : "물방울_뾱.mp3",
            "index" : 1
        },
        {
            "name" : "우아한 뾰롱",
            "src" : "우아한_뾰롱.mp3",
            "index" : 2
        },
        {
            "name" : "딩동댕 뾰롱",
            "src" : "딩동댕_뾰롱.mp3",
            "index" : 3
        }
    ],

    "띵" : [
        {
            "name" : "터지는 띵",
            "src" : "터지는_띵.mp3",
            "index" : 4
        },
        {
            "name" : "딱딱한 띵",
            "src" : "딱딱한_띵.mp3",
            "index" : 5
        },
        {
            "name" : "밝은 띠링",
            "src" : "밝은_띠링.mp3",
            "index" : 6
        },
        {
            "name" : "게임용 띠링",
            "src" : "게임용_띠링.mp3",
            "index" : 7
        }
    ],

    "휙" : [
        {
            "name" : "휘익",
            "src" : "휘익.mp3",
            "index" : 8
        },
        {
            "name" : "홱",
            "src" : "홱.mp3",
            "index" : 9
        },
        {
            "name" : "후욱",
            "src" : "후욱.mp3",
            "index" : 10
        },
        {
            "name" : "후웅",
            "src" : "후웅.mp3",
            "index" : 11
        }
    ],

    "샤라랑" : [
        {
            "name" : "등장 샤라랑",
            "src" : "등장_샤라랑.mp3",
            "index" : 12
        },
        {
            "name" : "짧은 샤랑",
            "src" : "짧은_샤랑.mp3",
            "index" : 13
        },
        {
            "name" : "도레미파 샤랑",
            "src" : "도레미파_샤랑.mp3",
            "index" : 14
        },
        {
            "name" : "도시라솔 샤랑",
            "src" : "도시라솔_샤랑.mp3",
            "index" : 15
        }
    ]
}

def get_effect_src():
    effect_src = []
    # for category in effect_data.values():
    #     print("================")
    #     print(category)
    for effect_list in effect_data.values():
        # print(effect_list)
        for effect in effect_list:
            effect_src.append(effect['src'])
    return effect_src

def get_effect_list():
    long_effect_file, short_effect_file = long_effect, short_effect
    return long_effect, short_effect

def effect_export(id, video_name, effect_list, time_list):
    input_path = os.path.join(UPLOAD_FOLDER, id, video_name)
    output_path = os.path.join(UPLOAD_FOLDER, id, f"output_{id}.mp4")
    
    time = time_list
    effect = effect_list
    # print(effect)
    
    input_video = ffmpeg.input(input_path)
    added_audio = input_video.audio

    for i in range(len(time)):
        # print(effect[i])
        a = ffmpeg.input(os.path.join(EFFECT_FOLDER, effect[i])).audio.filter('adelay', f"{time[i]}|{time[i]}")
        added_audio = ffmpeg.filter([added_audio, a], 'amix')

    (
        ffmpeg
        .concat(input_video, added_audio, v=1, a=1)
        .output(output_path)
        .run(overwrite_output=True)
    )
    
    return {
                'status' : 'COMPLETE',
                'src' : get_src(output_path),
                'msg' : 'exporting...'
        }