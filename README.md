# ytdownload

A command line tool which can download youtube videos and playlists without the hassal of dealing with websites.

## Features

ytdownload has a whole range of features including:

- Youtube video downloading
- Youtube Playlist downloading
- Commands to change the file name
- Commands to change where the video(s) are saved
- Confirmation page showing information about the vidoe to know if you choose the right one.
- If you want videos that are just the audio
- And other features like itags so you can choose which video you want exactly to download.

## Installation

You'll need to have Python 3.6+ and run the command `pip install -r requirements.txt`

## Commands/Arguments

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

## Examples

This will download a video and rename it too "video.mp4"

`ytdownload url=https://www.youtube.com/watch?v=ExwqNreocpg file_name=video.mp4`

This will download a playlist, folder name as "playlist_videos", and set the directory as the parent folder.
`ytdownload --Playlist url=https://www.youtube.com/playlist?list=PL38p7pccpLcTxGhBKcy9zCjD61I0dN2PT file_name=playlist_videos dir=../`
