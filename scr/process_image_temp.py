import os

def delete_files_with_keywords(root_folder, keywords=("d3", "d4", "d5", "d6")):
    deleted_files = []

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if any(keyword in filename for keyword in keywords):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    print(f"\n✅ Total files deleted: {len(deleted_files)}")

# === USAGE ===
# Replace with your actual path
target_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_DATA"
delete_files_with_keywords(target_folder)