@echo off
echo ================================================
echo BIRD SOUND DATASET COLLECTION WORKFLOW
echo ================================================
echo.

echo Step 1: Environment Setup
echo --------------------------
python setup.py
echo.

echo Step 2: Download Dataset  
echo -------------------------
python dataset_collector.py
echo.

echo Step 3: Convert to WAV (requires FFmpeg)
echo ------------------------------------------
python convert_to_wav.py
echo.

echo Step 4: Dataset Summary
echo -----------------------
python dataset_summary.py
echo.

echo ================================================
echo WORKFLOW COMPLETE!
echo ================================================
echo.
echo Next steps:
echo 1. Check the bird_sound_dataset_clean/ folder
echo 2. Proceed with audio preprocessing and feature extraction
echo 3. Generate spectrograms for CNN training
echo.
pause
