#!/usr/bin/env python
"""
Generator
"""
import random
import os
import subprocess
import sys

random.seed(1242)
VERBOSE = 1

def yield_random(length:int, count=10) -> []:
    """Generator function for random numbers"""
    i = 0
    seen = []

    while i < count:
        temp = int(random.random() * length)
        counter = 0
        while temp in seen:
            temp = int(random.random() * length)
            if len(seen) == length:
                raise Exception("Not enough values in length to handle random generation")
            counter += 1
        counters = 0
        seen.append(temp)
        yield temp
        i += 1

    temp = int(random.random() * length)
    counter = 0
    while temp in seen:
        temp = int(random.random() * length)
        if len(seen) == length:
            raise Exception("Not enough values in length to handle random generation")
        counter += 1

    return temp

def select_files(dir:str, count=10):
    """
    Selects the given files
    """
    retval = []
    files = [x for x in os.listdir(dir) if x[-4:] == ".wav"]

    b = yield_random(len(files), count=count)
    return [files[x] for x in b]

def combine(filelist:[], cmd="sox", output=""):
    """Combines given WAV files"""
    
    files = [x for x in filelist if x[-4:] == ".wav"]
    if output == "":
        output_name = str(abs(hash(tuple(files)))) + ".wav"
    else:
        output_name = output
    return subprocess.run([cmd] + files + [output_name, "splice", "-h", "2,1"], capture_output=True)

def check(filename, combination):
    """Checks if a given combination is in the filename"""
    if not os.path.exists(filename):
        return False

    with open(filename) as f:
        return str(combination) in f.read()

def update(filename, combination):
    """Updates the file with the combination"""
    with open(filename, "a+") as f:
        if str(combination) not in f.read():
            f.write(str(combination) + "\n")

def log(*args): # pragma: no cover
    """Logs the item"""
    if VERBOSE:
        print(*args)

def main(num_to_generate, directory=".", tracking_file="tracking.txt", file_size=100):
    """Main function to run and generate combined wav files"""
    for i in range(0,num_to_generate):
        log("Generating file #", i)
        combination  = [directory + "/" + x for x in select_files(directory, file_size)]
        log("Combination: ", combination)
        while check(tracking_file, combination):
            combination  = select_files(directory)
            log("Combination already existed...trying again")

        log("Combining...")
        log(combine(combination))
        log("Done, updating tracking file...")
        update(tracking_file, combination)

    log("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generator.py [number of combined wav files to generate] [directory]")
    else:
        main(int(sys.argv[1]), sys.argv[2])
