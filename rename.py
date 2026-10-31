#rename all files in a directory with a specific prefix and sequential numbering

import os

# Configuration
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Renaming Folder") #Change this to your target directory
prefix = "train_game09" # Change this to your desired prefix

# Get all files in the directory
files = sorted([
    f for f in os.listdir(directory)
    if os.path.isfile(os.path.join(directory, f))
])

# Rename files
for i, filename in enumerate(files, start=1):
    old_path = os.path.join(directory, filename)

    # Preserve file extension
    extension = os.path.splitext(filename)[1]

    new_filename = f"{prefix}_{i:04d}{extension}"
    new_path = os.path.join(directory, new_filename)

    os.rename(old_path, new_path)
    print(f"{filename} -> {new_filename}")

print("Renaming complete!")