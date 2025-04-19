from pytube import Playlist, YouTube
from urllib import error
import os
import argparse
import re
import sys

parser = argparse.ArgumentParser(description="Download videos/playlists from YouTube")
# parser.add_argument("--type", type=str, help="is it a single video or a playlist?")
parser.add_argument("--link", type=str, help="link of a playlist/video")
parser.add_argument("--links_file", type=str,
    help="location of a file with videos/pleylists links")
parser.add_argument("--start_with", type=int, 
    help="position of a video in the playlist to start downloading from")
parser.add_argument("--nth_video", type=int, 
    help="download single video from a playlist")    
parser.add_argument("--dest", type=str, 
    help="destination path where videos will be saved")
parser.add_argument("--audio", type=bool,
    help="download audio file")
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
    playlist_title = "-".join(playlist.title.split("/"))
    current_playlist_path = f'{dest_dir}/{playlist_title}'
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


def download_audio():
    try:
        video = YouTube(args.link)
        video.streams.get_audio_only().download(output_path=dest_dir, filename=video.title)
    except KeyError:
        print('KeyError')
        errors += 1
        if errors == 10:
            return
        else:
            download_audio()
    except Exception as err:
        print(f"General error!\n{err}")
        

def main():
    if args.dest:
        create_dir(dest_dir)
    if args.link:
        if args.audio:
            download_audio()
        elif "watch" in args.link:
            link_type = "video"
        elif "list" in args.link:
            link_type = "playlist"
        else:
            print("Please provide a valid youtube link")
            return
        
        # if link_type == "playlist":
        #     download_playlist()
        # else:
        #     download_video()
    else:   
        with open(links_path, 'r') as links:
            for link in links:
                download_playlist(link)

if __name__ == "__main__":
    main()
