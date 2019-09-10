import urllib.request
import argparse
import os
import sys
import math

from requests_html import HTMLSession
from pytube import YouTube
from bs4 import BeautifulSoup

VIDEO_LINK_CLASS = "yt-simple-endpoint style-scope ytd-playlist-video-renderer"
VIDEO_TAG = "ytd-playlist-video-renderer"
VIDEO_TITLE_CLASS = "watch-title"


def get_js_rendered_html_handler(url):
	session = HTMLSession()
	raw_html = session.get(url)
	raw_html.html.render()
	return BeautifulSoup(raw_html.html.html, 'html.parser')


def get_video_urls_from_playlist(playlist_url):
	try:
		handler = get_js_rendered_html_handler(playlist_url)
		print("-- {} --".format(handler.title.contents[0]))
		playlist_video_struct = handler.findAll(VIDEO_TAG)
		return [vid.find("a", attrs={'class': VIDEO_LINK_CLASS}).attrs['href'] for vid in playlist_video_struct]

	except:
		print("Can't open playlist URL. Please check the URL again")


def generate_local_video_downloader(destination_folder):
	def download_video(video_url):
		try:
			YouTube(video_url).streams.first().download(destination_folder)
		except:
			print("Can't get a Youtube Handler")

	return download_video


def print_progress(current_downloaded, index, total_length):
	sys.stdout.flush()
	sys.stdout.write("\r")
	print("Downloaded: {}".format(current_downloaded))
	precent_done = 100 * float(index + 1) / total_length
	sys.stdout.flush()
	sys.stdout.write("Completed: {}% ({} out of {})".format(precent_done, index + 1, total_length))


def retrieve_title(complete_url):
	handler = BeautifulSoup(urllib.request.urlopen(complete_url), 'html.parser')
	title = handler.find(attrs={'class': VIDEO_TITLE_CLASS})
	return title.contents[0].strip()


def download_playlist(playlist_url, destination_folder, start_index, end_index):
	video_downloader = generate_local_video_downloader(destination_folder)
	urls = get_video_urls_from_playlist(playlist_url)
	print("-- Begin Downloading playlist --")

	if end_index is not None:
		urls = urls[:end_index]
	if start_index is not None:
		urls = urls[start_index:]

	for i in range(len(urls)):
		complete_url = "".join(["https://www.youtube.com", urls[i]])
		video_downloader(complete_url)
		print_progress(retrieve_title(complete_url), i, len(urls))


def main():
    args = parser.parse_args()
    try:
    	os.system("mkdir {}".format(args.destination_folder))
    except:
    	pass

    download_playlist(args.playlist_url,
    				  args.destination_folder,
    				  args.start_index,
    				  args.end_index)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download every video from the wanted playlist in the best quality store them in the destination folder')
    parser.add_argument('-p', '--playlist_url', dest='playlist_url', help='the playlist\'s url')
    parser.add_argument('-d', '--destination_folder', dest='destination_folder', help='the videos will be saved in this folder')
    parser.add_argument('-f', '--start_index', dest='start_index', help='from video at index')
    parser.add_argument('-t', '--end_index', dest='end_index', help='to video at index')
    main()