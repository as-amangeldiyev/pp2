from pathlib import Path
import shutil
import os

folder = Path(__file__).parent / "sample_data"
folder.mkdir(exist_ok=True)
text_file = folder / "sample.txt"

# Write mode creates a file or replaces its old contents.
with open(text_file, "w", encoding="utf-8") as file:
    file.write("Apples\nBananas\nCherries\n")

# Read the whole file.
with open(text_file, "r", encoding="utf-8") as file:
    print("read():")
    print(file.read())

# readline() reads one line. readlines() returns all lines as a list.
with open(text_file, "r", encoding="utf-8") as file:
    print("readline():", file.readline().strip())

with open(text_file, "r", encoding="utf-8") as file:
    print("readlines():", file.readlines())

# Append mode adds text to the end of the file.
with open(text_file, "a", encoding="utf-8") as file:
    file.write("Dates\n")

# Exclusive creation mode only works when the file does not exist.
new_file = folder / "created_once.txt"
if not new_file.exists():
    with open(new_file, "x", encoding="utf-8") as file:
        file.write("This file was created with x mode.\n")

# Copy a backup with shutil, then copy the contents to another file.
backup_file = folder / "sample_backup.txt"
copy_file = folder / "sample_copy.txt"
shutil.copy(text_file, backup_file)
copy_file.write_text(text_file.read_text(encoding="utf-8"), encoding="utf-8")
print("Backup and copy created.")

# Delete only the generated copy after checking that it exists and is writable.
if copy_file.exists() and copy_file.is_file() and os.access(copy_file.parent, os.W_OK):
    copy_file.unlink()
    print("Deleted generated copy:", copy_file.name)
