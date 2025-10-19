
import pandas as pd

df = pd.read_excel("/datastore01/user-storage/y.zezhang/2025_high_dose_project/high_dose/filtered_2025_data.xlsx")



# Filter rows where 'CT Sessions' is not empty or NaN
df_non_empty = df[df['CT Sessions'].notna()]

# Save the filtered data to a new Excel file
df_non_empty.to_excel("filtered_ct_sessions_not_empty.xlsx", index=False)

print("Filtered data saved to 'filtered_ct_sessions_not_empty.xlsx'")