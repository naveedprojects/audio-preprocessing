import os
import wave
import struct
import numpy as np
import webrtcvad

# Set the directory containing the WAV files
directory = "wavs"

# Initialize the VAD
vad = webrtcvad.Vad()
vad.set_mode(3)  # Set the VAD aggressiveness level (0-3)

# Process each WAV file in the directory
for filename in os.listdir(directory):
    if not filename.endswith(".wav"):
        continue

    # Open the WAV file
    wav_file = wave.open(os.path.join(directory, filename), "rb")

    # Get the sample rate, sample width, and number of channels
    sample_rate = wav_file.getframerate()
    sample_width = wav_file.getsampwidth()
    num_channels = wav_file.getnchannels()

    # Calculate the frame size (number of bytes per frame)
    frame_size = sample_width * num_channels

    # Read the audio data in chunks
    chunk_size = int(sample_rate * 0.03)  # 30 ms chunk size
    is_speech = False
    count = 0
    while True:
        data = wav_file.readframes(chunk_size)
        # print(data)
        if len(data) == 0:
            break
        # Perform VAD analysis on the audio data
        if vad.is_speech(data, sample_rate):
            is_speech = True
            break

    # Print the result
    if not is_speech:
        print(filename, "does not contain speech")
    # else:
    #     print(filename, "contain speech")

    # Close the input file
    wav_file.close()
