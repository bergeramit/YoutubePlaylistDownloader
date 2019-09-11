'''
download videos from a youtube playlist
'''
import errno
import argparse
import os
import sys

from urllib.parse import urljoin
import requests_html
import requests
import pytube
from bs4 import BeautifulSoup

VIDEO_LINK_CLASS = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
VIDEO_TAG = "ytd-playlist-video-renderer"
VIDEO_TITLE_ID = "video-title"


def generate_local_video_downloader(destination_folder):
    '''
    retrieves a downloader that saves files locally to a destination folder
    '''
    def download_video(video_url):
        try:
            pytube.YouTube(video_url).streams.first().download(destination_folder)
        except pytube.exceptions.PytubeError as error:
            print("Pytube library error: {}".format(error))
            print("Can't get a Youtube Handler")

    return download_video


def download_videos(videos, local_downloader):
    '''
    download youtube videos from urls
    :param videos - dict of url and title
    :param local_downloader - function that downloads the vids locally
    '''
    for i, video in enumerate(videos):
        local_downloader(video['url'])
        sys.stdout.flush()
        sys.stdout.write("\r")
        print("Downloaded => {}".format(video['title']))
        print_progress(i, len(videos))


class YoutubePlaylist:
    '''
    youtube playlist class one can download videos from that playlist
    '''
    def __init__(self, url):
        self.url = url
        self.handler = get_js_rendered_html_handler(url)
        self.title = self.handler.title.contents[0]
        self.videos_in_playlist = []


    def extract_videos_from_playlist(self):
        '''
        get all of the video's url and title
        '''
        try:
            playlist_video_struct = self.handler.findAll(VIDEO_TAG)
            html_video_objects = [video.find("a", attrs={'class': VIDEO_LINK_CLASS}) for video in playlist_video_struct]

            for html_video_object in html_video_objects:
                full_url = urljoin("https://www.youtube.com", html_video_object.attrs['href'])
                video_title = html_video_object.find("span", attrs={'id': VIDEO_TITLE_ID}).contents[0].strip()
                self.videos_in_playlist.append({'title': video_title, 'url': full_url})
        except AttributeError:
            raise ValueError("Could not fetch the videos in playlist. Check the playlist link again")


    def download_playlist(self, destination_folder, start_index=None, end_index=None):
        local_downloader = generate_local_video_downloader(destination_folder)
        self.extract_videos_from_playlist()
        print("-- {} --".format(self.title))
        print("-- Begin Downloading playlist --")
        download_videos(self.videos_in_playlist[slice(start_index, end_index, 1)], local_downloader)


def get_js_rendered_html_handler(url):
    '''
    get the rendered html version of the site -
    includes the modifications JS makes dynamically
    '''
    try:
        session = requests_html.HTMLSession()
        raw_html = session.get(url)
        raw_html.html.render()
        return BeautifulSoup(raw_html.html.html, 'html.parser')
    except requests.exceptions.ConnectionError:
        raise ValueError("Can't open playlist URL. Please check the URL again")


def print_progress(current_value, total_value):
    '''
    print the progress of the task
    '''
    precent_done = 100 * float(current_value + 1) / total_value
    sys.stdout.flush()
    sys.stdout.write("Completed: {}% ({} out of {})".format(precent_done,
                                                            current_value + 1,
                                                            total_value))


def main():
    args = PARSER.parse_args()
    try:
        os.mkdir(args.destination_folder)
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

    playlist = YoutubePlaylist(args.playlist_url)
    playlist.download_playlist(args.destination_folder,
                               args.start_index,
                               args.end_index)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='Download every video from the wanted playlist \
                                     in the best quality store them in the destination folder')
    PARSER.add_argument('-p',
                        '--playlist_url',
                        required=True,
                        dest='playlist_url',
                        help='the playlist\'s url')
    PARSER.add_argument('-d',
                        '--destination_folder',
                        required=True,
                        dest='destination_folder',
                        help='the videos will be saved in this folder')
    PARSER.add_argument('-f',
                        '--start_index',
                        type=int,
                        dest='start_index',
                        help='from video at index')
    PARSER.add_argument('-t',
                        '--end_index',
                        type=int,
                        dest='end_index',
                        help='to video at index')
    main()
