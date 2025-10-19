import re
from pathlib import Path

# Load your file
file_path = Path("pilot_study.imrmc")

# Read lines
with file_path.open("r") as file:
    lines = file.readlines()

# Transformation function
def transform_case(case_str):
    match = re.match(r"case(\d+)", case_str)
    if match:
        digits = match.group(1)
        if len(digits) >= 3:
            xy = int(digits[:-1])+2  # first two digits
            z = int(digits[-1])    # last digit
            new_case = f"case{xy // 3}{z}"
            return new_case
        elif len(digits) == 2:
            x = int(digits[0])+2
            y = int(digits[1])
            new_case = f"case{x // 3}{y}"
            return new_case
            
    return case_str  # unchanged

# Apply transformation
modified_lines = [
    re.sub(r"case\d+", lambda m: transform_case(m.group()), line)
    for line in lines
]

# Save new file
modified_file_path = file_path.with_stem(file_path.stem + "_final")
with modified_file_path.open("w") as file:
    file.writelines(modified_lines)

print(f"Saved as: {modified_file_path.name}")
