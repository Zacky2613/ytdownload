from colorama import Back, Style
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import urllib
import sys
import os

# ytdownload by Zacky2613

url = ""
dir = ""
itag = ""
file_name = ""
audio_only = None  # Mp3 (True) or Mp4 (False)
debug_mode = False
playlist = False


def help_command():
    print("""List of commands for command ytdownload:

* = required
Options:
    --version / -v,\t- Displays version of ytdownload.
    --help,\t\t- Shows all argument options.
    --streams [url],\t- Shows stream information about a url.
    --playlist / -pl,\t- Use for first arg to download playlists.
    --debug,\t\t- Shows debugging information.


    *url=YOUTUBE_VIDEO_LINK,\t- Youtube video url.
    audio_only={True|False},\t- Audio only video (default=false).
    itag=ITAG,\t\t\t- Select video using itag (--streams for itag).
    file_name=FILE.mp4,\t\t- Change video file name (default=video title).
    dir=SAVE_DIRECTORY,\t\t- Directory to save video (default=cd).
""")


def error_function(msg: str) -> None:
    print(f"\n{Style.RESET_ALL}{Back.RED}ERROR:{Back.RESET} {msg}\
        {Style.RESET_ALL}")


def download_video(
        url: str,
        audio_only: bool,
        itag: int,
        file_name: str,
        dir: str,
        playlist: bool
        ) -> None:

    try:
        if (playlist is False):
            yt_video = YouTube(url, on_progress_callback=on_progress)
        else:
            yt_video = Playlist(url)
    except Exception:
        error_function(msg="No url/incorrect youtube url. Please try again")
        return

    # User input confirmation:
    print(Style.RESET_ALL)
    print(f"{Back.LIGHTBLUE_EX}[ CONFIRMATION ]:{Style.RESET_ALL}")

    try:
        if (playlist is False):
            print(f"Title: {yt_video.title}")
            print(f"Creator: {yt_video.author}")
            print(f"Views: {yt_video.views:,}")

        else:
            print(f"Playlist Title: {yt_video.title}")
            print(f"Number of videos: {len(yt_video.video_urls)}")

        print(f"\nFile Name: \"{file_name}\"\nDirectory: {dir}")

    except urllib.error.URLError:  # No internet error handling.
        error_function(msg="You must be connected to internet.")
        return

    while True:
        user_input = input("\nConfirm [y/n]: ")

        if (user_input.lower() == "y" or user_input.lower() == "yes"):
            print("\n[STATUS]: Downloading video.")
            break

        elif (user_input.lower() == "n" or user_input.lower() == "no"):
            print("Cancelling download.")
            return
        else:
            error_function(msg="Unknown input, please try again.")

    # Video downloading, filtering, and renaming.
    try:
        if (itag != ""):
            yt_video.streams.get_by_itag(itag=itag).download(dir)

        elif (audio_only is not None):
            yt_video.streams.get_audio_only(audio_only).download(dir)

        elif (audio_only is not None and itag != ""):
            yt_video.streams.filter(audio_only=audio_only, itag=itag).download(dir)

        else:
            if (playlist is False):
                yt_video.streams.get_highest_resolution().download(dir)
            else:
                for video in yt_video.videos:
                    video_download = video.streams.get_highest_resolution()
                    video_download.download(dir)
                    print(f"\nDownloaded {video_download.title}.")

    except AttributeError:  # If video is not avaiable
        error_function("Video(s) cannot be found, --streams to get by itag")
        return

    print("[STATUS]: Video succesfully downloaded.")

    if (file_name != ""):
        try:
            os.rename(dir + yt_video.streams.get_highest_resolution().default_filename,
                      dir + file_name)

        except FileExistsError:
            error_function(msg=f"\"{file_name}\" exists, delete to contuine.")
            return

        print(f"\n[STATUS]: File renamed to \"{file_name}\"")

    if (dir != ""):
        print(f"[STATUS]: Video saved to dir \"{dir}\"")

    print("\n[STATUS]: Finished, video ready.")


if __name__ == "__main__":
    try:
        # Command handling
        if (sys.argv[1] == "--help"):
            help_command()

        elif (sys.argv[1] == "--version" or sys.argv[1] == "-v"):
            print("v1.2")

        elif (sys.argv[1] == "--streams"):
            yt_videoo = YouTube(sys.argv[2])
            print(yt_videoo.streams)

        else:
            if (sys.argv[1] == "--playlist" or sys.argv[1] == "-pl"):
                playlist = True

            for item in sys.argv[1:]:
                if (item == "--pl" or item == "--playlist"):
                    continue

                try:
                    arg, result = item.split("=")

                except ValueError:
                    if (playlist is False):
                        try:
                            arg, result, result2 = item.split("=")
                            result += "=" + result2
                            # Becuase Youtube urls have a "=" in them.
                        except Exception:
                            error_function(msg="Unsupported Argument")
                            exit()

                    else:
                        try:
                            arg, result, result2, result3 = item.split("=")
                            result += "=" + result2 + "=" + result3

                        except Exception:
                            error_function(msg="Unsupported Argument")
                            exit()

                result = result.replace("\"", "")
                result = result.replace("'", "")

                # Argument Handling:
                if (arg.lower() == "url"):
                    url = result

                elif (arg.lower() == "audio_only"):
                    audio_only = bool(result)

                elif (arg.lower() == "itag"):
                    itag = result

                elif (arg.lower() == "--debug"):
                    debug_mode = bool(result)

                elif (arg.lower() == "file_name"):
                    file_name = result

                elif (arg.lower() == "dir"):
                    if (result[-1] != "\\"):
                        result += "/"

                    dir = result

                else:
                    error_function(msg=f"{arg} is unknown, --help for help.")

            if (url is None):
                error_function(msg="You must enter a link, e.g url=LINK_HERE")

            download_video(url=url, audio_only=audio_only,
                           itag=itag, file_name=file_name,
                           dir=dir, playlist=playlist)

    except IndexError:
        error_function(msg="Please enter a argument.")

    if (debug_mode is True):
        # Used for debugging purposes.
        print(f"\n[ DEBUG: ] \nurl={url} \nitag={itag} \n\
        audio_only={audio_only}\nfile_name={file_name}\n\
        playlist={playlist} \ndir={dir}")
