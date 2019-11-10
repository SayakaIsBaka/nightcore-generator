# nightcore-generator

A tool to automatically generate nightcore videos out of an audio file. It grabs the image from Safebooru using specific tags.
You should be ashamed of yourself for using that.

Please do not actually use this to make actual Nightcore videos and upload them. Seriously.

## Requirements
- Python 3 (tested on 3.7)
- [pydub](https://github.com/jiaaro/pydub)
- [requests](https://pypi.org/project/requests)
- [youtube-dl](http://ytdl-org.github.io/youtube-dl)
- ffmpeg

## Setting up

For instructions on how to install ffmpeg, please see [this page.](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up)

### Using pipenv
```sh
pipenv install
```

### Without pipenv
```sh
pip install pydub requests youtube-dl
```

## Usage

Use the `--help` argument to have a list of the different arguments.

### Using pipenv
```sh
# To specifiy a local file
pipenv run python nightcore.py --file [audio file]

# To search on YouTube
pipenv run python nightcore.py --search [search query]

# To use youtube-dl
pipenv run python nightcore.py --ytdl [query]

# To set output filename
pipenv run python nightcore.py --ytdl/search/file -o [output filename]
pipenv run python nightcore.py --ytdl/search/file --output [output filename]

# To set framerate to 1fps (outputs a lighter file, but less compatible with playback)
pipenv run python nightcore.py --ytdl/seach/file -1
pipenv run python nightcore.py --ytdl/seach/file --frame

```

### Without pipenv
```sh
# To specifiy a local file
python nightcore.py --file [audio file]

# To search on YouTube
python nightcore.py --search [search query]

# To use youtube-dl
python nightcore.py --ytdl [query]

# To set output filename
python nightcore.py --ytdl/search/file -o [output filename]
python nightcore.py --ytdl/search/file --output [output filename]

# To set framerate to 1fps (outputs a lighter file, but less compatible with playback)
python nightcore.py --ytdl/seach/file -1
python nightcore.py --ytdl/seach/file --frame
```

I'm deeply sorry for making that, please forgive me
