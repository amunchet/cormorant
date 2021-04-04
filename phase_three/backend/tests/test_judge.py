#!/usr/bin/env python3
"""
Tests the judgement (i.e. the application of the model) and a returned result

This will require loading in fastai - we probably need a version tag on it too
"""

import os
import judge

def test_model_exists():
    """Tests that the given model exists"""
    print("If this test fails, then `models/current.pkl` does not exist.  It is not included in the repository since it takes up too much space.")
    
    assert os.path.exists("/src/data/models/current.pkl")

def test_judge_song():
    """
    Tests judging a known song
        - Going to just pass in the raw image to judge.  Processing or acquisition are for other parts of the pipeline.
    """
    
    assert judge.judge("tests/yes.png", "/src/data/models/current.pkl")

    assert not judge.judge("tests/no.png", "/src/data/models/current.pkl")


    assert judge.judge("tests/test_cron.py", "/src/data/models/current.pkl") == -1