#!/usr/bin/env python3
"""Full conversion and cleanup from mp3 to spectrogram"""
import os
import spectrogram
import convert
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("usage: [FOLDER to convert]")
        sys.exit(0)
    filelist = [x for x in sorted(os.listdir(sys.argv[1])) if x[-4:] == ".mp3" ]
    existing = [x for x in sorted(os.listdir(sys.argv[1])) if x[-4:] == ".png" ]

    for filename in [x for x in filelist if x+".png" not in existing]:
        try:
            print("Starting for", filename)

            print("Converting to wav...")
            convert.run_ffmpeg(filename.split("/")[-1], sys.argv[1])

            print("Generating spectrogram...")
            spectrogram.plotstft(sys.argv[1] + "/" + filename.replace(".mp3", ".wav"), plotpath=sys.argv[1] + "/" + filename + ".png")

            print("Deleting wav file...")
            os.remove(sys.argv[1] + "/" + filename.replace(".mp3", ".wav"))
        except Exception:
            print("Had a problem: ", sys.exc_info()[1])
        
    print("Done.")
