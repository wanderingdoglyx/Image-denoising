import random

# Set a seed for reproducibility
random.seed(42)

# Function to generate the new variable
def generate_variable():
    variable_loc = random.choice(['da', 'di'])
    variable_extent = random.choice([60])
    #variable_severity = random.choice([100, 175, 250])
    variable_severity = random.choice([250])
    return f"{variable_loc}21{variable_extent}s{variable_severity}"

# Read the input file and process
def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Read the number from the first column
            number = line.strip()
            # Generate the new variable
            new_variable = generate_variable()
            # Write the original number and new variable to the output file
            outfile.write(f"{number} {new_variable}\n")

source_path=f'/datastore01/user-storage/y.zezhang/2025_high_dose_project/document/observer_study'

# Example usage
input_file = f'{source_path}/pat_id_diseased_pilot.txt'  # Replace with your input file path
output_file = f'{source_path}/pat_id_diseased_pilot_defect_selected.txt'  # Replace with your desired output file path
process_file(input_file, output_file)