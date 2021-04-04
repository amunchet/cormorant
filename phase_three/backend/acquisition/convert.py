#!/usr/bin/env python3
"""
Converts Mp3 files to Wav - also repeats them a given number of times
"""
import os
import random
import sys

def run_ffmpeg(fname:str): # pragma: no cover
    """Runs the ffmpeg and copies the file a random number of times"""
    filename = fname
    if ".mp3" in fname:
        filename = filename.replace(".mp3", "")

    cmd = """ffmpeg  -nostats -loglevel 0 -t 00:05:00 -i {}.mp3 {}.wav""".format(fname, fname)
    os.system(cmd)
