# Summary
Cormorant is part of the Homelab Music Aquisition System (HMAS).

Components of this system include:
- VPN - Wireguard to access from Mobile
- Airsonic - server for app to access via mobile
- Youtubber
	+ Downloads new additions to playlist (Currently "Not Added Yet")
	+ [Future] Will download portions of the song based on Youtube comment

- Cormorant

## Cormorant

Cormorant is a proactive music acquisition system.  This differs from recommendation systems based on similar users that Youtube and Spotify use.  Cormorant seeks to render a given song into a spectrogram, then use a Neural network to determine whether or not it is a "good" song.  To put it simply, Cormorant is less dependent on others and seeks to objectively codify the user's song preferences.


## Requirements
- `ffmpeg` must be installed
- `sox` must be installed	

## Phases
1.  Be able to download a given Youtube playlist
2.  Convert to WAV files via ffmpeg
3.  Turn into spectograms and label

4.  Bring into Jupyter notebooks to train first version of network
	  - Some thoughts: Do we want to classify or regress the score of the song?

5.  Deploy - needs frontend to continue online training and rating of songs.

