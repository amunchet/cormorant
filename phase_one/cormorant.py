#!/usr/bin/env python3
"""
Cormorant Main program
"""

import spectrogram
import youtube_dl


def read_playlists(fname="playlists.txt"):
    """Reads in the Playlists"""
    with open(fname) as f:
        return f.readlines()


def parse_playlist(url):
	"""Parses out the playlist from the url"""
	ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

	with ydl:
		result = ydl.extract_info(
			url,
			download=False # We just want to extract the info
		)

	if 'entries' in result:
		# Can be a playlist or a list of videos
		video = result['entries'][0]
	else:
		# Just a video
		video = result

	print(video)
	video_url = video['url']
	print(video_url) 
