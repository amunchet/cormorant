#!/usr/bin/env python3
"""
Determination using the model of whether a song is 'yes' or 'no'
"""
import sys
from fastai.imports import *
from fastai.vision import *
from fastai.vision.all import *
from fastai.metrics import accuracy


def judge(image_path, model_path) -> bool:
    """Judges a Path according to the given model"""
    learn = load_learner(model_path)
    try:
        output = learn.predict(image_path)[0]
    except Exception:
        print("ERROR")
        print(sys.exc_info()[1])
        return -1
    
    return output == 'yes'

