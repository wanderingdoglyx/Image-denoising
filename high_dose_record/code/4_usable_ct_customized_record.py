
import pandas as pd

# Load the first Excel file
file1 = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/high_dose/filtered_ct_sessions_not_empty.xlsx'  # Replace with your actual file name
df1 = pd.read_excel(file1, usecols=['Subject'])

# Load the second Excel file
file2 = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/high_dose/high_dose patient.xlsx'  # Replace with your actual file name
df2 = pd.read_excel(file2)

# Filter df2 to only keep rows where 'Subject' appears in df1
filtered_df2 = df2[df2['Subject'].isin(df1['Subject'])]

# Optionally save the result to a new Excel file
filtered_df2.to_excel('usable_patient_customized.xlsx', index=False)

print("Filtered data saved to 'filtered_output.xlsx'")