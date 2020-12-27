#!/usr/bin/env python3
"""
Converts Mp3 files to Wav - also repeats them a given number of times
"""
import os
import random

def run_ffmpeg(fname:str, directory:str):
    """Runs the ffmpeg and copies the file a random number of times"""
    filename = fname
    if ".mp3" in fname:
        filename = filename.replace(".mp3", "")

    repl = """"concat:"""

    for i in range(0, int((random.random() * 10) % 4)+1):
        repl += """/workspace/{}.mp3|""".format(filename)
    
    print("Repeated ", i, " times")

    repl += """/workspace/{}.mp3""".format(filename)
    
    repl += "\""

    print("Starting up program for ", fname)

    a = """docker run --rm --runtime=nvidia --volume {}:/workspace jrottenberg/ffmpeg:4.1-nvidia -nostats -loglevel 0 -hwaccel cuvid -i {} /workspace/{}.wav""".format(directory,repl, filename)
    print(a)
    os.system(a)
            
if __name__ == "__main__":
    for filename in [x for x in os.listdir(".") if ".mp3" in x]:
        print("Running for", filename)
        run_ffmpeg(filename)
                    



