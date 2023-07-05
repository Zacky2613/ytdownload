# ytdownload

A command line tool which can download youtube videos and playlists without the hassal of dealing with websites.

## Features

ytdownload has a whole range of features including:

- Youtube Video, Shorts, and Playlist downloading
- Arguments to change the filename and save dir
- Confirmation page showing information about the vidoe to know if you choose the right one.
- If you want videos that are just the audio
- And other features like itags so you can choose which video you want exactly to download.

## Installation

You'll need to have Python 3.6+ and run the command `pip install -r requirements.txt`

## Commands/Arguments

A copy of this can be found in the terminal using the command, `ytdownload --help`.

```text
* = requried
DOWNLOAD AND SAVING:
    *url=[video_url]: The Youtube url to download the video.
    dir=[dir]: The directory to save the video(s) too. (e.g: dir=./yt-videos)
    file_name=[NAME].mp4: When download a video and not a playlist rename the file name after it's done
    itag=[ITAG]: Download videos using itags, itags are found in --streams.
    audio_only=[True|False]: Output video as just audio.

    [PLAYLISTS]:
        --playlist/-pl: Tells the program you're download a playlist, wont download without this argument.

INFORMATION:
    --debug: Shows debugging information.
    --help: What you're reading, shows information on all commands.
    --version/-v: Displays current version of the program.
    --streams: enter the url argument aswell with this command. Shows information about every possible download.

```

## Examples

This will download a video and rename it too "video.mp4"

`ytdownload url=https://www.youtube.com/watch?v=ExwqNreocpg file_name=video.mp4`

This will download a playlist, folder name as "playlist_videos", and set the directory as the parent folder.
`ytdownload --Playlist url=https://www.youtube.com/playlist?list=PL38p7pccpLcTxGhBKcy9zCjD61I0dN2PT file_name=playlist_videos dir=../`
