import os
import json
import sys

def compare_json(json_1, json_2):
    try:
        assert sorted(json_1.items()) == sorted(json_2.items())
        return True
    except AssertionError:
        return False

def read_json(path: str):
    with open(path, "r") as _file:
        return json.load(_file)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        original_folder = sys.argv[1]
        new_folder = sys.argv[2]
        print(f"Note: using {original_folder} for original JSONs and {new_folder} for new JSONs folders.")
    else:
        original_folder = "compare/"
        new_folder = "templates/config/"
    original_paths = sorted(os.listdir(original_folder))
    new_paths = sorted(os.listdir(new_folder))

    didnt_match = []
    matched = []
    for path, new_path in zip(original_paths, new_paths):

        path = "compare/" + path
        new_path = "templates/config/" + new_path

        # print(f"Now comparing: {path} vs {new_path}")
        obj_original, obj_new = read_json(path), read_json(new_path)
        did_match = compare_json(obj_original, obj_new)
        if not did_match:
            didnt_match.append(new_path)
        else:
            matched.append(path)


    print(f"Failures: {len(didnt_match)}/{len(new_paths)}")
    print(f"Success: {len(matched)}/{len(new_paths)}")

    if len(didnt_match) != 0:
        print("Files that didn't match are: ")
        print(didnt_match)
