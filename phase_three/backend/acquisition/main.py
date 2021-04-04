#!/usr/bin/env python3
"""Full conversion and cleanup from mp3 to spectrogram"""
import os
import sys

try:
    import spectrogram
except ModuleNotFoundError:
    from acquisition import spectrogram

try:
    import convert
except ModuleNotFoundError:
    from acquisition import convert
try:
    import get
except ModuleNotFoundError:
    from acquisition import get 


DOWNLOAD_PATH ="/src/data/incoming/"

def main(youtube_id): # pragma: no cover
    """
    Downloads and converts given youtube_id
    """

    try:
        print("Starting for", youtube_id)
        print("Downloading...")
        get.download_url(youtube_id)

        print("Rename to id only")
        os.system("""mv *-{}.* {}.mp3""".format(youtube_id, youtube_id))

        print("Converting to wav...")
        convert.run_ffmpeg(youtube_id + ".mp3")

        print("Generating spectrogram...")
        spectrogram.plotstft(youtube_id + ".mp3", plotpath= youtube_id + ".png")

        print("Deleting mp3 and wav file...")
        os.system("rm *" + youtube_id + ".mp3 || true")
        os.system("rm *" + youtube_id + ".wav || true")

        print("Moving file...")
        os.system("""mv {}.png {}""".format(youtube_id, DOWNLOAD_PATH))

    except Exception:
        print("Had a problem: ", sys.exc_info()[1])
        
    print("Done.")
