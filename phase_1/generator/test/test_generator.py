#!/usr/bin/env python
"""
Tests the generator function
"""
import generator
import os
import subprocess
import filecmp

OUTPUT = [
        'bass_acoustic_000-025-025.wav',
        'bass_acoustic_000-029-100.wav',
        'bass_acoustic_000-025-127.wav',
        'bass_acoustic_000-029-025.wav',
        'bass_acoustic_000-024-075.wav',
        'bass_acoustic_000-027-025.wav',
        'bass_acoustic_000-025-075.wav',
        'bass_acoustic_000-025-050.wav',
        'bass_acoustic_000-024-100.wav',
        'bass_acoustic_000-026-100.wav'
            ]

def test_select_files():
    """
    Tests selection of the files
        - Should return a list of file names to combine

    Since we'll be passing the random seed, should be consistent
    """
    a = generator.select_files(dir="data")
    
        
    assert a == OUTPUT


def test_create_combined_wav():
    """
    Tests creation of combined wav file from given list
    """
    found = 0
    try:
        generator.combine(OUTPUT, cmd="asdfasdf", output="output.wav")
    except Exception:
        found = 1

    assert found

    a = generator.combine(["data/" + x for x in OUTPUT], output="output.wav")
    
    ref = ['sox', 'data/bass_acoustic_000-025-025.wav', 'data/bass_acoustic_000-029-100.wav', 'data/bass_acoustic_000-025-127.wav', 'data/bass_acoustic_000-029-025.wav', 'data/bass_acoustic_000-024-075.wav', 'data/bass_acoustic_000-027-025.wav', 'data/bass_acoustic_000-025-075.wav', 'data/bass_acoustic_000-025-050.wav', 'data/bass_acoustic_000-024-100.wav', 'data/bass_acoustic_000-026-100.wav', 'output.wav', 'splice', '-h', '2,1']

    assert a.args == ref

    os.remove("output.wav")



def test_combinations():
    """Tests reading and updating the combinations txt file"""
    assert "temp.txt" not in os.listdir(".")
    assert not generator.check(filename="temp.txt", combination=OUTPUT)
    generator.update(filename="temp.txt", combination=OUTPUT)
    assert generator.check(filename="temp.txt", combination=OUTPUT)
    os.remove("temp.txt")


