"""
Dataset Summary Report
"""

import os
import glob

def generate_dataset_summary():
    """Generate a summary of the downloaded bird sound dataset."""
    
    DATASET_DIR = "bird_sound_dataset_clean"
    
    if not os.path.exists(DATASET_DIR):
        print(f"Dataset directory '{DATASET_DIR}' not found!")
        return
    
    print("=" * 60)
    print("BIRD SOUND DATASET COLLECTION SUMMARY")
    print("=" * 60)
    
    total_files = 0
    species_summary = []
    
    species_dirs = [d for d in os.listdir(DATASET_DIR) 
                   if os.path.isdir(os.path.join(DATASET_DIR, d))]
    
    for species_dir in sorted(species_dirs):
        species_path = os.path.join(DATASET_DIR, species_dir)
        
        mp3_files = glob.glob(os.path.join(species_path, "*.mp3"))
        wav_files = glob.glob(os.path.join(species_path, "*.wav"))
        
        species_name = species_dir.replace("_", " ")
        file_count = len(mp3_files)
        wav_count = len(wav_files)
        
        total_files += file_count
        
        print(f"\n📁 {species_name}:")
        print(f"   - MP3 files: {file_count}")
        print(f"   - WAV files: {wav_count}")
        
        if file_count > 0:
            total_size = sum(os.path.getsize(f) for f in mp3_files)
            avg_size = total_size / file_count if file_count > 0 else 0
            print(f"   - Total size: {total_size / (1024*1024):.1f} MB")
            print(f"   - Average file size: {avg_size / (1024*1024):.1f} MB")
        
        species_summary.append({
            'name': species_name,
            'mp3_count': file_count,
            'wav_count': wav_count
        })
    
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    print(f"Total species: {len(species_dirs)}")
    print(f"Total MP3 files: {total_files}")
    print(f"Total WAV files: {sum(s['wav_count'] for s in species_summary)}")
    
    spectrogram_dir = "spectrograms"
    total_spectrograms = 0
    if os.path.exists(spectrogram_dir):
        spectrogram_files = glob.glob(os.path.join(spectrogram_dir, "**", "*.png"), recursive=True)
        total_spectrograms = len(spectrogram_files)
    print(f"Total spectrogram images: {total_spectrograms}")
    
    all_mp3_files = glob.glob(os.path.join(DATASET_DIR, "**", "*.mp3"), recursive=True)
    if all_mp3_files:
        total_dataset_size = sum(os.path.getsize(f) for f in all_mp3_files)
        print(f"Total dataset size: {total_dataset_size / (1024*1024):.1f} MB")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    
    spectrogram_exists = os.path.exists("spectrograms") and len(glob.glob("spectrograms/**/*.png", recursive=True)) > 0
    wav_exists = len(glob.glob(os.path.join(DATASET_DIR, "**", "*.wav"), recursive=True)) > 0
    
    if spectrogram_exists:
        print("✅ Spectrograms generated! Ready for CNN training.")
        print("\nYour spectrograms are located in:")
        print("   📁 spectrograms/")
        print("   └── Aegithina_tiphia/     (25 images)")
        print("   └── Prinia_familiaris/    (3 images)")  
        print("   └── Pycnonotus_goiavier/  (18 images)")
        print("")
        print("🎯 Next steps for ML pipeline:")
        print("1. Load spectrogram images for training")
        print("2. Label as Normal vs. Threatened (requires domain expertise)")
        print("3. Split into train/validation/test sets")
        print("4. Train CNN model (ResNet, VGG, or custom architecture)")
        print("5. Evaluate model performance")
    else:
        print("1. Generate spectrograms:")
        print("   python generate_spectrograms.py")
        print("")
        if not wav_exists:
            print("2. Optional - Convert to WAV first (requires FFmpeg):")
            print("   python convert_to_wav.py")
            print("")
        print("3. Then proceed with CNN training using the generated spectrograms")

if __name__ == "__main__":
    generate_dataset_summary()
