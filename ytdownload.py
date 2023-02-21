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

banned_filename_characters = [
    '&', '"', '?', '<', '>', '#',
    '{', '}', '%', '~', '/', '\\'
]


def help_command():
    print("""List of commands for command ytdownload v1.2.2:

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

    # Confirmation page, showing information about the video/playlist-
    # and how they want to store it.
    print(Style.RESET_ALL)
    print(f"{Back.LIGHTBLUE_EX}[ CONFIRMATION ]:{Style.RESET_ALL}")

    try:
        if (playlist is False):
            print(f"Title: {yt_video.title}")
            print(f"Creator: {yt_video.author}")
            print(f"Views: {yt_video.views}")

        else:
            print(f"Playlist Title: {yt_video.title}")
            print(f"Number of videos: {len(yt_video.video_urls)}")

        if (file_name == ""):
            # This is because Windows bans some characters being in a filename
            title_name = yt_video.title
            for symbol in banned_filename_characters:
                title_name = title_name.replace(symbol, "")

            # Becuase Playlist files get put into a folder.
            if (Playlist is False):
                print(f"\nFile Name: \"{title_name}.mp4\" ")
            else:
                print(f"\nFolder Name: \"{title_name}\" ")

        else:
            if (Playlist is False):
                print(f"\nFile Name: \"{file_name}\".mp4")
            else:
                print(f"\nFolder Name: \"{file_name}\"")

        print(f"Directory: {dir}")

    except urllib.error.URLError:  # No internet error handling.
        error_function(msg="You must be connected to internet.")
        return

    # User confirmation input
    while True:
        if (Playlist is True):
            print("\n[NOTE]: Playlists will create a folder to store videos into")

        user_input = input("Confirm [y/n]: ")

        if (user_input.lower() == "y" or user_input.lower() == "yes"):
            print("\n[STATUS]: Downloading video.")
            break

        elif (user_input.lower() == "n" or user_input.lower() == "no"):
            print("Cancelling download.")
            return
        else:
            error_function(msg="Unknown input, please try again.")

    # Video downloading, filtering, and renaming section.
    try:
        if (itag != ""):  # itag downloading.
            yt_video.streams.get_by_itag(itag=itag).download(dir)

        elif (audio_only is not None):
            yt_video.streams.get_audio_only(audio_only).download(dir)

        elif (audio_only is not None and itag != ""):
            yt_video.streams.filter(audio_only=audio_only, itag=itag).download(dir)

        # Playlist/video downloading section
        else:
            if (playlist is False):
                yt_video.streams.get_highest_resolution().download(dir)
            else:
                # Creates a folder and downloads into the folder.
                if (file_name == ""):
                    os.system(f'mkdir "{yt_video.title}"')
                    dir += f'{yt_video.title}'
                else:
                    os.system(f'mkdir "{file_name}"')
                    dir += f'{file_name}'

                for video in yt_video.videos:
                    video_download = video.streams.get_highest_resolution()
                    video_download.download(dir)
                    print(f"Downloaded {video_download.title}.")

    except AttributeError:  # If video is not avaiable
        error_function("Video(s) cannot be found, --streams to download by itag")
        return

    print("[STATUS]: Video succesfully downloaded.")

    # Changing the downloaded video's filename.
    if (file_name != "" and playlist is False):
        try:
            os.rename(dir + yt_video.streams.get_highest_resolution().default_filename,
                      dir + file_name)

        except FileExistsError:
            error_function(msg=f"\"{file_name}\" exists, delete to contuine.")
            return

        print(f"\n[STATUS]: File renamed to \"{file_name}\"")

    # Confirming where the videos were saved.
    if (dir != ""):
        print(f"[STATUS]: Video saved to dir \"{dir}\"")


if __name__ == "__main__":
    try:
        # "--" Command handling
        if (sys.argv[1] == "--help"):
            help_command()

        elif (sys.argv[1] == "--version" or sys.argv[1] == "-v"):
            print("v1.2.2")

        elif (sys.argv[1] == "--streams"):
            video_streams = YouTube(sys.argv[2])
            print(video_streams.streams)

        else:
            # Becuase --playlist takes in other commands, it's excluded from the other -- commands.
            if (sys.argv[1] == "--playlist" or sys.argv[1] == "-pl"):
                playlist = True

            for item in sys.argv[1:]:
                if (item == "-pl" or item == "--playlist"):
                    continue

                try:
                    arg, result = item.split("=")

                except ValueError:
                    if (item == "--debug"):
                        debug_mode = True
                        continue

                    elif (playlist is False):
                        try:
                            arg, result, result2 = item.split("=")
                            result += "=" + result2
                            # Becuase Youtube urls have a "=" in them.
                        except Exception:
                            error_function(msg="Unsupported Argument")
                            exit()

                    else:
                        try:
                            arg, result, result2 = item.split("=")
                            result += "=" + result2

                        except Exception:
                            error_function(msg="Unsupported Argument")
                            exit()

                # No clue why these are hear, but too scared to remove them.
                result = result.replace("\"", "")
                result = result.replace("'", "")

                # Regular command handling
                if (arg.lower() == "url"):
                    url = result

                elif (arg.lower() == "audio_only"):
                    audio_only = bool(result)

                elif (arg.lower() == "itag"):
                    itag = result

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
        # Used for debugging purposes. Do --debug to display this.
        print("\n[ DEBUG: ]")
        print(f"url={url}")
        print(f"itag={itag}")
        print(f"audio_only={audio_only}")
        print(f"file_name={file_name}")
        print(f"playlist={playlist}")
        print(f"dir={dir}")
