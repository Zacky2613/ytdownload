# ytdownload

ytdownload is a tool to use download youtube videos and playlists using the command line. Made using python and the pytube module. I'd recommended putting into your PATH for easier use.

## Installation

You will need to have Python 3.6+ and install the following modules:

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
    --version,          - Displays version of ytdownload.
    --help,             - Shows all argument options.
    --streams [url],    - Shows stream information about a url.
    --playlist / --pl,  -Use this for first argument and use a playlist video link to download playlists.
    --debug,            - Shows debugging information.

    *url=YOUTUBE_VIDEO_LINK,    - Youtube video url.
    audio_only={True|False},    - audio only video (default=false).
    itag=ITAG,                  - select video using itag (get itag info by using --streams).
    file_name=FILE.mp4,         - change video file name (default=video title).
    dir=SAVE_DIRECTORY,         - type in a directory for the video to save to (default=current directory).
```

## Example

```text
ytdownload url=https://www.youtube.com/watch?v=ExwqNreocpg file_name=video.mp4
```
