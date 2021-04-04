#!/usr/bin/env python3
"""
Tests for periodic tasks related to Cormorant
"""
from test_serve import client, songs
import cron
import serve
from serve import mongo_client

def test_one_at_a_time():
    """Tests that only one instance of cron can run at a time"""
    assert False


def test_populate_children(client):
    """
    Finds songs without children and populates them
        - Key here is that the songs must be judged
    """

    # Test listing the judged but no children
    assert ("dWOj02nPyxk", 2) in cron.list_judged_no_children() 

    # Obviously, we are ignoring the code that actually goes and finds the children
    # Test inserting a found child

    cron.insert_child("Test", "asdfasf", "parent", 1)

    a = mongo_client["cormorant"]["songs"].find_one({"title" : "Test"})

    assert a["children"] == []
    assert a["parents"] == ["parent"]
    assert a["generation"] == 2

    mongo_client["cormorant"]["songs"].delete_one({"title" : "Test"})

    # Test updating with a given set of children
    cron.update_with_children("dWOj02nPyxk", ["a", "b", "c"])
    
    a = serve.mongo_client["cormorant"]["songs"].find_one({"youtube_link" : "dWOj02nPyxk"})
    assert a

    assert a["children"] == ["a", "b", "c"]



def test_download_waiting():
    """Codifies the waiting songs that don't exist yet"""
    
    # Any existing song that doesn't have a matching image needs to be acquired - only if it doesn't have an automatic judgement

    a = cron.list_missing_images()
    assert a == ["WgdhRxxXQDk"]

    # Touch a file
    with open("/src/data/incoming/WgdhRxxXQDk.png", "w") as f:
        f.write("hi")
        
    a = cron.list_missing_images()
    assert "WgdhRxxXQDk" not in a


def test_training():
    """
    Updates the model and saves a copy as a backup
        - This is fairly intense.  Needs to balance with the ones from no-holding.  No-holding will probably have all the files, and a random amount will be brought over for model updating
    """
    assert False

def test_prune():
    """
    Tests pruning a branch that hasn't born fruit
        - Goes through each child to prune
        - Key will be if there is only one parent, then delete the child.  If there are multiple parents, then just remove the one parent that's being pruned
        - Also delete the node itself - the node itself will obviously be approved.  I guess we don't need it any more?  We will save the found good songs into another database
        - We do not delete any files
    """
    # This can be tested fully
    assert False

def test_snapshot_model_performance():
    """Snapshot the model performance and store it in the database for another graph"""
    assert False