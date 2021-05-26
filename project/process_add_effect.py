import os
import ffmpeg
import pandas as pd
import json
import numpy as np
from app import UPLOAD_FOLDER, EFFECT_FOLDER
from file_path import get_src

effect_data = {
    "short" : {
        "뿅" : [
            {
                "name" : "뿅 01",
                "src" : "짧은_뿅_01.mp3",
                "index" : 0
            },
            {
                "name" : "뿅 02",
                "src" : "짧은_뿅_02.mp3",
                "index" : 1
            }
        ],
        "띵" : [
            {
                "name" : "띵01",
                "src" : "짧은_띵_01.mp3",
                "index" : 2
            },
            {
                "name" : "띵02",
                "src" : "짧은_띵_02.mp3",
                "index" : 3
            }
        ],
        "휙" : [
            {
                "name" : "휙01",
                "src" : "짧은_휙_01.mp3",
                "index" : 4
            },
            {
                "name" : "휙02",
                "src" : "짧은_휙_02.mp3",
                "index" : 5
            }
        ],
        "별가루" : [
            {
                "name" : "별가루 01",
                "src" : "짧은_별가루_01.mp3",
                "index" : 6
            },
            {
                "name" : "별가루 02",
                "src" : "짧은_별가루_02.mp3",
                "index" : 7
            }
        ]
    },
    
    "long" : {
        "뾰롱" : [
            {
                "name" : "뾰롱 01",
                "src" : "긴_뾰롱_01.mp3",
                "index" : 8
            },
            {
                "name" : "뾰롱 02",
                "src" : "긴_뾰롱_02.mp3",
                "index" : 9
            }
        ],
        "띠링" : [
            {
                "name" : "띠링01",
                "src" : "긴_띠링_01.mp3",
                "index" : 10
            },
            {
                "name" : "띠링02",
                "src" : "긴_띠링_02.mp3",
                "index" : 11
            }
        ],
        "휘익" : [
            {
                "name" : "휘익01",
                "src" : "긴_휙_01.mp3",
                "index" : 12
            },
            {
                "name" : "휘익02",
                "src" : "긴_휙_02.mp3",
                "index" : 13
            }
        ],
        "별가루" : [
            {
                "name" : "별가루 01",
                "src" : "긴_별가루_01.mp3",
                "index" : 14
            },
            {
                "name" : "별가루 02",
                "src" : "긴_별가루_02.mp3",
                "index" : 15
            }
        ]
    }
}

def get_effect_src():
    effect_src = []
    for category in effect_data.values():
        for effect_list in category.values():
            for effect in effect_list:
                effect_src.append(effect['src'])
    return effect_src

def get_effect_list():
    long_effect_file, short_effect_file = long_effect, short_effect
    return long_effect, short_effect

def effect_export(id, effect_list, time_list):
    input_path = os.path.join(UPLOAD_FOLDER, id, f"{id}.mp4")
    output_path = os.path.join(UPLOAD_FOLDER, id, f"output_{id}.mp4")
    
    time = time_list
    effect = effect_list
    print(effect)
    
    input_video = ffmpeg.input(input_path)
    added_audio = input_video.audio

    for i in range(len(time)):
        print(effect[i])
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
                'src' : get_src(output_path)
        }