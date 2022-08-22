from colorama import Fore, Back, Style
from moviepy.editor import * 
from pytube import YouTube
import urllib
import sys
import os

url = ""
dir = ""
itag = ""
file_name = ""
audio_only = None # Mp3 (True) or Mp4 (False)
video_clip = ["", ""] 
debug_mode = False

def help_command():
    print("""List of commands for command ytdownload:

* = required
Options:
    --version,\t\tDisplays version of ytdownload
    --help,\t\tShows all argument options
    --streams, [url],\tShows stream information about a url

    *url=YOUTUBE_VIDEO_LINK,\t- Youtube video url.
    audio_only={True|False},\t- audio only video (default=false).
    itag=ITAG,\t\t\t- select video using itag (get itag info by using --streams).
    debug_mode={True|False},\t- Shows debugging information.
    file_name=FILE.mp4,\t\t- change video file name (default=video title).
    dir=SAVE_DIRECTORY,\t\t- type in a directory for the video to save to (default=current directory).
    clip=START_AT-END_AT,\t- (seconds) example: clip=0-15.5 (defualt=full video).
""")

def error_function(msg: str) -> None:
    # Resets style (for simplicity), Turns background text red for "ERROR:",
    # and finally resets background for the error message itself.
    print(f"\n{Style.RESET_ALL}{Back.RED}ERROR:{Back.RESET} {msg}{Style.RESET_ALL}")


def download_video(
        url: str, 
        audio_only: bool, 
        itag: int, 
        file_name: str,
        dir: str,
        video_clip: list[float]
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
        print(f"Title: {yt_video.title} \nCreator: {yt_video.author}\nViews: {yt_video.views:,}")

    except urllib.error.URLError: # No internet error handling.
        error_function(msg="You need internet to use this command.")
        return

    while True:
        user_input = input("\nConfirm [y/n]: ")
        if (user_input.lower() == "y" or user_input.lower() == "yes"):
            print("\nDownloading video...")
            break

        elif (user_input.lower() == "n" or user_input.lower() == "no"):
            print("Cancelling download.")
            return
        else:
            error_function(msg="Unknown input, please try again.")

    # Video downloading, filtering, and renaming.
    if (itag != ""):
        yt_video.streams.get_by_itag(itag=itag).download(dir)

    elif (audio_only != None):
        yt_video.streams.filter(audio_only=audio_only).download(dir)

    elif (audio_only != None and itag != ""):
        yt_video.streams.filter(audio_only=audio_only, itag=itag).download(dir)

    else:
        yt_video.streams.get_highest_resolution().download(dir)

    print("Video Succesfully downloaded.")

    if (file_name != ""):
        try:
            os.rename(dir + yt_video.streams.get_highest_resolution().default_filename,
                    dir + file_name)

        except FileExistsError:
            error_function(msg=f"\"{file_name}\" already exists, delete file to contuine.")
            return

        print(f"\nVideo renamed to \"{file_name}\"")

    
    if (video_clip != []):
        if (file_name != ""):
            video = VideoFileClip(dir + file_name)
            video = video.subclip(video_clip[0], video_clip[1]) 
            video.write_videofile(dir + "clipped" + file_name, verbose=False, logger=None)   
        else:
            video = VideoFileClip(dir + yt_video.title + ".mp4")
            video = video.subclip(video_clip[0], video_clip[1]) 
            video.write_videofile(dir + "clipped" + yt_video.title + ".mp4", verbose=False, logger=None)

            # 'dir + "clipped"' is a temporary solution because of a issue with moviepy,
            # where os.remove() doesn't work because somewhere is using it so it cannot be deleted.
            # More information at this github issue: https://github.com/Zulko/moviepy/issues/1819

        print(f"Video clipped down to {video_clip[0]}s-{video_clip[1]}s")

    if (dir != ""):
        print(f"Video moved to {dir}")


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
                        # Becuase Youtube urls have a "=" in them we must put this here to handle it.
                    except Exception:
                        error_function(msg="Unsupported Argument")

                # Argument Handling:
                if (arg == "url"):
                    url = result
                
                elif (arg.lower() == "audio_only"):
                    audio_only = bool(result)
                
                elif (arg.lower() == "itag"):
                    itag = result
                
                elif (arg.lower() == "debug_mode"):
                    debug_mode = bool(result)
                
                elif (arg.lower() == "file_name"):
                    file_name = result
                
                elif (arg.lower() == "dir"):
                    if (result[-1] != "\\"):
                        result += "/"

                    dir = result
                
                elif (arg.lower() == "clip"):
                    result = result.split("-")

                    for item in result:
                        try:
                            item = float(item)
                        except ValueError:
                            error_function(msg="Cannot enter letters in clip.")
                            exit()


                        video_clip.append(item)
                
                else:
                    error_function(msg=f"{arg} is unknown, do --help for all arguments and commands.")
                
            if (url == None):
                error_function(msg="You must enter a link, example: url=LINK_HERE")

            download_video(url=url, audio_only=audio_only, 
                           itag=itag, file_name=file_name,
                           dir=dir, video_clip=video_clip)

    except IndexError as e:
        error_function(msg=f"Please enter a argument.")

    if (debug_mode == True):
        # Used for debugging purposes.
        print(f"\n[ DEBUG: ] \nurl={url} \nitag={itag} \n\
        audio_only={audio_only}\nfile_name={file_name}\n\
        clip={video_clip[0]}s-{video_clip[1]}s")