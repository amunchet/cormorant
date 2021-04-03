#!/usr/bin/env python3
"""
Tests acquisition of an image given a youtube url
    - This is carry over from phase_1
"""

def test_acquire():
    url = ""
    assert acquire.get(url)

    # Open the image file and compare it to.  Make sure the filename matches the URL
