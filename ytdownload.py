from colorama import Fore, Back, Style
from pytube import YouTube
import urllib
import sys
import os

url = ""
dir = ""
itag = ""
file_name = ""
audio_only = None # Mp3 (True) or Mp4 (False)
debug = False

def help_command():
    print("""List of commands for command ytdownload:

* = required
Arguments:
    - *url=https://www.youtube.com/watch?v= 
    - audio_only=<bool> | Default = False
    - itag=<integer> | Use --streams [url] for itag information, Defualt = get_highest_resolution()
    - debug=<bool> | Default = False
    - file_name=str.mp4 | Defualt = defualt_filename 
            (remember to put .mp4 at the end or .mp3 if audio_only=True)
    - dir=<string> | Defualt = current directory, example: dir=./Desktop/videos

Commands:
    --help (shows help menu)
    --verison (shows verison)
    --streams [url] """)

def error_function(msg: str):
    # Resets style (for simplicity), Makes the string "ERROR: " Red
    # and turns the actually error message back to regular text.
    print(f"\n{Style.RESET_ALL}{Back.RED}ERROR:{Back.BLACK} {msg}")


def download_video(
        url: str, 
        audio_only: bool, 
        itag: int, 
        file_name: str,
        dir: str
    ):
    
    try:
        yt_video = YouTube(url)
    except Exception:
        error_function(msg="No url/incorrect youtube url. Please try again")
        return

    # User input confirmation:
    print(Style.RESET_ALL)
    print(f"{Back.LIGHTBLUE_EX}[ CONFIRMATION ]:{Style.RESET_ALL}")

    try:
        print(f"Title: {yt_video.title}\nViews: {yt_video.views:,}")
    except urllib.error.URLError:
        # No internet error handling.
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

    # Video downloading, filtering, and file renaming.
    if (itag != ""):
        yt_video.streams.get_by_itag(itag=itag).download(dir)
        print("Video Succesfully downloaded.")

        if (file_name != ""):
            os.rename(yt_video.streams.get_by_itag(itag=itag).default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")
        
    elif (audio_only != None):
        yt_video.streams.filter(audio_only=audio_only).download(dir)

        if (file_name != ""):
            os.rename(yt_video.streams.filter(audio_only=audio_only).default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")

    else:
        yt_video.streams.get_highest_resolution().download(dir)
        print("Video Succesfully downloaded.")

        if (file_name != ""):
            os.rename(yt_video.streams.get_highest_resolution().default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")

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

                # Becuase Youtube urls have a "=" sign in them we must put this in
                # to handle for them.
                except ValueError: 
                    try:
                        arg, result, result2 = item.split("=")
                        result += "=" + result2 
                    except Exception:
                        error_function(msg="Unsupported Argument")

                # Argument Handling:
                if (arg == "url"):
                    url = result
                
                elif (arg.lower() == "audio_only"):
                    audio_only = bool(result)
                
                elif (arg.lower() == "itag"):
                    itag = result
                
                elif (arg.lower() == "debug"):
                    debug = bool(result)
                
                elif (arg.lower() == "file_name"):
                    file_name = result
                
                elif (arg.lower() == "dir"):
                    dir = result
                
                else:
                    error_function(msg=f"{arg} is unknown, do --help for all arguments and commands.")
                
            if (url == None):
                error_function(msg="You must enter a link, example: url=LINK_HERE")

            download_video(url=url, audio_only=audio_only, 
                           itag=itag, file_name=file_name,
                           dir=dir)

    except IndexError as e:
        error_function(msg=f"Please enter a argument.")

    if (debug == True):
        # Used for debugging purposes.
        print(f"\n[ DEBUG: ] \nurl={url} \nitag={itag} \naudio_only={audio_only}\nfile_name={file_name}")