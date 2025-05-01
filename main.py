from pytubefix import Playlist, YouTube
import os
import argparse

LINKS_PATH = './links'
VIDEO_DIR = f'{os.path.expanduser("~")}/Videos'
AUDIO_DIR = f'{os.path.expanduser("~")}/Music'

parser = argparse.ArgumentParser(description="Download videos/playlists from YouTube")
parser.add_argument("--link", type=str, help="link of a playlist/video")
parser.add_argument("--start", type=int, 
    help="position of a video in the playlist to start downloading from")
parser.add_argument("--audio", type=bool,
    help="download audio file")
args = parser.parse_args()


def create_dir(dir_path: str) -> bool:
    """ Create the directory if it doesn't exist. """
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def download_playlist(link: str, start: int):
    playlist = Playlist(link)
    videos = enumerate(playlist.videos, start=start)
    print(f'Playlist: {playlist.title}')
    playlist_title = "-".join(playlist.title.split("/"))
    playlist_path = f'{VIDEO_DIR}/{playlist_title}'
    create_dir(playlist_path)
    for index, video in videos:
        title = video.title
        if "/" in title:
            title = "-".join(title.split("/"))
        title = f"{index + 1}_{title}.mp4"  
          
        print(f'Downloading video: {title}')
        video.streams.get_highest_resolution().download(
            output_path=playlist_path,
            filename=title)


def download_video(link: str):
    video = YouTube(link)
    print(f'Downloading video: {video.title}')
    title = video.title
    if "/" in title:
        title = "-".join(title.split("/"))
    video.streams.get_highest_resolution().download(output_path=VIDEO_DIR, filename=title)


def download_audio(link: str):
    video = YouTube(link)
    video.streams.get_audio_only().download(
        output_path=AUDIO_DIR,
        filename=video.title)

        
def download(link: str):
    if args.audio:
        download_audio(link=link)
    elif "watch" in link:
        download_video(link=link)
    elif "playlist" in link:
        start = args.start - 1 if args.start else 0
        download_playlist(link=link, start=start)
    else:
        print("Please provide a valid youtube link")


def main():
    if args.link:
        download(args.link)
    else:   
        with open(LINKS_PATH, 'r') as links:
            for link in links:
                download(link)

if __name__ == "__main__":
    main()