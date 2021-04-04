#!/usr/bin/env python3
"""
Basic Flask service for backend functions 
"""

import functools
import os
import datetime

from flask import Flask, request, send_file, send_from_directory, render_template, Response
from flask_cors import CORS


from werkzeug.utils import secure_filename
import uuid
import json


from dotenv import load_dotenv

import pymongo
import requests
from bson.objectid import ObjectId


app = Flask(__name__, template_folder="/src/frontend/html")
CORS(app)


# Load dot-env


load_dotenv(verbose=True)



# Mongo Access
mongo_client = pymongo.MongoClient(
    "mongodb://{}:{}@{}:27017".format(
        os.environ.get("MONGO_USERNAME"),
        os.environ.get("MONGO_PASSWORD"),
        os.environ.get("MONGO_HOST"),
    )
)

MENU = [
    "home",
    "judge",
    "status",
    "playlist",
    "settings"
]

@app.route("/")
@app.route("/<path>")
def serve_index(path=""):
    """Serves the index"""

    if path == "":
        return render_template("home.html", active="home", menu=MENU)
    else:
        if path.isalpha():
            return render_template(path + ".html", active=path, menu=MENU)
        return "Invalid information", 407

@app.route("/favicon.ico")
def favicon():
    return send_file("/src/frontend/favicon.ico")


@app.route("/images/<path:path>")
def static_serve_image(path):
    return send_from_directory('/src/frontend/images/',path)

@app.route("/css/<path:path>")
def static_serve_css(path):
    return send_from_directory('/src/frontend/css/',path)


@app.route("/youtube/<path>")
def youtube_thumbnail(path):
    url = """https://img.youtube.com/vi/{}/hqdefault.jpg""".format(path)
    return Response(requests.get(url), mimetype="image/jpeg")

@app.route("/api/status")
def graph_stats():
    """Returns Graph stats"""
    all_songs = [x for x in mongo_client["cormorant"]["songs"].find({})]

    elements = []
    style = []

    # Elements - nodes
    temp_elements = []
    for item in all_songs:
        if item["youtube_link"] not in temp_elements:
            elements.append({
                "data" : {
                    "id" : item["youtube_link"],
                    "name" : item["title"]
                }
            })
            temp_elements.append(item["youtube_link"])
    

    # Elements - connections
    for item in all_songs:
        for child in item["children"]:
            elements.append({
                "data": {
                    "id" : item["youtube_link"] + "-" + child,
                    "source": item["youtube_link"],
                    "target": child
                }
            })

    # Style, static
    style.append(
        {
            "selector" : 'node',
            "style" : {
                'label': 'data(name)',
                'background-fit': 'cover',
                'border-color': '#000',
                'border-width': 3,
                'border-opacity': 0.5
            }
        }
    )
    style.append(
        {
            "selector" : 'edge',
            "style" : {
                'width': 3,
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
            }
        })

    # Style, images
    for item in all_songs:
        style.append({
            "selector" : "#" + item["youtube_link"],
            "style" : {
                "background-image" : "/youtube/" + item["youtube_link"]
            }
        })

    return json.dumps([elements, style], default=str)

@app.route("/api/current_song")
def current_song():
    """Returns current song"""
    a = mongo_client["cormorant"]["songs"].find({"predicted_judgement" : {"$exists" : True}, "manual_judgement" : {"$exists" : True}})
    return json.dumps([
        {
            "youtube_link" : x["youtube_link"],
            "title" : x["title"],
            "predicted_judgement": x["predicted_judgement"]
        }
        for x in a
    ][0], default=str), 200

@app.route("/version")
def version():
    return "0.0.1"

if __name__ == "__main__":  # pragma: no cover
    app.debug = True
    app.config["ENV"] = "development"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7000)))