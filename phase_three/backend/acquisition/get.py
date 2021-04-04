#!/usr/bin/env python3
"""
Cormorant Main program
"""
import os

from subprocess import Popen, PIPE
from threading import Timer

import youtube_dl

from functools import wraps
import errno
import os
import signal


class TimeoutError(Exception):  # pragma: no cover
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):  # pragma: no cover
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout(60)
def download_url(url):  # pragma: no cover
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
            '-ar', '16000', '-t', '00:05:00'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
