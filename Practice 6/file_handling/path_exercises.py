from pathlib import Path
import os

folder = Path(__file__).parent / "sample_data"
folder.mkdir(exist_ok=True)
text_file = folder / "lines.txt"

# Write a list to a file.
items = ["first item", "second item", "third item"]
with open(text_file, "w", encoding="utf-8") as file:
    for item in items:
        file.write(item + "\n")

# Count lines in the text file.
with open(text_file, "r", encoding="utf-8") as file:
    line_count = len(file.readlines())
print("Line count:", line_count)

# Make 26 text files named A.txt through Z.txt.
letters_folder = folder / "letters"
letters_folder.mkdir(exist_ok=True)
for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    (letters_folder / (letter + ".txt")).write_text(letter, encoding="utf-8")
print("Created A.txt through Z.txt")

# Check path existence and access permissions.
path = text_file
print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))

# If a path exists, show its filename and directory portion.
if path.exists():
    print("Filename:", path.name)
    print("Directory:", path.parent)

# List only files, only directories, and all entries in the sample folder.
entries = list(folder.iterdir())
print("Files:", [entry.name for entry in entries if entry.is_file()])
print("Directories:", [entry.name for entry in entries if entry.is_dir()])
print("All entries:", os.listdir(folder))

# Find files by extension, including files in the letters subdirectory.
print("Text files:", [file.name for file in folder.rglob("*.txt")])
