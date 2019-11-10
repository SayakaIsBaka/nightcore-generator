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

### Using pipenv
```sh
# To specifiy a local file
pipenv run python nightcore.py --file [audio file]

# To search on YouTube
pipenv run python nightcore.py --search [search query]

# To use youtube-dl
pipenv run python nightcore.py --ytdl [query]
```

### Without pipenv
```sh
# To specifiy a local file
python nightcore.py --file [audio file]

# To search on YouTube
python nightcore.py --search [search query]

# To use youtube-dl
python nightcore.py --ytdl [query]
```

I'm deeply sorry for making that, please forgive me