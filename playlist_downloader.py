from pytube import YouTube
import argparse

def generate_local_video_downloader(destination_folder):
	
	def download_video(url):
		try:
    		YouTube(url).streams.first().download(destination_folder)
        		print("Done URL: {}".format(url))
    	except Exception as error:
        	print(error)
    
    return download_video


def main():
    args = parser.parse_args()
    video_downloader = generate_local_video_downloader(args.destination_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download every video from the wanted playlist in the best quality store them in the destination folder')
    parser.add_argument('-p', '--playlist_url', dest='playlist_url', help='the playlist\'s url')
    parser.add_argument('-d', '--destination_folder', dest='destination_folder', help='the videos will be saved in this folder')
    main()