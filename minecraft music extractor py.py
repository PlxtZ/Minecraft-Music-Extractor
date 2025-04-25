import json, os, platform, shutil, re

''' 
    Extracts Minecraft sound/music files from .minecraft/assets to a readable folder structure.
    Output will be saved to ~/Desktop/MC_Sounds/
'''

# Detect OS and get .minecraft/assets path
print("Your OS is " + platform.system())
if platform.system() == "Windows":
    MC_ASSETS = os.path.expandvars(r"%APPDATA%\.minecraft\assets")
else:
    MC_ASSETS = os.path.expanduser("~/.minecraft/assets")

INDEXES_PATH = os.path.join(MC_ASSETS, "indexes")
OBJECTS_PATH = os.path.join(MC_ASSETS, "objects")

# Function to extract numeric or semantic version numbers
def version_key(filename):
    # Prioritize numeric-only files like '24.json' by using int conversion
    match = re.findall(r'\d+', filename)
    return tuple(map(int, match)) if match else (0,)

# Find the latest index file (e.g., '24.json' or '1.20.4.json')
index_files = [f for f in os.listdir(INDEXES_PATH) if f.endswith(".json")]
latest_index = sorted(index_files, key=version_key)[-1]

print("Using index file:", latest_index)

# Output path on desktop
OUTPUT_PATH = os.path.normpath(os.path.expanduser("~/Desktop/MC_Sounds/"))

# Load index JSON
with open(os.path.join(INDEXES_PATH, latest_index), "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter for only sound files in 'minecraft/sounds/'
MC_SOUNDS = "minecraft/sounds/"
sound_entries = {
    key[len(MC_SOUNDS):]: value["hash"]
    for key, value in data["objects"].items()
    if key.startswith(MC_SOUNDS)
}

print(f"Found {len(sound_entries)} sound files. Extracting...\n")

# Extract and copy files to proper folder
for rel_path, hash_val in sound_entries.items():
    source = os.path.join(OBJECTS_PATH, hash_val[:2], hash_val)
    destination = os.path.join(OUTPUT_PATH, "sounds", rel_path)

    # Create folder path if needed
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    # Copy file
    try:
        shutil.copyfile(source, destination)
        print("✓", rel_path)
    except Exception as e:
        print("✗", rel_path, "-", e)

print("\nDone! All files extracted to:", os.path.join(OUTPUT_PATH, "sounds"))
