#! /usr/bin/env python3

from pydub import AudioSegment
from pydub import effects

from random import randint
from xml.etree import ElementTree

import sys
import os
import shutil
import requests
import subprocess

def speedup_song(path):
    sound = AudioSegment.from_file(path)
    
    octaves = 4/12 # x1.25
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    nightcore = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)

    nightcore.export("tmp/nightcore.mp3", format="mp3", bitrate="192k")

def get_request_url(page):
    tags = ['vocaloid', 'looking_at_another', '1girl', '1girl+1boy']

    return "https://safebooru.org/index.php?page=dapi&s=post&q=index&pid=" + str(page) + "&tags=width:1920+height:1080+-swimsuit+-feet+-text+score:>=1+" + tags[randint(0, len(tags) - 1)]

def get_random_image():
    total_results = int(ElementTree.fromstring(requests.get(get_request_url(1)).content).get('count'))
    if total_results % 100 == 0:
        total_results -= 1
    page = randint(0, total_results // 100)

    r = requests.get(get_request_url(page))
    image_list = list(ElementTree.fromstring(r.content))
    image_url = image_list[randint(0, len(image_list) - 1)].get('file_url')
    img_data = requests.get(image_url).content

    with open('tmp/image.jpg', 'wb') as handler:
        handler.write(img_data)

def render_video():
    cmd = 'ffmpeg -loop 1 -i tmp/image.jpg -i tmp/nightcore.mp3 -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest nightcore.mp4'
    subprocess.call(cmd, shell=True)

def main(path):
    if (os.path.isdir('tmp')):
        shutil.rmtree('tmp')
    os.mkdir('tmp')

    speedup_song(path)
    get_random_image()
    render_video()

    shutil.rmtree('tmp')
    print('Nightcore video successfully generated! You should be ashamed of yourself.')


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: nightcore.py [path to music file]", file=sys.stderr)
    else:
        main(sys.argv[1])