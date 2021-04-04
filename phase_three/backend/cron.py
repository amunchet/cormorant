#!/usr/bin/env python3
"""
Handles Periodic Tasks for Cormorant
"""
import os
import sys
import json
import datetime

import spider
import judge
from serve import mongo_client
from acquisition import main as ac


# Children Section

def list_judged_no_children():
    """Lists Judged entries without children"""
    a = mongo_client["cormorant"]["songs"].find({"manual_judgement" : 1, "children" : []})

    return [(x["youtube_link"], x["generation"]) for x in a]

def update_with_children(youtube_link, children):
    """Updates a given song with the children"""
    return mongo_client["cormorant"]["songs"].update_one({"youtube_link" : youtube_link}, {"$set" : {"children" : children}})

def insert_child(title, youtube_link, parent, generation):
    """Inserts a child into the database"""
    return mongo_client["cormorant"]["songs"].insert_one({
        "title" : title,
        "youtube_link" : youtube_link,
        "parents" : [parent],
        "children" : [],
        "generation" : int(generation) + 1
    })


def add_children(): # pragma: no cover
    """Finds and adds children to those judged without them"""
    a = list_judged_no_children()
    for (item, generation) in a:
        b = spider.load_related(item)
        update_with_children(item, [x[1] for x in b])
        for j in b:
            insert_child(title=j[0], youtube_link=j[1], parent=item, generation=generation)

# Images Section
def list_missing_images(count=5, directory="/src/data/incoming", models_directory="/src/data/models/"):
    """Returns list of missing images.  Default limit is 5"""

    # Need to list everything that hasn't been automatically judged yet
    a = [x["youtube_link"] for x in mongo_client["cormorant"]["songs"].find({"predicted_judgement" : {"$exists" : False }})][:count]


    for song in a:
        ac.main(song)

        judgement = judge.judge(directory + "/" + song + ".png", models_directory + "/" + "current.pkl")

        mongo_client["cormorant"]["songs"].update_one({"youtube_link": song}, {"$set" : {"predicted_judgement" : int(judgement)}})



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Needs an argument.")
        sys.exit(1)
    
    print(datetime.datetime.now())
    if sys.argv[1] == "images":
        print("Starting images...")
        list_missing_images()
        print("Image download completed.")
    
    elif sys.argv[1] == "children":
        print("Starting add children...")
        add_children()
        print("Children addition completed.")
    