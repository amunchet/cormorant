#!/usr/bin/env python3
"""
Cormorant Main program
"""
import os
import spectrogram
import youtube_dl

DOWNLOAD_DIR="./playlists"

def read_playlists(fname="playlists.txt"):
    """Reads in the Playlists"""
    with open(fname) as f:
        return f.readlines()


def download_urls(url):
    """
    Downloads a given url
        - Will download all items in a given playlist
    """

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False, 
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # TODO: Move anything downloaded to timestamped directory

    # TODO: Make a file with the original URL in it too - url.txt
    
def generate_spectrograms():
    """TODO: Generates spectrograms for the given downloaded WAVs"""

def cleanup():
    """TODO: Removes any webm, png files"""

