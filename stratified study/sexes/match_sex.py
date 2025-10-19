import glob

# Step 1: Build sex_dict from female and male files
sex_dict = {}

# Add female IDs
with open("ze_F_patients.txt", "r") as f:
    for line in f:
        patient_id = line.strip().split()[0]  # Handle ID-only or ID with extra columns
        if patient_id:
            sex_dict[patient_id] = "F"

# Add male IDs
with open("ze_M_patients.txt", "r") as f:
    for line in f:
        patient_id = line.strip().split()[0]
        if patient_id:
            sex_dict[patient_id] = "M"

# Step 2: Read the ID list from two specific files
id_list = []
for file in ["pat_id_healthy_pilot.txt", "pat_id_diseased_pilot_defect_selected.txt"]:
    with open(file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                id_list.append(parts[0])

# Step 3: Write only IDs to male.txt, female.txt, unknown.txt
with open("male.txt", "w") as male_file, \
     open("female.txt", "w") as female_file, \
     open("unknown.txt", "w") as unknown_file:

    for pid in id_list:
        sex = sex_dict.get(pid)
        if sex == "M":
            male_file.write(f"{pid}\n")
        elif sex == "F":
            female_file.write(f"{pid}\n")
        else:
            unknown_file.write(f"{pid}\n")