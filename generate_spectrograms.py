"""
Spectrogram Generation Script
Converts audio files to visual spectrograms for CNN training
"""

import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import glob
from pathlib import Path

def create_spectrogram_directories(base_dir="spectrograms"):
    """Create directories for storing spectrograms."""
    species_dirs = ["Aegithina_tiphia", "Prinia_familiaris", "Pycnonotus_goiavier", "Zosterops_palpebrosus"]
    
    for species in species_dirs:
        spectrogram_dir = os.path.join(base_dir, species)
        os.makedirs(spectrogram_dir, exist_ok=True)
        print(f"Created directory: {spectrogram_dir}")
    
    return base_dir

def generate_mel_spectrogram(audio_file, output_dir, sr=22050, n_mels=128, hop_length=512):
    """
    Generate mel-spectrogram from audio file.
    
    Args:
        audio_file (str): Path to audio file
        output_dir (str): Directory to save spectrogram
        sr (int): Sample rate
        n_mels (int): Number of mel frequency bins
        hop_length (int): Number of samples between successive frames
    """
    try:
        y, sr = librosa.load(audio_file, sr=sr)
        
        mel_spec = librosa.feature.melspectrogram(
            y=y, sr=sr, n_mels=n_mels, hop_length=hop_length
        )
        
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(
            mel_spec_db, sr=sr, hop_length=hop_length, 
            x_axis='time', y_axis='mel', fmax=8000
        )
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'Mel-spectrogram: {os.path.basename(audio_file)}')
        plt.tight_layout()
        
        filename = os.path.splitext(os.path.basename(audio_file))[0]
        output_path = os.path.join(output_dir, f"{filename}_mel_spectrogram.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    except Exception as e:
        print(f"Error processing {audio_file}: {str(e)}")
        return None

def generate_stft_spectrogram(audio_file, output_dir, sr=22050, hop_length=512):
    """
    Generate STFT spectrogram from audio file.
    
    Args:
        audio_file (str): Path to audio file
        output_dir (str): Directory to save spectrogram
        sr (int): Sample rate
        hop_length (int): Number of samples between successive frames
    """
    try:
        y, sr = librosa.load(audio_file, sr=sr)
        
        stft = librosa.stft(y, hop_length=hop_length)
        stft_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(
            stft_db, sr=sr, hop_length=hop_length,
            x_axis='time', y_axis='hz'
        )
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'STFT Spectrogram: {os.path.basename(audio_file)}')
        plt.tight_layout()
        
        filename = os.path.splitext(os.path.basename(audio_file))[0]
        output_path = os.path.join(output_dir, f"{filename}_stft_spectrogram.png")
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
        
    except Exception as e:
        print(f"Error processing {audio_file}: {str(e)}")
        return None

def process_dataset(dataset_dir="bird_sound_dataset_clean", spectrogram_type="mel"):
    """
    Process entire dataset to generate spectrograms.
    
    Args:
        dataset_dir (str): Directory containing audio files
        spectrogram_type (str): Type of spectrogram ('mel' or 'stft' or 'both')
    """
    if not os.path.exists(dataset_dir):
        print(f"Dataset directory '{dataset_dir}' not found!")
        print("Please run dataset_collector.py and convert_to_wav.py first.")
        return
    
    base_output_dir = create_spectrogram_directories()
    
    total_generated = 0
    
    species_dirs = [d for d in os.listdir(dataset_dir) 
                   if os.path.isdir(os.path.join(dataset_dir, d))]
    
    for species_dir in species_dirs:
        species_path = os.path.join(dataset_dir, species_dir)
        output_dir = os.path.join(base_output_dir, species_dir)
        
        print(f"\n🎵 Processing {species_dir}...")
        
        wav_files = glob.glob(os.path.join(species_path, "*.wav"))
        mp3_files = glob.glob(os.path.join(species_path, "*.mp3"))
        
        audio_files = wav_files if wav_files else mp3_files
        
        if not audio_files:
            print(f"No audio files found in {species_dir}")
            continue
        
        file_type = "WAV" if wav_files else "MP3"
        print(f"Found {len(audio_files)} {file_type} files")
        
        for i, audio_file in enumerate(audio_files, 1):
            print(f"Processing {i}/{len(audio_files)}: {os.path.basename(audio_file)}")
            
            if spectrogram_type in ['mel', 'both']:
                mel_output = generate_mel_spectrogram(audio_file, output_dir)
                if mel_output:
                    total_generated += 1
                    print(f"  ✅ Mel-spectrogram saved: {os.path.basename(mel_output)}")
            
            if spectrogram_type in ['stft', 'both']:
                stft_output = generate_stft_spectrogram(audio_file, output_dir)
                if stft_output:
                    total_generated += 1
                    print(f"  ✅ STFT spectrogram saved: {os.path.basename(stft_output)}")
    
    print(f"\n🎉 Spectrogram generation complete!")
    print(f"Total spectrograms generated: {total_generated}")
    print(f"Spectrograms saved in: {base_output_dir}/")
    
    return total_generated

if __name__ == "__main__":
    print("🎨 BIRD SOUND SPECTROGRAM GENERATOR")
    print("=" * 50)
    
    try:
        import librosa
        import matplotlib.pyplot as plt
        print("✅ Required libraries available")
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("Please install: pip install librosa matplotlib")
        exit(1)
    
    print("\nSpectrogram types:")
    print("1. Mel-spectrogram (recommended for bird sounds)")
    print("2. STFT spectrogram") 
    print("3. Both types")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    spectrogram_types = {
        '1': 'mel',
        '2': 'stft', 
        '3': 'both'
    }
    
    selected_type = spectrogram_types.get(choice, 'mel')
    print(f"\nGenerating {selected_type} spectrogram(s)...")
    
    process_dataset(spectrogram_type=selected_type)
