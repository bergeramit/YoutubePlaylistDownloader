'''
download youtube playlist
Author: Amit Berger
'''
import errno
import argparse
import os
import youtube_playlist_downloader


def main():
    args = PARSER.parse_args()
    try:
        os.mkdir(args.destination_folder)

    except OSError as error:
        if error.errno != errno.EEXIST:
            raise

    playlist = youtube_playlist_downloader.YoutubePlaylist(args.playlist_url)
    playlist.download(args.destination_folder,
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
