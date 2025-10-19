from pathlib import Path

# Path to the .imrmc file
file_path = Path("pilot_study_final.imrmc")

# Read all lines
with file_path.open("r") as file:
    lines = file.readlines()

# Locate BEGIN DATA and reader data start
begin_data_idx = next(i for i, line in enumerate(lines) if line.strip() == "BEGIN DATA:")
reader_start_idx = next(i for i, line in enumerate(lines) if line.strip().startswith("readerj.tania@wustl.edu,"))

# Extract the data block to deduplicate
data_block = lines[begin_data_idx + 1:reader_start_idx]

# Deduplicate based on the second column (case ID)
seen_case_ids = set()
deduped_data_block = []
for line in data_block:
    parts = line.strip().split(",")
    if len(parts) > 1 and parts[1].startswith("case"):
        case_id = parts[1]
        if case_id in seen_case_ids:
            continue
        seen_case_ids.add(case_id)
    deduped_data_block.append(line)

# Final cleaned content
cleaned_lines = lines[:begin_data_idx + 1] + deduped_data_block + lines[reader_start_idx:]

# Save to new file
output_path = file_path.with_stem(file_path.stem + "_partial_dedup")
with output_path.open("w") as file:
    file.writelines(cleaned_lines)

print(f"Cleaned file saved as: {output_path.name}")

