# OBSOLETED IN FAVOR OF THE FMA LARGE DATASET

# Generator
This is the script that generates the sample combined WAV files for pre-training the model.

## Functionality
1.  Pick a random combintion of 10 of the present wav files.  
2.  Check if the combination exists in `combinations.txt` - if so, pick another one.
3.  Use `sox` to generate the combined wav file
4.  Write to `combinations.txt`
