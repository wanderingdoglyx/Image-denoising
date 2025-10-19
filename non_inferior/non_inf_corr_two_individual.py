import csv

#  The CTAC column contains numbers from the first file.
#  The CTLESS column contains numbers from the second file.

def read_groups_from_file(filename):
    group_0, group_1 = [], []
    current_group = 0

    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "Large":
                current_group = 0
                continue
            if line == "*":
                if current_group == 0:
                    current_group = 1
                else:
                    break
            try:
                number = float(line)
                if current_group == 0:
                    group_0.append(number)
                elif current_group == 1:
                    group_1.append(number)
            except ValueError:
                continue  # Ignore non-numeric lines

    return group_0, group_1

def write_to_csv(file1_data, file2_data, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['CTAC', 'CTLESS', 'LABEL'])

        # Write the group 0 data (label 0)
        for ctac, ctless in zip(file1_data[0], file2_data[0]):
            writer.writerow([ctac, ctless, 1])

        # Write the group 1 data (label 1)
        for ctac, ctless in zip(file1_data[1], file2_data[1]):
            writer.writerow([ctac, ctless, 0])

# Read from the two text files

folder1='30'
folder2='15'
#folder2='d15_lmbdchdiff7_nn_CZT'

subsample_level1=30
subsample_level2=15




file1_data = read_groups_from_file(f'trainingdata_loc_a_i_sev_250_500_ext_30_60_d25_IO0_Ud32.txt')


file2_data = read_groups_from_file(f'trainingdata_loc_a_i_sev_250_500_ext_30_60_d100_IO0_Ud32.txt')

output=f'd25_d100.csv'


# Write to a CSV file
write_to_csv(file1_data, file2_data,output)

print("CSV file created successfully.")
