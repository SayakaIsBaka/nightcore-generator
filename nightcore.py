#! /usr/bin/env python3

from pydub import AudioSegment
from pydub import effects

from random import randint, choice
from xml.etree import ElementTree

import sys
import os
import shutil
import requests
import subprocess
import argparse
import youtube_dl

def speedup_song(path):
    sound = AudioSegment.from_file(path)
    
    octaves = 4/12 # x1.25
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    nightcore = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)

    nightcore.export("tmp/nightcore.mp3", format="mp3", bitrate="192k")

def get_request_url(page, tag):
    return "https://safebooru.org/index.php?page=dapi&s=post&q=index&pid=" + str(page) + "&tags=width:1920+height:1080+-swimsuit+-feet+-text+score:>=1+" + tag

def get_random_image():
    tags = ['looking_at_another', '1girl', 'vocaloid', '1girl+1boy']
    tag = choice(tags)

    total_results = int(ElementTree.fromstring(requests.get(get_request_url(1, tag)).content).get('count'))
    if total_results == 0:
        print("No images found... Retry by relaunching the script", file=sys.stderr)
        exit(1)
    elif total_results % 100 == 0:
        total_results -= 1
    page = randint(0, total_results // 100)

    r = requests.get(get_request_url(page, tag))
    image_list = list(ElementTree.fromstring(r.content))
    image_url = choice(image_list).get('file_url')
    img_data = requests.get(image_url).content

    with open('tmp/image.jpg', 'wb') as handler:
        handler.write(img_data)

def render_video(path):
    cmd = 'ffmpeg -loop 1 -i tmp/image.jpg -i tmp/nightcore.mp3 -c:v libx264 -tune stillimage -c:a copy -pix_fmt yuv420p -shortest ' + path
    subprocess.call(cmd, shell=True)

def youtube_download(terms):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'tmp/youtubedl.mp3'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([terms])

def main(args):
    if (os.path.isdir('tmp')):
        shutil.rmtree('tmp')
    os.mkdir('tmp')

    if args.ytdl:
        youtube_download(args.ytdl)
        path = 'tmp/youtubedl.mp3'
    
    elif args.search:
        youtube_download('ytsearch:' + args.search)
        path = 'tmp/youtubedl.mp3'

    elif args.file:
        path = args.file

    speedup_song(path)
    get_random_image()

    if args.output:
        render_video(args.output)
    else:
        render_video("nightcore.mp4")

    shutil.rmtree('tmp')
    print('Nightcore video successfully generated! You should be ashamed of yourself.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to automatically generate nightcore videos out of an audio file. You should be ashamed of yourself for using that.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-y", "--ytdl", help="use youtube-dl to search for a video or download a specific video")
    group.add_argument("-s", "--search", help="search for a specific song to Nightcore-ify on YouTube (same as --ytdl ytsearch:[search])")
    group.add_argument("-f", "--file", help="file path to the song to Nightcore-ify")
    parser.add_argument("-o", "--output", help="name of the output file")
    main(parser.parse_args())