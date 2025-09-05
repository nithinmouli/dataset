# Bird Sound Dataset Collection

This project downloads and preprocesses bird sound recordings from Xeno-Canto for machine learning applications.

## Species Included
Based on research paper specifications:
- **Cipoh** (Aegithina tiphia) - 25 recordings
- **Prenjak** (Prinia familiaris) - 3 recordings
- **Merbah cerucuk** (Pycnonotus goiavier) - 18 recordings  
- **Pleci** (Zosterops palpebrosus) - 0 recordings (URLs malformed)

## Project Structure
```
major_project/
├── dataset_collector.py      # Downloads MP3 files from Xeno-Canto
├── convert_to_wav.py        # Converts MP3 to WAV format
├── dataset_summary.py       # Shows dataset statistics
├── setup.py                # Environment setup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── bird_sound_dataset_clean/  # Created after running scripts
    ├── Aegithina_tiphia/     # 25 MP3 files (152.3 MB)
    ├── Prinia_familiaris/    # 3 MP3 files (4.6 MB)
    ├── Pycnonotus_goiavier/  # 18 MP3 files (112.5 MB)
    └── Zosterops_palpebrosus/ # 0 files (URL issues)
```

## Quick Start

### 1. Run Setup (Recommended)
```bash
python setup.py
```
This will:
- Check and install Python dependencies
- Check for FFmpeg and help install it
- Guide you through the complete setup

### 2. Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (choose one method):
# Option A: Using Chocolatey (recommended)
choco install ffmpeg

# Option B: Using winget (Windows 10+)
winget install ffmpeg

# Option C: Manual download from https://ffmpeg.org/download.html
```

### 3. Collect Dataset
```bash
python dataset_collector.py
```

### 4. Convert to WAV
```bash
python convert_to_wav.py
```

### 5. View Summary
```bash
python dataset_summary.py
```

## Current Dataset Status
- **Total files**: 46 MP3 recordings
- **Total size**: 269.4 MB
- **Quality**: Grade 'A' recordings only
- **Status**: ✅ Downloaded, ⏳ Awaiting WAV conversion

## Dataset Details
| Species | Scientific Name | Files | Size | Status |
|---------|----------------|-------|------|--------|
| Cipoh | Aegithina tiphia | 25 | 152.3 MB | ✅ Complete |
| Prenjak | Prinia familiaris | 3 | 4.6 MB | ✅ Complete |
| Merbah cerucuk | Pycnonotus goiavier | 18 | 112.5 MB | ✅ Complete |
| Pleci | Zosterops palpebrosus | 0 | 0 MB | ❌ API Issues |

## Next Steps for ML Pipeline

### 1. Preprocessing (After WAV conversion)
- **Noise reduction**: Remove background noise
- **Segmentation**: Cut into 1-second clips  
- **Normalization**: Standardize volume levels
- **Labeling**: Classify as Normal vs. Threatened calls

### 2. Feature Extraction  
- Generate spectrograms using `librosa`
- STFT (Short-Time Fourier Transform)
- Mel-spectrograms for CNN processing
- Convert audio signals → visual representations

### 3. Model Training
- Train CNN on spectrogram images
- Binary classification: Normal vs. Threatened
- Use extracted features for pattern recognition

## Troubleshooting

### FFmpeg Issues
If WAV conversion fails:
1. Ensure FFmpeg is installed and in PATH
2. Test with: `ffmpeg -version`
3. Restart terminal after installation

### Download Issues
- Some URLs from Xeno-Canto may be malformed
- Script includes error handling to skip bad URLs
- Re-run collector if needed (skips existing files)

## File Formats
- **Original**: MP3 (variable quality from Xeno-Canto)
- **Processed**: WAV (22050 Hz, mono, 16-bit) - Standard for ML
- **Target**: Spectrograms (PNG/arrays) for CNN training

## Research Context
This dataset supports research on automatic bird call classification, specifically for distinguishing between normal and threatened vocalizations in Southeast Asian bird species.
