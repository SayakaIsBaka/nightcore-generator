# nightcore-generator

A tool to automatically generate nightcore videos out of an audio file. It grabs the image from Safebooru using specific tags.
You should be ashamed of yourself for using that.

Please do not actually use this to make actual Nightcore videos and upload them. Seriously.

## Requirements
- Python 3 (tested on 3.7)
- [pydub](https://github.com/jiaaro/pydub)
- [requests](https://pypi.org/project/requests)
- ffmpeg

## Setting up

For instructions on how to install ffmpeg, please see [this page.](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up)

### Using pipenv
```sh
pipenv install
```

### Without pipenv
```sh
pip install pydub requests
```

## Usage

### Using pipenv
```sh
pipenv run python nightcore.py [audio file]
```

### Without pipenv
```sh
python nightcore.py [audio file]
```

I'm deeply sorry for making that, please forgive me