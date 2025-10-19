import os

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

def copy_and_modify_headers(source_root, target_root):
    for patient_id in os.listdir(target_root):
        target_sub = os.path.join(target_root, patient_id)
        source_sub = os.path.join(source_root, patient_id)

        if not os.path.isdir(target_sub) or not os.path.isdir(source_sub):
            continue

        # Find source base name (e.g., '01004358') from .a00 file
        source_a00s = [f for f in os.listdir(source_sub) if f.endswith('.a00')]
        if not source_a00s:
            print(f"No .a00 in source: {source_sub}")
            continue

        source_base = os.path.splitext(source_a00s[0])[0]  # assume name like '01004358'

        # Modify headers for each .a00 file in target folder
        for target_a00 in os.listdir(target_sub):
            if not target_a00.endswith('.a00'):
                continue

            target_base = target_a00.replace('.a00', '')  # e.g., 'mod_proj_da2115s100_01004358_d33'
            target_path_a00 = os.path.join(target_sub, target_a00)

            # Modify and copy .h00
            source_h00 = os.path.join(source_sub, f"{source_base}.h00")
            if os.path.exists(source_h00):
                target_h00 = os.path.join(target_sub, f"{target_base}.h00")
                modify_and_copy_file(
                    source_h00,
                    target_h00,
                    {
                        f"!name of data file := {source_base}.a00": f"!name of data file := {target_base}.a00",
                        f"patient name := SMC_{source_base}.a00": f"patient name := SMC_{target_base}.a00"
                    }
                )
                print(f"Created: {target_h00}")

            # Modify and copy .hct
            source_hct = os.path.join(source_sub, f"{source_base}.hct")
            if os.path.exists(source_hct):
                target_hct = os.path.join(target_sub, f"{target_base}.hct")
                modify_and_copy_file(
                    source_hct,
                    target_hct,
                    {
                        f"!name of data file := {source_base}.ict": f"!name of data file := {target_base}.ict"
                    }
                )
                print(f"Created: {target_hct}")

# Example usage
source_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100"
target_root = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_def"
copy_and_modify_headers(source_root, target_root)