#!/usr/bin/env python
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os 
load_dotenv()


api_key = os.getenv("API_KEY")

api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)

request = youtube.search().list(
    part="snippet",
    relatedToVideoId="wtLJPvx7-ys",
    type="video"
)
response = request.execute()

print(response)

