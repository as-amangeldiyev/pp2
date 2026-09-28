"""Parse JSON, convert Python values, and read/write JSON files."""

# This assignment requires the filename json.py. Temporarily exclude this
# script's directory so ``import json`` resolves to Python's standard library.
import os
import sys

_script_folder = os.path.dirname(os.path.abspath(__file__))
_original_path = sys.path[:]
try:
    sys.path[:] = [entry for entry in sys.path if os.path.abspath(entry or os.curdir) != _script_folder]
    import json
finally:
    sys.path[:] = _original_path


HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(HERE, "sample-data.json")
OUTPUT_FILE = os.path.join(HERE, "output.json")


def main():
    # JSON supports objects, arrays, strings, numbers, booleans, and null.
    raw_text = '{"language": "Python", "topics": ["iterators", "JSON"], "complete": true}'
    parsed = json.loads(raw_text)
    print("Parsed JSON string:", parsed)

    python_data = {
        "practice": 4,
        "topics": ["dates", "math", "JSON"],
        "completed": True,
        "optional_note": None,
    }
    encoded = json.dumps(python_data, indent=2)
    print("Python converted to JSON:\n" + encoded)

    # Read the supplied sample data and summarize it.
    with open(SAMPLE_FILE, encoding="utf-8") as sample_file:
        sample = json.load(sample_file)
    print("Sample course:", sample["course"])
    for student in sample["students"]:
        print(f"{student['name']}: {student['score']} (active: {student['active']})")

    # Write and then read a JSON file using the file helpers.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(python_data, output_file, indent=2)
    with open(OUTPUT_FILE, encoding="utf-8") as output_file:
        saved_data = json.load(output_file)
    print("Data read back from output.json:", saved_data)


if __name__ == "__main__":
    main()
