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



@app.route("/version")
def version():
    return "0.0.1"

if __name__ == "__main__":  # pragma: no cover
    app.debug = True
    app.config["ENV"] = "development"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7000)))