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
import ffmpeg

pid = os.getpid()
tmp_dir = "tmp_" + str(pid)
debug = False

def speedup_song(path):
    sound = AudioSegment.from_file(path)

    octaves = 4 / 12  # x1.25
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    nightcore = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)

    print("Exporting Audio")

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

    print("Grabbed Image: "+ image_url)

def render_video(path, singleframe):
    input_image = tmp_dir + '/image.jpg'
    input_audio = tmp_dir + '/nightcore.mp3'
    
    video = ffmpeg.input(input_image, loop=1)
    audio = ffmpeg.input(input_audio)
    
    if singleframe:
        video = ffmpeg.filter(video, 'fps', fps=1)
    
    output_params = {
        'vcodec': 'libx264',
        'acodec': 'copy',
        'pix_fmt': 'yuv420p',
        'shortest': None
    }
    
    try:
        if debug == True:
            (
                ffmpeg
                .output(video, audio, path, **output_params)
                .run(quiet=False, overwrite_output=True)
            )
        if debug == False:
            (
                ffmpeg
                .output(video, audio, path, **output_params)
                .run(quiet=True, overwrite_output=True)
            )
        return True
    except ffmpeg.Error as e:
        print("Error when making the video: \n"+e.stderr.decode('utf8'))
        return False



def youtube_download(terms):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': tmp_dir + '/yt_dlp'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([terms])


def main(args):
    global debug
    if args.debug:
        debug = True
        print("Debugging Enabled")

    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
        print("Removed old temp directory")
    os.mkdir(tmp_dir)
    print("Made temp directory")

    path = ''
    if args.ytdl:
        print("Started Video Downloading")
        youtube_download(args.ytdl)
        path = tmp_dir + '/yt_dlp.mp3'
        print("Finished Downloading")

    elif args.search:
        print("Started search with "+ args.search)
        youtube_download('ytsearch:' + args.search)
        path = tmp_dir + '/yt_dlp.mp3'
        print("Finished search")

    elif args.file:
        print("Set path is "+ args.file)
        path = args.file

    print("Starting song speedup")
    speedup_song(path)

    print("Grabbing Image from SafeBooru")
    get_random_image()

    print("Grabbing Filename from Path")
    if "/" in path:
        output = path.split("/")[-1] + " Nightcore" + ".mp4"
    if "\\" in path:
        output = path.split("\\")[-1] + " Nightcore"+ ".mp4"
    if args.output:
        output = args.output

    print("Output directory is "+ output)

    print("Rendering video")
    return_code = render_video(output, args.frame)

    print("Removing temp directory")
    shutil.rmtree(tmp_dir)

    if return_code == True:
        print('Nightcore video successfully generated! You should be ashamed of yourself.')
    else:
        print('Error while rendering video...', file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool to automatically generate nightcore videos out of an audio file. You should be ashamed of yourself for using that.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-y", "--ytdl", help="use yt-dlp to search for a video or download a specific video")
    group.add_argument("-s", "--search", help="search for a specific song to Nightcore-ify on YouTube (same as --ytdl ytsearch:[search])")
    group.add_argument("-f", "--file", help="file path to the song to Nightcore-ify")
    parser.add_argument("-o", "--output", help="name of the output file")
    parser.add_argument("-1", "--frame", action='store_true', help="sets framerate to 1 for faster encoding & lighter file. May affect compatibility with some video players")
    parser.add_argument("-d", "--debug", action='store_true', help="Running the script with the debug output")
    main(parser.parse_args())
