from pytube import Playlist, YouTube
import os
import argparse

LINKS_PATH = './links'
VIDEO_DIR = f'{os.path.expanduser("~")}/Videos'
AUDIO_DIR = f'{os.path.expanduser("~")}/Music'

parser = argparse.ArgumentParser(description="Download videos/playlists from YouTube")
parser.add_argument("--link", type=str, help="link of a playlist/video")
parser.add_argument("--start_with", type=int, 
    help="position of a video in the playlist to start downloading from")
parser.add_argument("--nth_video", type=int, 
    help="download single video from a playlist")
parser.add_argument("--audio", type=bool,
    help="download audio file")
args = parser.parse_args()


def create_dir(dir_path: str) -> bool:
    """ Create the directory if it doesn't exist. """
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def download_playlist(link: str):
    if args.link:
        playlist = Playlist(args.link)
    else:
        playlist = Playlist(link)
    print(f'Playlist: {playlist.title}')
    playlist_title = "-".join(playlist.title.split("/"))
    current_playlist_path = f'{VIDEO_DIR}/{playlist_title}'
    create_dir(current_playlist_path)
    video_counter = 0
    start_from = 0
    v_num = False
    if args.start_with:
        start_from = args.start_with
    if args.nth_video:
        v_num = args.nth_video
    for video in playlist.videos:
        video_counter += 1
        if video_counter < start_from:
            continue
        if v_num and video_counter < v_num:
            continue
        if v_num and video_counter > v_num:
            break
        try:
            title = video.title
        except Exception:
            print("Not able to access video title.")
            title = ""
        else:
            if "/" in title:
                title = "-".join(title.split("/"))
        title = f"{video_counter}_{title}"    
        print(f'Downloading video: {title}')
        video.streams.get_highest_resolution().download(output_path=current_playlist_path,filename=title)


def download_video(link: str):
    video = YouTube(link)
    print(f'Downloading video: {video.title}')
    if "/" in video.title:
        video.title = "-".join(video.title.split("/"))
    # print(video.streams)
    # itag = int(input("Enter the stream itag: "))
    # print(itag)
    # itag = 271
    # video_stream = video.streams.get_by_itag(itag)
    video_stream = None
    if video_stream:
        video_stream.download(output_path=VIDEO_DIR, filename=video.title)
    else:
        # print("Something went wrong. Downloading lower resolution video.")
        video.streams.get_highest_resolution().download(output_path=VIDEO_DIR, filename=video.title)


def download_audio(link: str):
    try:
        video = YouTube(link)
        video.streams.get_audio_only().download(output_path=AUDIO_DIR, filename=video.title)
    except KeyError:
        print('KeyError')
        errors += 1
        if errors == 10:
            return
        else:
            download_audio(link)
    except Exception as err:
        print(f"General error!\n{err}")

        
def download(link: str):
    if args.audio:
        download_audio(link=link)
    elif "watch" in link:
        download_video(link=link)
    elif "list" in link:
        download_playlist(link=link)
    else:
        print("Please provide a valid youtube link")
        return


def main():
    if args.link:
        download(args.link)
    else:   
        with open(LINKS_PATH, 'r') as links:
            for link in links:
                download(link)

if __name__ == "__main__":
    main()
