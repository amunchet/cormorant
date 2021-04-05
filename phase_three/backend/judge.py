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
        output = learn.predict(image_path)
        print(output)
        output = output[0]
    except Exception:
        print("ERROR")
        print(sys.exc_info()[1])
        return -1
    return output == 'yes'

def train(epochs=5):
    """Trains and returns a model"""
    DIR = "/src/data/training"
    DATASET_PATH = Path(DIR)
    size = 512
    bs = 8

    datablock = DataBlock(
        get_items=get_image_files,
        get_y=parent_label,
        blocks=(ImageBlock, CategoryBlock),
        item_tfms=Resize(700),
        batch_tfms=aug_transforms(size=700, min_scale=0.85),
        splitter=RandomSplitter(valid_pct=0.2, seed=100)
    )
    dls = datablock.dataloaders(DATASET_PATH, bs=bs, size=size)
    learn = load_learner("/src/data/models/current.pkl")
    learn.dls = dls

    learn.fine_tune(epochs)

    return learn