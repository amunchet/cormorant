#!/usr/bin/env python3
"""
Tests for periodic tasks related to Cormorant
"""

def test_find_hero():
    """Finds the hero song to follow related until 0 matches found"""

def test_find_next_hero():
    """
    Finds the next possible hero (i.e. the sibling of the current hero)
    Works by going up one generation and selecting the next candidate
    """

def test_find_related():
    """Returns a list of related songs and their judgements for review"""

def test_training():
    """Updates the model and saves a copy as a backup"""

def test_prune():
    """
    Tests pruning a branch that hasn't born fruit
        - Goes through each child to prune
        - Key will be if there is only one parent, then delete the child.  If there are multiple parents, then just remove the one parent that's being pruned
        - Also delete the node itself
    """