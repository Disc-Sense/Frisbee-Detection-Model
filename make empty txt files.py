#make empty txt files

import os

# Configuration
base_directory = os.path.dirname(os.path.abspath(__file__))

test_train_or_val = "val"

image_directory = os.path.join(base_directory, "data", "images", test_train_or_val)
txt_directory = os.path.join(base_directory, "data", "labels", test_train_or_val)

# Supported image extensions
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

# Make sure the text directory exists
os.makedirs(txt_directory, exist_ok=True)

# Get existing text filenames (without extensions)
existing_txt = {
    os.path.splitext(f)[0]
    for f in os.listdir(txt_directory)
    if f.lower().endswith(".txt")
}

# Process image files
created = 0

for filename in os.listdir(image_directory):
    if filename.lower().endswith(image_extensions):
        image_name = os.path.splitext(filename)[0]

        if image_name not in existing_txt:
            txt_path = os.path.join(txt_directory, image_name + ".txt")

            with open(txt_path, "w") as f:
                pass

            print(f"Created: {image_name}.txt")
            created += 1

print(f"\nComplete! Created {created} empty text files.")