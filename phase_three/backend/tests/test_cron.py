#!/usr/bin/env python3
"""
Tests for periodic tasks related to Cormorant
"""

def test_one_at_a_time():
    """Tests that only one instance of cron can run at a time"""


def test_populate_children():
    """Finds songs without children and populates them"""

def test_download_waiting():
    """Codifies the waiting songs that don't exist yet"""

def test_training():
    """
    Updates the model and saves a copy as a backup
        - This is fairly intense.  Needs to balance with the ones from no-holding.  No-holding will probably have all the files, and a random amount will be brought over for model updating
    """

def test_prune():
    """
    Tests pruning a branch that hasn't born fruit
        - Goes through each child to prune
        - Key will be if there is only one parent, then delete the child.  If there are multiple parents, then just remove the one parent that's being pruned
        - Also delete the node itself
    """

def test_snapshot_model_performance():
    """Snapshot the model performance and store it in the database for another graph"""