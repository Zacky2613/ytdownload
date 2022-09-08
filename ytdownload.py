from colorama import Back, Style
from pytube import YouTube
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


def help_command():
    print("""List of commands for command ytdownload:

* = required
Options:
    --version,\t\tDisplays version of ytdownload
    --help,\t\tShows all argument options
    --streams, [url],\tShows stream information about a url

    *url=YOUTUBE_VIDEO_LINK,\t- Youtube video url.
    audio_only={True|False},\t- Audio only video (default=false).
    itag=ITAG,\t\t\t- Select video using itag (--streams for itag).
    debug_mode={True|False},\t- Shows debugging information.
    file_name=FILE.mp4,\t\t- Change video file name (default=video title).
    dir=SAVE_DIRECTORY,\t\t- Directory to save video (default=cd).
""")


def error_function(msg: str) -> None:
    print(f"\n{Style.RESET_ALL}{Back.RED}ERROR:{Back.RESET} {msg}{Style.RESET_ALL}")


def download_video(
        url: str,
        audio_only: bool,
        itag: int,
        file_name: str,
        dir: str,
        ) -> None:

    try:
        yt_video = YouTube(url)
    except Exception:
        error_function(msg="No url/incorrect youtube url. Please try again")
        return

    # User input confirmation:
    print(Style.RESET_ALL)
    print(f"{Back.LIGHTBLUE_EX}[ CONFIRMATION ]:{Style.RESET_ALL}")

    try:
        print(f"Title: {yt_video.title} \nCreator: {yt_video.author}\n")
        print(f"Views: {yt_video.views:,}")

        print(f"\nFile Name: \"{file_name}\"\nDirectory: {dir}")

    except urllib.error.URLError:  # No internet error handling.
        error_function(msg="You need internet to use this command.")
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
    if (itag != ""):
        yt_video.streams.get_by_itag(itag=itag).download(dir)

    elif (audio_only is not None):
        yt_video.streams.filter(audio_only=audio_only).download(dir)

    elif (audio_only is not None and itag != ""):
        yt_video.streams.filter(audio_only=audio_only, itag=itag).download(dir)

    else:
        yt_video.streams.get_highest_resolution().download(dir)

    print("[STATUS]: Video succesfully downloaded.")

    if (file_name != ""):
        try:
            os.rename(dir + yt_video.streams.get_highest_resolution().default_filename,
                      dir + file_name)

        except FileExistsError:
            error_function(msg=f"\"{file_name}\" exists, delete file to contuine.")
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

        elif (sys.argv[1] == "--version"):
            print("v1.0")

        elif (sys.argv[1] == "--streams"):
            yt_videoo = YouTube(sys.argv[2])
            print(yt_videoo.streams)

        else:
            for item in sys.argv[1:]:
                try:
                    arg, result = item.split("=")

                except ValueError:
                    try:
                        arg, result, result2 = item.split("=")
                        result += "=" + result2
                        # Becuase Youtube urls have a "=" in them.
                    except Exception:
                        error_function(msg="Unsupported Argument")

                # Argument Handling:
                if (arg == "url"):
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
                           dir=dir)

    except IndexError:
        error_function(msg="Please enter a argument.")

    if (debug_mode is True):
        # Used for debugging purposes.
        print(f"\n[ DEBUG: ] \nurl={url} \nitag={itag} \n\
        audio_only={audio_only}\nfile_name={file_name}\n")
