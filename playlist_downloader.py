import urllib.request
import argparse

from requests_html import HTMLSession
from pytube import YouTube
from bs4 import BeautifulSoup

VIDEO_LINK_CLASS = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
VIDEO_TAG = "ytd-playlist-video-renderer"


def get_video_urls_from_playlist(playlist_url):
	try:
		session = HTMLSession()
		raw_html = session.get(playlist_url)
		raw_html.html.render()
		handler = BeautifulSoup(raw_html.html.html, 'html.parser')
		print("-- {} --".format(self.handler.title.contents[0]))
		playlist_video_struct = handler.findAll(VIDEO_TAG)
		return [vid.find("a", attrs={'class': VIDEO_LINK_CLASS}).attrs['href'] for vid in playlist_video_struct]

	except:
		print("Can't open playlist URL. please check the URL again")


def generate_local_video_downloader(destination_folder):
	def download_video(video_url):
		try:
			YouTube(video_url).streams.first().download(destination_folder)
			print("-- Downloaded URL: {} --".format(video_url))
		except Exception as error:
			print(error)

	return download_video


def download_playlist(playlist_url, destination_folder, start_index, end_index):
	video_downloader = generate_local_video_downloader(destination_folder)
	urls = get_video_urls_from_playlist(playlist_url)
	print("-- Begin Downloading playlist --")

	if end_index is not None:
		urls = urls[:end_index]
	if start_index is not None:
		urls = urls[start_index:]

	for video_url in urls:
		video_downloader("".join(["https://www.youtube.com", video_url]))


def main():
    args = parser.parse_args()
    download_playlist(args.playlist_url, args.destination_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download every video from the wanted playlist in the best quality store them in the destination folder')
    parser.add_argument('-p', '--playlist_url', dest='playlist_url', help='the playlist\'s url')
    parser.add_argument('-d', '--destination_folder', dest='destination_folder', help='the videos will be saved in this folder')
    parser.add_argument('-f', '--from_video', dest='from_video', help='the playlist\'s url')
    parser.add_argument('-t', '--to_video', dest='to_video', help='the playlist\'s url')
    main()