from pytube import Playlist, YouTube
from urllib import error
import os
import argparse
import sys

parser = argparse.ArgumentParser(description="Download videos/playlists from YouTube")
parser.add_argument("--type", type=str, help="is it a single video or a playlist?")
parser.add_argument("--link", type=str, help="link of a playlist/video")
parser.add_argument("--links_file", type=str,
    help="location of a file with videos/pleylists links")
parser.add_argument("--start_with", type=int, 
    help="position of a video in the playlist to start downloading from")
parser.add_argument("--video_number", type=int, 
    help="download single video from a playlist")    
parser.add_argument("--dest", type=str, 
    help="destination path where videos will be saved")
args = parser.parse_args()
links_path = './links'
dest_dir = f'{os.path.expanduser("~")}/Videos'
if args.links_file:
    links_path = args.links_file
if args.dest:
    dest_dir = args.dest


def create_dir(dir_path: str) -> bool:
    """ Create the directory if it doesn't exist. """
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)


def download_playlist(link=None):
    if args.link:
        playlist = Playlist(args.link)
    else:
        playlist = Playlist(link)
    print(f'Playlist: {playlist.title}')
    current_playlist_path = f'{dest_dir}/{playlist.title}'
    create_dir(current_playlist_path)
    video_counter = 0
    start_from = 0
    v_num = False
    if args.start_with:
        start_from = args.start_with
    if args.video_number:
        v_num = args.video_number
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


def download_video():
    video = YouTube(args.link)
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
        video_stream.download(output_path=dest_dir, filename=video.title)
    else:
        # print("Something went wrong. Downloading lower resolution video.")
        video.streams.get_highest_resolution().download(output_path=dest_dir, filename=video.title)
        
        

def main():
    if args.dest:
        create_dir(dest_dir)
    if args.link:
        if args.type == "playlist":
            download_playlist()
        elif args.type == "video":
            download_video()
        else:
            print("Please provide a link type")
    else:   
        with open(links_path, 'r') as links:
            for link in links:
                download_playlist(link)

if __name__ == "__main__":
    main()
