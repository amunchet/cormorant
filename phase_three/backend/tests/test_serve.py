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
        "manual_judgement" : 0,
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
        "predicted_judgement" : 1,
    },
    { # Child of One
        "title" : "Abandoned - Out Of The Grave (Feat. ENROSA) [NCS Release]",
        "youtube_link" : "dWOj02nPyxk",
        "generation" : 2,
        "parents" : ["WgdhRxxXQDk"], 
        "children": [], 
        "predicted_judgement" : 1,
    },
]

def teardown():
    """Removes all entries in the Mongo"""


@pytest.fixture
def client():
    teardown()

    
    stats = {
        "pointer" : "", # Youtube ID
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


def test_generate_graph():
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
                "id": 'WgdhRxxXQDk-uzwUNS0IjC8',
                "source": 'uzwUNS0IjC8',
                "target": 'WgdhRxxXQDk'
            }
        },
        {
            "data": {
                "id": 'WgdhRxxXQDk-midpbHJ4EIk',
                "source": 'midpbHJ4EIk',
                "target": 'WgdhRxxXQDk'
            }
        },
        {
            "data": {
                "id": "dWOj02nPyxk-WgdhRxxXQDk",
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