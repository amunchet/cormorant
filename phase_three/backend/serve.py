#!/usr/bin/env python3
"""
Basic Flask service for backend functions 
"""

import functools
import os
import datetime

from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS


from werkzeug.utils import secure_filename
import uuid
import json


from dotenv import load_dotenv

import pymongo
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app)


# Load dot-env


load_dotenv(verbose=True)

if os.environ.get("MONGO_USERNAME") == "":
    os.environ["MONGO_USERNAME"] = "root"
if os.environ.get("MONGO_PASSWORD") == "":
    os.environ["MONGO_PASSWORD"] = "temp"
if os.environ.get("MONGO_HOST") == "":
    os.environ["MONGO_HOST"] = "mongo"


# Mongo Access
mongo_client = pymongo.MongoClient(
    "mongodb://{}:{}@{}:27017".format(
        os.environ.get("MONGO_USERNAME"),
        os.environ.get("MONGO_PASSWORD"),
        os.environ.get("MONGO_HOST"),
    )
)


@app.route("/images/<path:path>")
def static_serve_image(path):
    return send_from_directory('/src/frontend/images/',path)

@app.route("/css/<path:path>")
def static_serve_css(path):
    return send_from_directory('/src/frontend/css/',path)


@app.route("/<path:path>")
def static_serve_html(path):
    return send_from_directory('/src/frontend/html/',path)




@app.route("/version")
def version():
    return "0.0.1"

if __name__ == "__main__":  # pragma: no cover
    app.debug = True
    app.config["ENV"] = "development"
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7000)))