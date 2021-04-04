#!/usr/bin/env python3
"""
Tests for Cormorant Service
"""

import pytest
import serve
import json

songs = [
    { # Parent 1
        "title" : "Rival - Thorne - (ft. Neoni) [NCS Release]",
        "youtube_link" : "midpbHJ4EIk",
        "generation" : 0,
        "parents" : [], 
        "children": ["WgdhRxxXQDk"], 
        "manual_judgement" : 1, 
        "predicted_judgement" : 1,
    },
    { # Parent 2
        "title" : "Mendum & Abandoned - Voyage (Feat. DNAKM) [NCS Release]",
        "youtube_link" : "uzwUNS0IjC8",
        "generation" : 0,
        "parents" : [], 
        "children": ["WgdhRxxXQDk"],
        "manual_judgement" : 0,
        "predicted_judgement" : 1,
    },
    { # Child of Both
        "title" : "Kozah - Cali4nia [NCS Release]",
        "youtube_link" : "WgdhRxxXQDk",
        "generation" : 1,
        "parents" : ["uzwUNS0IjC8", "midpbHJ4EIk"], 
        "children": ["dWOj02nPyxk"], 
    },
    { # Child of One
        "title" : "Abandoned - Out Of The Grave (Feat. ENROSA) [NCS Release]",
        "youtube_link" : "dWOj02nPyxk",
        "generation" : 2,
        "parents" : ["WgdhRxxXQDk"], 
        "children": [], 
        "predicted_judgement" : 1,
        "manual_judgement" : 1,
    },
]

def tearDown():
    """Removes all entries in the Mongo"""
    for item in [x["youtube_link"] for x in songs]:
        serve.mongo_client["cormorant"]["songs"].delete_one({"youtube_link" : item })


    serve.mongo_client["cormorant"]["stats"].delete_many({})

@pytest.fixture
def client():
    tearDown()

    
    stats = {
        "pointer" : "", # Youtube ID
        "manual_rejected" : 0, # Counted at the time of the manul judgement action
        "manual_accepted" : 0,
        "automatic_rejected" : 0, # This will also only be counted at the time of manual judgement, then never again
        "automatic_accepted" : 0,
        "model_accuracy" : 0, # How often do we agree?
        "total_judged" : 0, # How many have we judged?
    }

    for item in songs:
        serve.mongo_client["cormorant"]["songs"].insert_one(item)
    
    serve.mongo_client["cormorant"]["stats"].insert_one(stats)

    serve.app.config['TESTING'] = True
    with serve.app.test_client() as client:
        yield client

    tearDown()
    return "Done"

def test_serve_static(client):
    """Serves the static files"""
    a = client.get("/css/styles.css")
    assert a.data.decode("utf-8").split() == open("/src/frontend/css/styles.css").read().split()


def test_generate_graph(client):
    """
    This is the JSON output for the graph visualization
    """

    elements = [
        {
            "data": {
                "id": 'midpbHJ4EIk',
                "name": "Rival - Thorne - (ft. Neoni) [NCS Release]"
            }
        },
        {
            "data": {
                "id": 'uzwUNS0IjC8',
                "name": "Mendum & Abandoned - Voyage (Feat. DNAKM) [NCS Release]"
            }
        },
        {
            "data": {
                "name": "Kozah - Cali4nia [NCS Release]",
                "id": "WgdhRxxXQDk"
            }
        },
        {
            "data": {
                "name": "Abandoned - Out Of The Grave (Feat. ENROSA) [NCS Release]",
                "id": "dWOj02nPyxk"
            }
        },
        {
            "data": {
                "id": 'uzwUNS0IjC8-WgdhRxxXQDk',
                "source": 'uzwUNS0IjC8',
                "target": 'WgdhRxxXQDk'
            }
        },
        {
            "data": {
                "id": 'midpbHJ4EIk-WgdhRxxXQDk',
                "source": 'midpbHJ4EIk',
                "target": 'WgdhRxxXQDk'
            }
        },
        {
            "data": {
                "id": "WgdhRxxXQDk-dWOj02nPyxk",
                "source": "WgdhRxxXQDk",
                "target": "dWOj02nPyxk"
            }
        }
    ]
    style = [
        {
            "selector" : 'node',
            "style" : {
                'label': 'data(name)',
                'background-fit': 'cover',
                'border-color': '#000',
                'border-width': 3,
                'border-opacity': 0.5
            }
        },
        {
            "selector" : 'edge',
            "style" : {
                'width': 3,
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
            }
        },
        {
            "selector": "#midpbHJ4EIk",
            "style": {
                'background-image': "/youtube/midpbHJ4EIk"
            },
        },
        {
            "selector": "#uzwUNS0IjC8",
            "style": {
                'background-image': "/youtube/uzwUNS0IjC8"
            },
        },
        {
            "selector": "#WgdhRxxXQDk",
            "style": {
                'background-image': "/youtube/WgdhRxxXQDk"
            },
        },
        {
            "selector": "#dWOj02nPyxk",
            "style": {
                'background-image': "/youtube/dWOj02nPyxk"
            }
        }
    ]
    a = client.get("/api/status")
    b = json.loads(a.data.decode("utf-8"))
    for item in elements:
        assert item in b[0]
    
    for item in style:
        assert item in b[1]
    
    # These won't work if there are other entries in the database

    # for item in b[0]:
    #    assert item in elements
    
    # for item in b[1]:
    #    assert item in style

def test_get_current_song(client):
    """
    Returns the current song to be judged, as determined by the pointer
    
    - If the pointer isn't defined, then set it to an item in the...newest generation?  

    {
        "youtube_link" : "",
        "title" : "",
        "predicted_judgement" : ""
    }
    """
    a = json.loads(client.get("/api/current_song").data.decode("utf-8"))
    assert "youtube_link" in a
    assert a["youtube_link"]

    assert "title" in a
    assert "predicted_judgement" in a

def test_manual_judge(client):
    """
    Tests manual judgement of a song (yes or no)
        - Need to make sure the files are moved properly
        - Yes goes to `yes`, no goes to `no_holding` since we are afraid of imbalance 
        - We also want to save the Youtube id to another database
    """
    link = "WgdhRxxXQDk"
    # Set and entry to `yes`

    # TODO: I also need parsed images

    a = serve.mongo_client["cormorant"]["songs"].find_one({"youtube_link" : link})
    assert "manual_judgement" not in a


    client.get("/api/judge/" + link + "/yes")

    a = serve.mongo_client["cormorant"]["songs"].find_one({"youtube_link" : link})

    assert "manual_judgement" in a
    assert a["manual_judgement"] == 1

    # TODO: Need to have file movement
    assert False


    # Set an entry to `no`

    client.get("/api/judge/" + link + "/no")
    a = serve.mongo_client["cormorant"]["songs"].find_one({"youtube_link" : link})

    assert "manual_judgement" in a
    assert a["manual_judgement"] == 0

    # TODO: I need to have file movement
    assert False

def test_list_current_generation():
    """
    Lists the current generation of songs
        - The original generation is going to be everyone without a parent
    """


def test_list_success():
    """
    Returns all songs found and judged yes - saved in a separate database
    """

def test_list_unjudged():
    """Returns list of unjudged songs"""

def test_list_no_children():
    """How many songs have no children?"""

def test_list_no_image():
    """How many songs have no spectrogram?"""

def test_list_last_training():
    """When was the model last updated?"""

def test_branches_needing_prune():
    """How many nodes are marked as dead that have not been deleted?"""

def test_historical_model_performance():
    """Return the data for historical model performance for the home page"""