#!/usr/bin/env python3
"""
Cormorant Main program
"""
import os
import spectrogram
import youtube_dl



def download_url(url): # pragma: no cover
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



