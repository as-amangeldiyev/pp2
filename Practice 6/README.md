# Practice 6: File Handling and Built-in Functions

Beginner examples for Python files, paths, directories, and built-in functions. The examples use only the Python standard library and create their sample data inside this folder.

## Files

- `file_handling/file_basics.py` writes, reads, appends, and copies text files. It demonstrates `r`, `w`, `a`, and `x` modes, `read()`, `readline()`, `readlines()`, `with`, `pathlib`, `shutil`, and safe deletion of a generated copy.
- `file_handling/path_exercises.py` writes a list to a file, counts lines, creates A.txt through Z.txt, checks path access and existence, shows the filename and directory, lists files/directories, and finds `.txt` files.
- `directory_management/directory_examples.py` demonstrates `os.mkdir()`, `os.makedirs()`, `os.listdir()`, `os.chdir()`, `os.getcwd()`, `os.rmdir()`, plus copying and moving files with `shutil`.
- `builtin_functions/map_filter_reduce.py` demonstrates `len()`, `sum()`, `min()`, `max()`, `map()`, `filter()`, `reduce()`, and `sorted()`.
- `builtin_functions/enumerate_zip_examples.py` demonstrates `enumerate()`, `zip()`, `type()`, and common type conversions.

## Run the examples

From this folder, run each script with Python, for example:

```bash
python3 file_handling/file_basics.py
python3 file_handling/path_exercises.py
python3 directory_management/directory_examples.py
python3 builtin_functions/map_filter_reduce.py
python3 builtin_functions/enumerate_zip_examples.py
```

The scripts can be run more than once. They create or replace only their sample files and folders under `file_handling/sample_data/` and `directory_management/sample_directories/`.

## Learning resource

- [W3Schools: Python File Handling](https://www.w3schools.com/python/python_file_handling.asp)
- [Python `os` module](https://docs.python.org/3/library/os.html)
- [Python `pathlib`](https://docs.python.org/3/library/pathlib.html)
- [Python built-in functions](https://docs.python.org/3/library/functions.html)

For GitHub, add and commit the folder from the repository root:

```bash
git add "Practice 6"
git commit -m "Add Practice 6 file handling and built-in examples"
git push origin main
```
