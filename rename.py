#rename all files in a directory with a specific prefix and sequential numbering

import os

# Configuration
directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Renaming Folder") #Change this to your target directory
prefix = "validation_game10" # Change this to your desired prefix
start_number = 1 # Change this to the first number to use (1 is lowest)

if start_number < 1:
    start_number = 1

# Get all files in the directory
files = sorted([
    f for f in os.listdir(directory)
    if os.path.isfile(os.path.join(directory, f))
])

# Rename files
for i, filename in enumerate(files, start=start_number):
    old_path = os.path.join(directory, filename)

    # Preserve file extension
    extension = os.path.splitext(filename)[1]

    new_filename = f"{prefix}_{i:04d}{extension}"
    new_path = os.path.join(directory, new_filename)

    os.rename(old_path, new_path)
    print(f"{filename} -> {new_filename}")

print("Renaming complete!")