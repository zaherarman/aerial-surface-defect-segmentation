import requests
import os
import zipfile
import shutil

from ..config import RAW_DATA_DIR

def extract_data(id="17477702", raw_data_dir="data/raw", only_images=False):
    dirs = {
        "images": os.path.join(RAW_DATA_DIR, "images"),
        "videos": os.path.join(RAW_DATA_DIR, "videos"),
        "labels": os.path.join(RAW_DATA_DIR, "labels"),
        "raw": os.path.join(RAW_DATA_DIR, "raw_zips")
    }

    for d in dirs.values(): 
        os.makedirs(d, exist_ok=True)

    api_url = f"https://zenodo.org/api/records/{id}"
    files_metadata = requests.get(api_url).json()['files']

    for file in files_metadata:
        filename = file['key']
        zip_path = os.path.join(dirs["raw"], filename)
        
        # Keyword filter: prioritize images if req
        lowered_name = filename.lower()
        if only_images and "images" not in lowered_name:
            print(f"Skipping {filename} (priority: Images Only)")
            continue

        # Targeted download
        if not os.path.exists(zip_path):
            print(f"Downloading {filename}...")
            r = requests.get(file['links']['self'], stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

        # Unpacking and sorting
        if zip_path.endswith(".zip"):
            print(f"Unpacking and sorting {filename}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if zip_ref.getinfo(member).is_dir(): continue
                    
                    ext = os.path.splitext(member)[1].lower()
                    
                    # Logic for internal sorting
                    if ext in ['.jpg', '.jpeg', '.png']:
                        target = dirs["images"]
                    elif ext in ['.mp4', '.avi', '.mov']:
                        target = dirs["videos"]
                    elif ext in ['.txt', '.json']:
                        target = dirs["labels"]
                    else:
                        continue
                    
                    # Stream extraction straight to target
                    with zip_ref.open(member) as source, \
                         open(os.path.join(target, os.path.basename(member)), "wb") as f:
                        shutil.copyfileobj(source, f)

    print("Success: Data organized.")

if __name__ == "__main__":
    extract_data()