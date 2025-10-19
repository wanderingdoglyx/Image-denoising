import numpy as np
import os
import re

def binomial_subsampling(proj_data, prob):
    proj_data = np.asarray(proj_data)
    int_data = proj_data.astype(np.int32)  # Ensure integer counts
    subsampled = np.zeros_like(int_data)
    mask = int_data > 0
    subsampled[mask] = np.random.binomial(int_data[mask], 1 - prob)
    return subsampled.astype(np.float32)  # Return as float32 to match original format

def extract_dose_level(filename):
    match = re.search(r'd(\d+)\.a00$', filename)
    if match:
        dose_percent = int(match.group(1))
        return dose_percent / 100.0
    else:
        raise ValueError(f"Cannot extract dose level from filename: {filename}")

def process_all_a00_files(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.a00') and 'd' in filename:
                filepath = os.path.join(dirpath, filename)
                try:
                    dose_level = extract_dose_level(filename)
                    prob = 1.0 - dose_level

                    print(f"Subsampling {filename} with prob = {prob:.2f}")

                    # Load as float32
                    proj_data = np.fromfile(filepath, dtype=np.float32)

                    # Apply subsampling
                    proj_data_ss = binomial_subsampling(proj_data, prob)

                    # Overwrite original file
                    proj_data_ss.tofile(filepath)

                except Exception as e:
                    print(f"Error processing {filename}: {e}")

# Example usage
root_dir = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_def_375"
process_all_a00_files(root_dir)