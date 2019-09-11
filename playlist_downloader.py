'''
download videos from a youtube playlist
'''
import argparse
import os
import sys

from requests_html import HTMLSession
from pytube import YouTube
from bs4 import BeautifulSoup

VIDEO_LINK_CLASS = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
VIDEO_TAG = "ytd-playlist-video-renderer"
VIDEO_TITLE_ID = "video-title"


class YoutubePlaylist:
    '''
    youtube playlist class one can download videos from that playlist
    '''
    def __init__(self, url):
        self.url = url
        self.handler = get_js_rendered_html_handler(url)
        self.title = self.handler.title.contents[0]
        self.videos_in_playlist = []
        self.extract_videos_from_playlist()


    def generate_local_video_downloader(self, destination_folder):
        '''
        retrieves a downloader that saves files locally to a destination folder
        '''
        def download_video(video_url):
            try:
                YouTube(video_url).streams.first().download(destination_folder)
            except:
                print("Can't get a Youtube Handler")

        return download_video


    def extract_videos_from_playlist(self):
        '''
        get all of the video's url and title
        '''
        try:
            playlist_video_struct = self.handler.findAll(VIDEO_TAG)
            html_video_objects = [video.find("a", attrs={'class': VIDEO_LINK_CLASS}) for video in playlist_video_struct]

        except:
            print("Can't open playlist URL. Please check the URL again")

        for html_video_object in html_video_objects:
            full_url = "".join(["https://www.youtube.com", html_video_object.attrs['href']])
            video_title = html_video_object.find("span", attrs={'id': VIDEO_TITLE_ID}).contents[0].strip()
            self.videos_in_playlist.append({'title': video_title, 'url': full_url})


    def download_playlist(self, destination_folder, start_index=None, end_index=None):
        video_downloader = self.generate_local_video_downloader(destination_folder)
        print("-- {} --".format(self.title))
        print("-- Begin Downloading playlist --")
        download_videos(self.videos_in_playlist[slice(start_index, end_index, 1)], video_downloader)


def get_js_rendered_html_handler(url):
    '''
    get the rendered html version of the site -
    includes the modifications JS makes dynamically
    '''
    try:
        session = HTMLSession()
        raw_html = session.get(url)
        raw_html.html.render()
        return BeautifulSoup(raw_html.html.html, 'html.parser')
    except:
        print("Can't open playlist URL. Please check the URL again")


def print_progress(current_downloaded, index, total_length):
    '''
    print the progress of the task
    '''
    sys.stdout.flush()
    sys.stdout.write("\r")
    print("Downloaded: {}".format(current_downloaded))
    precent_done = 100 * float(index + 1) / total_length
    sys.stdout.flush()
    sys.stdout.write("Completed: {}% ({} out of {})".format(precent_done, index + 1, total_length))


def download_videos(videos, downloader):
    for i, video in enumerate(videos):
        downloader(video['url'])
        print_progress(video['title'], i, len(videos))





def main():
    args = parser.parse_args()
    try:
        os.mkdir(args.destination_folder)
    except:
        pass

    playlist = YoutubePlaylist(args.playlist_url)
    playlist.download_playlist(args.destination_folder,
                               args.start_index,
                               args.end_index)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download every video from the wanted playlist in the best quality store them in the destination folder')
    parser.add_argument('-p', '--playlist_url', required=True, dest='playlist_url', help='the playlist\'s url')
    parser.add_argument('-d', '--destination_folder', required=True, dest='destination_folder', help='the videos will be saved in this folder')
    parser.add_argument('-f', '--start_index', type=int, dest='start_index', help='from video at index')
    parser.add_argument('-t', '--end_index', type=int, dest='end_index', help='to video at index')
    main()
