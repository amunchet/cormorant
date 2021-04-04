#!/usr/bin/env python3
"""
Dumps in a given playlist into the Mongo Database as Generation 0
"""
import serve
import spider
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a playlist Id to load into the database.")
        sys.exit(1)


    # Clear the database first 
    print("Clearing the database...")
    serve.mongo_client["cormorant"]["songs"].delete_many({})
    serve.mongo_client["cormorant"]["stats"].delete_many({})
    

    # Download list from the playlist URL
    print("Downloading the playlist...")
    a = spider.load_playlist(sys.argv[1])

    # Save to database
    print("Loading into the database...")
    for item in a:
        item["generation"] = 0
        item["children"] = []
        item["parents"] = []
        item["manual_judgement"] = 1
        item["predicted_judgement"] = 1
        serve.mongo_client["cormorant"]["songs"].insert_one(item)
    
    print("Done")
