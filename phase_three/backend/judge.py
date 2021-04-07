#!/usr/bin/env python3
"""
Determination using the model of whether a song is 'yes' or 'no'
"""
import sys
import os
import datetime
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

    # TODO: Rename to be user specific
    learn = load_learner("/src/data/models/current.pkl")
    learn.dls = dls

    # learn.fine_tune(epochs)
    last_rate = -1
    current_rate = 0
    while current_rate > last_rate:
        print("Saving model...")

        # TODO: Rename to be user specific
        learn.export("/tmp/model.pkl")
        print("Fitting...")
        learn.fine_tune(1)

        preds,y_hat,_ = learn.get_preds(with_loss=True)
        count = 0
        for i in range(0,len(preds)):
            count += int(bool(y_hat[i]) == bool(preds[i][0] < preds[i][1]))
        

        last_rate = current_rate
        current_rate = 1.0 * count / len(preds)

        print("Last_rate:", last_rate)
        print("Current rate:", current_rate)

    print("Out of loop")
    print("Loading back in...")

    # TODO: Rename to be user specific
    learn = load_learner("/tmp/model.pkl")
    learn.dls = dls
    preds,y_hat,_ = learn.get_preds(with_loss=True)
    count = 0
    for i in range(0,len(preds)):
        count += int(bool(y_hat[i]) == bool(preds[i][0] < preds[i][1]))
    
    current_rate = 1.0 * count / len(preds)
    print("Current rate:", current_rate)

    # TODO: Rename to be user speicific
    os.system("rm /tmp/model.pkl")

    print("Moving model into place...")
    now = str(datetime.datetime.now()).replace(" ", "..")
    os.system("mv /src/data/models/current.pkl /src/data/models/current.pkl-" + now)
    learn.export("/src/data/models/current.pkl")

    print("Done")
    return learn