import os

def get_unmatched_folder_names(folder_path, file_path):
    folder_names = [
        name for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]

    file_base_names = {
        os.path.splitext(name)[0]
        for name in os.listdir(file_path)
        if os.path.isfile(os.path.join(file_path, name))
    }

    unmatched = [name for name in folder_names if name not in file_base_names]
    return unmatched

def find_matching_subfolders(unmatched_names, search_path):
    matched_paths = []

    for root, dirs, files in os.walk(search_path):
        for name in dirs:
            for unmatched in unmatched_names:
                if unmatched in name:
                    matched_paths.append(os.path.join(root, name))
                    break  # Avoid duplicate entries for the same folder

    return matched_paths


# Example usage
folder_with_subfolders =  "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments"
folder_with_files = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl"
search_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM"

# Step 1: Find unmatched folder names
unmatched_folders = get_unmatched_folder_names(folder_with_subfolders, folder_with_files)

# Step 2: Find matches in the third folder
matching_subfolders = find_matching_subfolders(unmatched_folders, search_folder)

# Output
print("Matching subfolders in the third directory:")
for path in matching_subfolders:
    print(path)