"""
Audio Format Converter: MP3 to WAV
This script converts downloaded MP3 files to WAV format for ML processing.
"""

import os
from pydub import AudioSegment
import glob

def convert_mp3_to_wav(dataset_dir="bird_sound_dataset_clean"):
    """
    Convert all MP3 files in the dataset to WAV format.
    
    Args:
        dataset_dir (str): Path to the dataset directory
    """
    if not os.path.exists(dataset_dir):
        print(f"Dataset directory '{dataset_dir}' not found!")
        return
    
    # Get all subdirectories (species folders)
    species_dirs = [d for d in os.listdir(dataset_dir) 
                   if os.path.isdir(os.path.join(dataset_dir, d))]
    
    total_converted = 0
    
    for species_dir in species_dirs:
        species_path = os.path.join(dataset_dir, species_dir)
        print(f"\nProcessing species: {species_dir}")
        
        # Find all MP3 files in this species directory
        mp3_files = glob.glob(os.path.join(species_path, "*.mp3"))
        
        if not mp3_files:
            print(f"No MP3 files found in {species_dir}")
            continue
        
        print(f"Found {len(mp3_files)} MP3 files to convert")
        
        for mp3_file in mp3_files:
            try:
                # Create WAV filename
                wav_file = mp3_file.replace('.mp3', '.wav')
                
                # Skip if WAV already exists
                if os.path.exists(wav_file):
                    print(f"WAV already exists: {os.path.basename(wav_file)}")
                    continue
                
                # Load MP3 and convert to WAV
                audio = AudioSegment.from_mp3(mp3_file)
                
                # Export as WAV with standard ML settings
                # 16-bit depth, mono channel, 22050 Hz sample rate (common for bird sounds)
                audio = audio.set_frame_rate(22050)
                audio = audio.set_channels(1)  # Convert to mono
                audio = audio.set_sample_width(2)  # 16-bit
                
                audio.export(wav_file, format="wav")
                
                print(f"Converted: {os.path.basename(mp3_file)} -> {os.path.basename(wav_file)}")
                total_converted += 1
                
            except Exception as e:
                print(f"Error converting {mp3_file}: {str(e)}")
    
    print(f"\nConversion complete! Total files converted: {total_converted}")
    print("WAV files are now ready for preprocessing and feature extraction.")

if __name__ == "__main__":
    print("Starting MP3 to WAV conversion...")
    convert_mp3_to_wav()
