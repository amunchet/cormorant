#!/usr/bin/env python3
"""
Tests for Cormorant Service
"""
import pytest

@pytest.fixture
def setup():
    yield "Setting Up"
    return "Done"

def test_serve_static():
    """Serves the static files"""

def test_list_songs():
    """Lists all songs"""

def test_list_related_songs():
    """Lists all songs related to a given song"""

def test_judge():
    """
    Tests judgement of a song (yes or no)
        - Need to make sure the files are moved properly and retrained
        - Training won't use GPU (since we aren't guaranteed to have it)
    """
