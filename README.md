# ytdownload

ytdownload is a terminal based way of downloading youtube videos throught the `ytdownload` command. It is made using python and the pytube module. I would recommened putting the ytdownload.py into PATH for easier use.

## Installation

The following modules will need to be installed for the program to work (if running the .py file):

```text
# Linux/macOS
py3 -m pip install colorama
py3 -m pip install pytube

# Windows
python3 -m pip install colorama
python3 -m pip install pytube
```

## Commands

A copy of this can be found in the terminal using the command, `ytdownload --help`.

```text
* = required
Options:
    --version,          - Displays version of ytdownload
    --help,             - Shows all argument options
    --streams [url],    - Shows stream information about a url

    *url=YOUTUBE_VIDEO_LINK,    - Youtube video url.
    audio_only={True|False},    - audio only video (default=false).
    itag=ITAG,                  - select video using itag (get itag info by using --streams).
    debug_mode={True|False},    - Shows debugging information.
    file_name=FILE.mp4,         - change video file name (default=video title).
    dir=SAVE_DIRECTORY,         - type in a directory for the video to save to (default=current directory).
    clip=START_AT-END_AT,       - (seconds) example: clip=0-15.5 (defualt=full video).
```

## Example

```text
ytdownload url=https://www.youtube.com/watch?v=ExwqNreocpg file_name=video.mp4
```
