import pandas as pd

# Read the CSV file
df = pd.read_csv("zezhang_4_6_2025_23_33_29.CSV")

# Convert the "inserted" column to datetime format
df['Inserted'] = pd.to_datetime(df['Inserted'], errors='coerce')

# Filter rows where the year is 2025
df_2025 = df[df['Inserted'].dt.year == 2025]

# Save the filtered data to a new Excel file
df_2025.to_excel("filtered_2025_data.xlsx", index=False)

print("Filtered data saved to 'filtered_2025_data.xlsx'")