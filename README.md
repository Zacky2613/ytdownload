# ytdownload

ytdownload is a terminal based way of downloading youtube videos throught the `ytdownload` command. It is made using python and the pytube module.

## Installation

...

## Commands

A copy of this can be found in the terminal using the command, `ytdownload --help`.

```text
* = required
Arguments:
    - *url = https://www.youtube.com/watch?v= 
    - audio_only = <bool> | Default = False
    - itag = <integer> | Use --streams [url] for itag information, Defualt = get_highest_resolution()
    - debug = <bool> | Default = False
    - file_name = str.mp4 | Defualt = defualt_filename 
            (remember to put .mp4 at the end or .mp3 if audio_only=True)

Commands:
    --help (shows help menu)
    --verison (shows verison)
    --streams [url]
```

## Example

```text
ytdownload url=https://www.youtube.com/watch?v=ExwqNreocpg file_name=video.mp4
```
