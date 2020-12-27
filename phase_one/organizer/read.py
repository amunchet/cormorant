#!/usr/bin/env python3
"""
Reads in the genres CSV file and creates folders/moves files based on results
"""
import sys
import csv

def test(filename, genres_inp):
    genres = {}
    for genre in genres_inp:
        genres[int(genre[0])] = genre[1]

    def parse(inp):
        try:
            return [genres[int(x.strip())] for x in inp.replace("[", "").replace("]", "").split(",")]
        except:
            print("Problem occurred with ", inp, " : ", sys.exc_info()[1])
            return []

    with open(filename) as f:
        a = csv.reader(f)
        for line in a:
            (id,top_genre,best_genre, genres_all) = (line[0], line[-13], parse(line[-12]), parse(line[-11]))
            
            combined = [top_genre] + best_genre + genres_all
            for item in combined:
                if item != "":
                    combined = item
                    break
            print(id, combined)
            



def load_genres(genres_csv:str):
    """Loads in the genres CSV"""
    with open(genres_csv) as f:
        return [(x[0],x[3]) for x in [y.split(",") for y in f.readlines()]][1:]



if __name__ == "__main__":

    genres = load_genres("/mnt/sdf/genres.csv")
    arr = test("/mnt/sdf/head.csv", genres)

    print("-------------")

    print(arr)
    print(len(arr))
