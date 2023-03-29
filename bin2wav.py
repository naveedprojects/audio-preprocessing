import os
import wave
import struct
import multiprocessing as mp

# Define the input and output directories
input_dir = 'vb-audio-efs-directory-2-24-2022'
output_dir = 'processed_audios'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def convert_bin_to_wav(bin_path):
    # Open the bin file
    with open(bin_path, 'rb') as bin_file:
        bin_data = bin_file.read()

    # Pad the data if the length is not a multiple of two
    if len(bin_data) % 2 != 0:
        bin_data += b'\x00'

    bin_array = struct.unpack('h' * (len(bin_data) // 2), bin_data)

    # Create the output wav file path
    wav_filename = os.path.basename(bin_path).replace('.bin', '.wav')
    wav_path = os.path.join(output_dir, wav_filename)

    # Open the output wav file and set the parameters
    with wave.open(wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)

        # Write the data to the wav file
        wav_file.writeframesraw(struct.pack('h' * len(bin_array), *bin_array))

    print(f'Converted {bin_path} to {wav_path}')

if __name__ == '__main__':
    # Recursively traverse the input directory and find all the bin files
    bin_paths = []
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.bin'):
                bin_paths.append(os.path.join(root, filename))

    # Use all available CPU cores to convert the bin files to wav files
    with mp.Pool() as pool:
        pool.map(convert_bin_to_wav, bin_paths)
