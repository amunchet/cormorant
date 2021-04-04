#!/usr/bin/env python
"""
Youtube API functions
"""
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os 
load_dotenv()


def load_related(video_id): # pragma: no cover
    """Loads related"""
    api_key = os.getenv("API_KEY")

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        # relatedToVideoId="wtLJPvx7-ys",
        relatedToVideoId=video_id,
        type="video",
        maxResults=10
    )
    response = request.execute()

    return response

def load_playlist(playlist_id): # pragma: no cover
    """Loads playlist id"""
    api_key = os.getenv("API_KEY")

    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)

    
    continuing = True
    items = []
    count = 0
    nextToken = ""

    print("Starting...")

    while count < 40: # Max size of 2000 items
        print("On page ", count)
        if not nextToken and count != 0: # Reached the end
            print("No nextTokens found, breaking.")
            break

        if nextToken == "":
            request = youtube.playlistItems().list(
                part="snippet, status, id, contentDetails",
                playlistId=playlist_id,
                maxResults=50
            )
        else:
            request = youtube.playlistItems().list(
                part="snippet, status, id, contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken = nextToken
            )

        response = request.execute()
    

        for item in response["items"]:
            items.append({
                "title": item["snippet"]["title"],
                "youtube_link" : item["snippet"]["resourceId"]["videoId"]
            })

        if "nextPageToken" in response:
            nextToken = response["nextPageToken"]
        else:
            break
        count += 1

    print("Done.")
    return items