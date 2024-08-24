#! /usr/bin/env python3

from pydub import AudioSegment
from random import randrange, choice
from xml.etree import ElementTree

import sys
import os
import shutil
import requests
import subprocess
import argparse
import yt_dlp

pid = os.getpid()
tmp_dir = "tmp_" + str(pid)


def speedup_song(path):
    sound = AudioSegment.from_file(path)

    octaves = 4 / 12  # x1.25
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    nightcore = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)

    nightcore.export(tmp_dir + "/nightcore.mp3", format="mp3", bitrate="192k")


def get_request_url(page, tag):
    return "https://safebooru.org/index.php?page=dapi&s=post&q=index&pid=" + str(
        page) + "&tags=width:1920+height:1080+-swimsuit+-feet+-text+score:>=1+" + tag


def get_random_image():
    tags = ['looking_at_another', '1girl', 'vocaloid', '1girl+1boy', '2girls']
    tag = choice(tags)

    total_results = int(ElementTree.fromstring(requests.get(get_request_url(1, tag)).content).get('count'))
    if total_results == 0:
        print("No images found... Retry by relaunching the script", file=sys.stderr)
        exit(1)
    image_id = randrange(0, total_results)
    page = image_id // 100

    r = requests.get(get_request_url(page, tag))
    image_list = list(ElementTree.fromstring(r.content))
    image_url = image_list[image_id % 100].get('file_url')
    img_data = requests.get(image_url).content

    with open(tmp_dir + '/image.jpg', 'wb') as handler:
        handler.write(img_data)


def render_video(path, singleframe):
    rate = ''
    if singleframe:
        rate = '-r 1 '
    cmd = 'ffmpeg -loop 1 -i ' + tmp_dir + '/image.jpg -i ' + tmp_dir + '/nightcore.mp3 -c:v libx264 ' + rate + '-c:a copy -pix_fmt yuv420p ' \
                                                                                                                '-shortest ' + path
    return subprocess.call(cmd, shell=True)


def youtube_download(terms):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': tmp_dir + '/yt_dlp.mp3'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([terms])


def main(args):
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    path = ''
    if args.ytdl:
        youtube_download(args.ytdl)
        path = tmp_dir + '/yt_dlp.mp3'

    elif args.search:
        youtube_download('ytsearch:' + args.search)
        path = tmp_dir + '/yt_dlp.mp3'

    elif args.file:
        path = args.file

    speedup_song(path)
    get_random_image()

    output = "nightcore_" + str(pid) + ".mp4"
    if args.output:
        output = args.output

    return_code = render_video(output, args.frame)
    shutil.rmtree(tmp_dir)

    if return_code == 0:
        print('Nightcore video successfully generated! You should be ashamed of yourself.')
    else:
        print('Error while rendering video...', file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A tool to automatically generate nightcore videos out of an audio file. You should be ashamed of "
                    "yourself for using that.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-y", "--ytdl", help="use yt-dlp to search for a video or download a specific video")
    group.add_argument("-s", "--search",
                       help="search for a specific song to Nightcore-ify on YouTube (same as --ytdl ytsearch:[search])")
    group.add_argument("-f", "--file", help="file path to the song to Nightcore-ify")
    parser.add_argument("-o", "--output", help="name of the output file")
    parser.add_argument("-1", "--frame", action='store_true',
                        help="sets framerate to 1 for faster encoding & lighter file. May affect compatibility with "
                             "some video players")
    main(parser.parse_args())
