
import requests
import os
import json

species_list = [
    "Aegithina tiphia",
    "Prinia familiaris",
    "Pycnonotus goiavier",
    "Zosterops palpebrosus" 
]

# Define the base URL for the Xeno-Canto API
BASE_API_URL = "https://www.xeno-canto.org/api/2/recordings"

# Set a limit for the number of files to download per species
DOWNLOAD_LIMIT_PER_SPECIES = 25

# Create a main directory to store the dataset
# The paper saves audio files into a 'clean' folder, so we'll do the same.
DATASET_DIR = "bird_sound_dataset_clean"
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)
    print(f"Created directory: {DATASET_DIR}")

for species in species_list:
    species_dir = os.path.join(DATASET_DIR, species.replace(" ", "_"))
    if not os.path.exists(species_dir):
        os.makedirs(species_dir)
        print(f"Created subdirectory: {species_dir}")
    

    query = f'{species} q:A'
    params = {'query': query}
    
    # Make a GET request to the Xeno-Canto API
    print(f"\nFetching data for {species}...")
    response = requests.get(BASE_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        recordings = data.get('recordings', [])
        if not recordings:
            print(f"No recordings found for {species}.")
            continue
            
        print(f"Found {len(recordings)} recordings for {species}. Downloading the first {DOWNLOAD_LIMIT_PER_SPECIES}...")
        
        for i, recording in enumerate(recordings[:DOWNLOAD_LIMIT_PER_SPECIES]):
            try:
                file_url = recording['file']
                if not file_url.startswith('http'):
                    file_url = "https:" + file_url
                
                if file_url == "https:":
                    print(f"Skipping malformed URL for recording {recording.get('id', 'unknown')}")
                    continue
                recording_id = recording['id']
                file_name = f"{recording_id}.mp3"
                file_path = os.path.join(species_dir, file_name)
                
                if not os.path.exists(file_path):
                    print(f"Downloading {i+1}/{DOWNLOAD_LIMIT_PER_SPECIES}: {file_name}")
                    audio_response = requests.get(file_url)
                    with open(file_path, 'wb') as f:
                        f.write(audio_response.content)
                else:
                    print(f"File {file_name} already exists. Skipping.")
            except Exception as e:
                print(f"Error downloading recording {i+1}: {str(e)}")
                continue
    else:
        print(f"Failed to fetch data for {species}. Status code: {response.status_code}")

print("\nDataset download complete!")
print("Next step: Convert the downloaded .mp3 files to .wav format for preprocessing.")
