import os

def find_unmatched_folders(folder_path, file_path):
    # Get list of subfolder names
    folder_names = [
        name for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]

    # Get set of base filenames (before the extension)
    file_names = {
        os.path.splitext(filename)[0]
        for filename in os.listdir(file_path)
        if os.path.isfile(os.path.join(file_path, filename))
    }

    # Find unmatched folders
    unmatched = [name for name in folder_names if name not in file_names]

    # Output the unmatched folders
    print("Unmatched folders:")
    for name in unmatched:
        print(name)

# Example usage
subfolders_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments"
files_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl"

find_unmatched_folders(subfolders_root, files_root)
