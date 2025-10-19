
import pandas as pd

# Load both Excel files
df_high_dose = pd.read_excel("/datastore01/user-storage/y.zezhang/2025_high_dose_project/high_dose/high-dose patient.xlsx")
df_filtered = pd.read_excel("filtered_ct_sessions_not_empty.xlsx")

# Get list of subject IDs from high-dose file
high_dose_subjects = df_high_dose['Subject'].astype(str).str.strip()

# Filter rows in df_filtered where subject is in high_dose_subjects
df_matching = df_filtered[df_filtered['Subject'].astype(str).str.strip().isin(high_dose_subjects)]

# Combine the original high-dose data with the matching new rows
df_combined = pd.concat([df_high_dose, df_matching], ignore_index=True)

# Save to a new Excel file
df_combined.to_excel("updated_high_dose_patients.xlsx", index=False)

print("Combined data saved to 'updated_high_dose_patients.xlsx'")