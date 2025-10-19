import pandas as pd
import re

# --- Extraction Functions ---
def extract_sex(text):
    if pd.isna(text):
        return None
    text = text.lower()
    if re.search(r'\b(male|man|gentleman)\b', text):
        return 'M'
    elif re.search(r'\b(female|woman|lady)\b', text):
        return 'F'
    else:
        return None

def extract_rest_dose(text):
    if pd.isna(text):
        return None
    match = re.search(r'rest:\s*([\d.]+)\s*mci', text, re.IGNORECASE)
    return float(match.group(1)) if match else None

def extract_stress_dose(text):
    if pd.isna(text):
        return None
    match = re.search(r'(pharmacologic\s+)?stress:\s*([\d.]+)\s*mci', text, re.IGNORECASE)
    return float(match.group(2)) if match else None

# --- File Paths ---
csv_path = 'M19010_RadiologyReads_16June2025.csv'       # Contains 'label', 'history', 'exam'
xlsx_path = 'usable_patient_customized_v2.xlsx'     # Contains 'Subject', 'male', 'female', 'stress dose(mCi)', 'rest dose(mCi)'

# --- Read CSV and extract info ---
df_csv = pd.read_csv(csv_path)
df_csv['subject_id'] = df_csv['label'].apply(lambda x: x.split('_')[0])
df_csv['sex'] = df_csv['history'].apply(extract_sex)
df_csv['rest_dose'] = df_csv['exam'].apply(extract_rest_dose)
df_csv['stress_dose'] = df_csv['exam'].apply(extract_stress_dose)

# --- Read Excel File ---
df_xlsx = pd.read_excel(xlsx_path)

# --- Fill the columns ---
for idx, row in df_csv.iterrows():
    subject_id = row['subject_id']
    match_idx = df_xlsx[df_xlsx['Subject'] == subject_id].index
    if not match_idx.empty:
        i = match_idx[0]
        if row['sex'] == 'M':
            df_xlsx.at[i, 'male'] = 1
        elif row['sex'] == 'F':
            df_xlsx.at[i, 'female'] = 1
        if pd.notna(row['rest_dose']):
            df_xlsx.at[i, 'rest dose(mCi)'] = row['rest_dose']
        if pd.notna(row['stress_dose']):
            df_xlsx.at[i, 'stress dose(mCi)'] = row['stress_dose']

# --- Save updated Excel ---
output_path = 'updated_file.xlsx'
df_xlsx.to_excel(output_path, index=False)

print(f"Updated file saved to: {output_path}")




#csv_path = 'M19010_RadiologyReads_16June2025.csv'  # Replace with your CSV file path