import os
import shutil
from pathlib import Path

data_path = f"{Path.home()}/data/0.35_reduced_then_balanced/data_224"


create_folders = [
    "unseen", "unseen/data_224", "unseen/data_224/entangled", "unseen/data_224/not_entangled"
]
for f in create_folders:
    if os.path.exists(f"{Path.home()}/data/{f}"):
        continue
    else:
        os.mkdir(f"{Path.home()}/data/{f}")


# Function to list all files in a directory (including subdirectories)
def list_files(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


# Paths to your datasets
small_dataset_path = f"{Path.home()}/data/0.35_reduced_then_balanced"
large_dataset_path = f"{Path.home()}/data/all_data"

# List files in both datasets
small_dataset_filenames = [path.split("/")[-1] for path in list_files(small_dataset_path)]
large_dataset_paths = list_files(large_dataset_path)

data_map = {
    path.split("/")[-1]: path for path in large_dataset_paths if path.split("/")[-1] not in small_dataset_filenames
}

print("Size of large dataset", len(large_dataset_paths))
print("Size of smaller dataset", len(small_dataset_filenames))
print("size of non-overlapping (unseen) data", len(data_map))

target_path = f"{Path.home()}/data/unseen"
for file_path in data_map.values():
    point_a = file_path
    point_b = f'{target_path}/{"/".join(file_path.split("/")[5:])}'
    shutil.copy(point_a, point_b)