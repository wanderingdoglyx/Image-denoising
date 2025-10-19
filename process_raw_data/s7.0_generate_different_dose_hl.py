import numpy as np
import os
import shutil

def binomial_subsampling(proj_data, prob):
    proj_data = np.asarray(proj_data)
    int_data = proj_data.astype(np.int32)
    subsampled = np.zeros_like(int_data)
    mask = int_data > 0
    subsampled[mask] = np.random.binomial(int_data[mask], 1 - prob)
    return subsampled.astype(np.float32)

def modify_and_copy_file(original_path, output_path, replacements):
    with open(original_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        for old, new in replacements.items():
            if old in line:
                line = line.replace(old, new)
        new_lines.append(line)

    with open(output_path, 'w') as f:
        f.writelines(new_lines)

def process_fixed_dose_levels(input_root, output_root, dose_levels=(50, 33, 100)):
    for dirpath, _, filenames in os.walk(input_root):
        a00_files = [f for f in filenames if f.endswith('.a00')]
        if not a00_files:
            continue

        relative_path = os.path.relpath(dirpath, input_root)

        for filename in a00_files:
            input_path = os.path.join(dirpath, filename)
            base_name = filename[:-4]  # Remove '.a00'
            try:
                proj_data = np.fromfile(input_path, dtype=np.float32)

                for dose in dose_levels:
                    prob = 1.0 - dose / 100.0
                    proj_data_ss = binomial_subsampling(proj_data, prob)

                    output_subdir = os.path.join(output_root, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)

                    # Save modified .a00 file
                    new_base = f"{base_name}_d{dose}"
                    output_a00_path = os.path.join(output_subdir, f"{new_base}.a00")
                    proj_data_ss.tofile(output_a00_path)
                    print(f"Saved: {output_a00_path}")

                    # Modify and save .h00
                    h00_original = os.path.join(dirpath, f"{base_name}.h00")
                    if os.path.exists(h00_original):
                        h00_output = os.path.join(output_subdir, f"{new_base}.h00")
                        modify_and_copy_file(
                            h00_original, h00_output,
                            {
                                f"!name of data file := {base_name}.a00": f"!name of data file := {new_base}.a00",
                                f"patient name := SMC_{base_name}.a00": f"patient name := SMC_{new_base}.a00"
                            }
                        )
                        print(f"Modified: {h00_output}")

                    # Modify and save .hct
                    hct_original = os.path.join(dirpath, f"{base_name}.hct")
                    if os.path.exists(hct_original):
                        hct_output = os.path.join(output_subdir, f"{new_base}.hct")
                        modify_and_copy_file(
                            hct_original, hct_output,
                            {
                                f"!name of data file := {base_name}.ict": f"!name of data file := {new_base}.ict"
                            }
                        )
                        print(f"Modified: {hct_output}")

                    # Copy .ict without modification (rename only)
                    ict_original = os.path.join(dirpath, f"{base_name}.ict")
                    if os.path.exists(ict_original):
                        ict_output = os.path.join(output_subdir, f"{new_base}.ict")
                        shutil.copy2(ict_original, ict_output)
                        print(f"Copied: {ict_output}")

            except Exception as e:
                print(f"Error processing {input_path}: {e}")



# Example usage
input_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100"
output_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_hl"
process_fixed_dose_levels(input_folder, output_folder, dose_levels=(33, 25,100))
