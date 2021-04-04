#!/usr/bin/env python3
"""
Handles Periodic Tasks for Cormorant
"""
from serve import mongo_client
import json
import spider

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