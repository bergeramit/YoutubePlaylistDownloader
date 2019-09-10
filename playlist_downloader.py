import urllib.request
import argparse

from pytube import YouTube
from bs4 import BeautifulSoup


def get_next_video_in_playlist(playlist_url):
	try:
		playlist_page = urllib.request.urlopen(playlist_url)
	except:
		print("Cant open playlist URL. please check the URL again")

	playlist_parsed = BeautifulSoup(playlist_page, 'html.parser')
	print("Begin Downloading playlist: {}".format(playlist_parsed.title.contents[0]))


def generate_local_video_downloader(destination_folder):
	def download_video(video_url):
		try:
			YouTube(video_url).streams.first().download(destination_folder)
			print("Done URL: {}".format(video_url))
		except Exception as error:
			print(error)

	return download_video


def main():
    args = parser.parse_args()
    video_downloader = generate_local_video_downloader(args.destination_folder)
    get_next_video_in_playlist(args.playlist_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download every video from the wanted playlist in the best quality store them in the destination folder')
    parser.add_argument('-p', '--playlist_url', dest='playlist_url', help='the playlist\'s url')
    parser.add_argument('-d', '--destination_folder', dest='destination_folder', help='the videos will be saved in this folder')
    main()