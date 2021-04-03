#!/usr/bin/env python3
"""
Tests for Cormorant Service
"""

import pytest
import serve

def teardown():
    """Removes all entries in the Mongo"""


@pytest.fixture
def client():
    teardown()

    song_1 = {
        "title" : "Some title",
        "youtube_link" : "Some link",
        "thumbnail" : "Some link",
        "generation" : 0,
        "parents" : [], # These are the UUIDs
        "children": [], # These are the UUIDs
        "manual_judgement" : 0,
        "predicted_judgement" : 1,
    }
    song_2 = {
        "title" : "Some title",
        "youtube_link" : "Some link",
        "thumbnail" : "Some link",
        "generation" : 0,
        "parents" : [], # These are the UUIDs
        "children": [], # These are the UUIDs
        "manual_judgement" : 0,
        "predicted_judgement" : 1,
    }
    song_3 = {
        "title" : "Some title",
        "youtube_link" : "Some link",
        "thumbnail" : "Some link",
        "generation" : 0,
        "parents" : [], # These are the UUIDs
        "children": [], # These are the UUIDs
        "manual_judgement" : 0,
        "predicted_judgement" : 1,
    }

    stats = {
        "pointer" : "", # UUID - This will indicate the next song to judge.  It will also move up and down the generations as needed.
        "manual_rejected" : 0, # Counted at the time of the manul judgement action
        "manual_accepted" : 0,
        "automatic_rejected" : 0, # This will also only be counted at the time of manual judgement, then never again
        "automatic_accepted" : 0,
        "model_accuracy" : 0, # How often do we agree?
        "total_judged" : 0, # How many have we judged?
    }




    serve.app.config['TESTING'] = True
    with serve.app.test_client() as client:
        yield client

    teardown()
    return "Done"

def test_serve_static(client):
    """Serves the static files"""
    a = client.get("/css/styles.css")
    assert a.data.decode("utf-8").split() == open("/src/frontend/css/styles.css").read().split()


def test_list_related_songs():
    """
    Lists all songs related to a given song
        - This is going to be children
    """

def test_get_current_song():
    """
    Returns the current song to be judged, as determined by the pointer
    
    - If the pointer isn't defined, then set it to an item in the...newest generation?  

    """

def test_list_current_generation():
    """
    Lists the current generation of songs
        - The original generation is going to be everyone without a parent
    """

def test_manual_judge():
    """
    Tests manual judgement of a song (yes or no)
        - Need to make sure the files are moved properly and retrained
    """

def test_list_unjudged():
    """Returns list of unjudged songs"""