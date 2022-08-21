from colorama import Fore, Back, Style
from pytube import YouTube
import urllib
import sys
import os

url = ""
itag = ""
file_name = ""
audio_only = None # Mp3 (True) or Mp4 (False)
debug = False


def help_command():
    print("""List of commands for command ytdownload:

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
    --streams [url] """)


def download_video(
        url: str, 
        audio_only: bool, 
        itag: int, 
        file_name: str
    ):
    
    try:
        yt_video = YouTube(url)
    except Exception:
        print("ERROR: No url/incorrect youtube url. Please try again")
        return
    
    print(Style.RESET_ALL)
    print(f"{Back.LIGHTBLUE_EX}[ CONFIRMATION ]:{Style.RESET_ALL}")

    try:
        print(f"Title: {yt_video.title}\nViews: {yt_video.views:,}")
    except urllib.error.URLError:
        # No internet error handling.
        print("ERROR: You need internet to use this command.")
        return

    while True:
        user_input = input("\nConfirm [y/n]: ")
        if (user_input.lower() == "y" or user_input.lower() == "yes"):
            print("\nDownloading video...")
            break

        elif (user_input.lower() == "n" or user_input.lower() == "no"):
            print("Cancelling download.")
            exit()
        else:
            print("unknown option. Please try again")

    if (itag != ""):
        yt_video.streams.get_by_itag(itag=itag).download()
        print("Video Succesfully downloaded.")

        if (file_name != ""):
            os.rename(yt_video.streams.get_by_itag(itag=itag).default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")
        
    elif (audio_only != None):
        yt_video.streams.filter(audio_only=audio_only).download()

        if (file_name != ""):
            os.rename(yt_video.streams.filter(audio_only=audio_only).default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")

    else:
        yt_video.streams.get_highest_resolution().download()
        print("Video Succesfully downloaded.")

        if (file_name != ""):
            os.rename(yt_video.streams.get_highest_resolution().default_filename, file_name)
            print(f"File renamed to \"{file_name}\"")

if __name__ == "__main__":
    try:
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

                # Becuase Youtube urls have a "=" sign in them we must put a exception for them.
                except ValueError: 
                    try:
                        arg, result, result2 = item.split("=")
                        result += "=" + result2 
                    except Exception:
                        print(f"ERROR: Unsupported argument.")

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
                
                else:
                    print(f"{arg} is unknown, do --help for all arguments.")
                
            if (url == None):
                print("ERROR: You Must provided a url. url=LINK")

            download_video(url=url, audio_only=audio_only, 
                           itag=itag, file_name=file_name)

    except IndexError as e:
        print("ERROR: Please enter a argument.")

    if (debug == True):
        # Used for debugging purposes.
        print(f"\n[ DEBUG: ] \nurl={url} \nitag={itag} \naudio_only={audio_only}\nfile_name={file_name}")