from pathlib import Path
import os
import shutil

base = Path(__file__).parent / "sample_directories"

# os.mkdir() creates one directory; os.makedirs() creates nested directories.
base.mkdir(exist_ok=True)
one_folder = base / "one_folder"
if not one_folder.exists():
    os.mkdir(one_folder)
nested = base / "parent" / "child"
os.makedirs(nested, exist_ok=True)

source = nested / "example.txt"
source.write_text("Move and copy practice.\n", encoding="utf-8")
copy_folder = base / "copies"
copy_folder.mkdir(exist_ok=True)
shutil.copy(source, copy_folder / "example_copy.txt")

move_folder = base / "moved_files"
move_folder.mkdir(exist_ok=True)
shutil.move(str(source), str(move_folder / "example_moved.txt"))

print("Current working directory:", os.getcwd())
print("Items in sample directory:", os.listdir(base))

# Change directories briefly, then return to the original working directory.
old_directory = os.getcwd()
os.chdir(nested)
print("After chdir:", os.getcwd())
os.chdir(old_directory)

# Remove an empty directory. rmdir() requires the directory to be empty.
empty_folder = base / "empty_folder"
empty_folder.mkdir(exist_ok=True)
os.rmdir(empty_folder)
print("Removed empty_folder")
