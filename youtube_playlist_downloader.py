'''
youtube playlist downloader
Author: Amit Berger
'''
import sys

from urllib.parse import urljoin
import requests_html
import requests
import pytube
from bs4 import BeautifulSoup


VIDEO_LINK_CLASS = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
VIDEO_TAG = "ytd-playlist-video-renderer"
VIDEO_TITLE_ID = "video-title"


def _extract_video_title(video):
    '''
    extract the title from the html object
    '''
    return video.find("span", attrs={'id': VIDEO_TITLE_ID}).contents[0].strip()


def _get_rendered_html_handler(url):
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


def _print_progress(current_value, total_value):
    '''
    print the progress of the task
    '''
    precent_done = 100 * float(current_value + 1) / total_value
    sys.stdout.flush()
    sys.stdout.write("Completed: {}% ({} out of {})".format(precent_done,
                                                            current_value + 1,
                                                            total_value))


class YoutubePlaylist:
    '''
    youtube playlist class one can download videos from that playlist
    '''
    def __init__(self, url):
        self.url = url
        self.handler = _get_rendered_html_handler(url)
        self.title = self.handler.title.contents[0]


    def _extract_html_video_structs(self):
        '''
        extract the list of the videos URLs from the htmk object
        '''
        playlist_video_struct = self.handler.findAll(VIDEO_TAG)
        return [video.find("a", attrs={'class': VIDEO_LINK_CLASS}) for video in playlist_video_struct]


    def get_videos_in_playlist(self, start_index, end_index):
        '''
        get all of the video's urls and titles from the playlist
        '''

        videos = []
        try:
            html_video_structs = self._extract_html_video_structs()

        except AttributeError:
            raise ValueError("Could not fetch the videos in playlist. Check the link again")

        for video in html_video_structs:
            full_url = urljoin("https://www.youtube.com", video.attrs['href'])
            title = _extract_video_title(video)
            videos.append({'title': title, 'url': full_url})

        return videos[slice(start_index, end_index, 1)]


    def download(self, destination_folder, start_index=None, end_index=None):
        '''
        Download a full youtube playlist
        '''
        videos = self.get_videos_in_playlist(start_index, end_index)
        print("-- {} --".format(self.title))
        print("Begin Downloading playlist")

        try:
            for i, video in enumerate(videos):
                pytube.YouTube(video['url']).streams.first().download(destination_folder)
                sys.stdout.flush()
                sys.stdout.write("\r")
                print("Downloaded => {}".format(video['title']))
                _print_progress(i, len(videos))

        except pytube.exceptions.PytubeError as error:
            print("Pytube library error: {}".format(error))
            print("Can't download the video")
