#!/usr/bin/env python3
"""
Reads in the genres CSV file and creates folders/moves files based on results
"""
import os
import sys
import shutil
import csv
import re

def load_genres(genres_csv:str):
    """Loads in the genres CSV"""
    with open(genres_csv) as f:
        return [(x[0],x[3]) for x in [y.split(",") for y in f.readlines()]][1:]


def parse_track_list(filename, genres_inp):
    """Reads in the CSV file and returns an array of the genres to id mapping"""
    genres = {}
    arr = {}

    for genre in genres_inp:
        genres[int(genre[0])] = genre[1]

    def parse(inp):
        try:
            return [genres[int(x.strip())] for x in inp.replace("[", "").replace("]", "").split(",")]
        except:
            # print("Problem occurred with ", inp, " : ", sys.exc_info()[1])
            return []

    with open(filename) as f:
        a = csv.reader(f)
        for line in a:
            (id,top_genre,best_genre, genres_all) = (line[0], line[-13], parse(line[-12]), parse(line[-11]))
            
            combined = [top_genre] + best_genre + genres_all
            for item in combined:
                if item != '' and item != "":
                    combined = item
                    break
            arr[id] = combined
    return arr

def list_files(directory:str, tracklist:{}):
    """Lists files in a given folder and what genre they belong to"""
    return [(directory + "/" + x, tracklist[str(int(x.replace(".mp3.png", "")))]) for x in os.listdir(directory) if ".mp3.png" in x]
    


def copy_file(pairs, directory:str):
    """
    Inputs:
        :pairs - Array of tuples in format (path, genre)
        :directory - location to place sorted images

    Moves the file to the correct folder location if it exists.
    Also creates folder if it doesn't exist.
    """
    
    for (path, raw_genre) in pairs:
        try:
            genre = re.sub(r'\W+', '', raw_genre)
        except Exception:
            print("Uncategorized found")
            genre = "Uncategorized"
        print("Path:", path, " and genre:", genre)
        if type(genre) != type(""): # Problem where empty list indicates no genre
            continue
        if not os.path.exists(directory + "/" + genre):
            os.mkdir(directory + "/" + genre)

        shutil.copy(path, directory + "/" + genre)


if __name__ == "__main__":
    genres = load_genres("/mnt/sdf/genres.csv")
    # arr = parse_track_list("/mnt/sdf/head.csv", genres)
    tracklist = parse_track_list("/mnt/sdf/tracks.csv", genres)

    # listing = list_files("/mnt/sdf/fma_large/000", tracklist)
    #copy_file(listing, "/mnt/sdf/data")
    
    for i in range(0,156):
        print("Starting for ", i)
        listing = list_files("""/mnt/sdf/fma_large/{}""".format(str(i).zfill(3)), tracklist)
        copy_file(listing, "/mnt/sdf/data")
    
    print("All done.")

