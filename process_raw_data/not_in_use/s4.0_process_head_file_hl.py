import os
import numpy as np
import shutil


#h00                

# Example usage
head_file_folder_path = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file' 
save_path='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100'
patient_list=os.listdir('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100') 


for patient in patient_list:
    
    hl_head_file_name='mod_proj_da2130s100_obj_01927022_d1.h00'
    
    head_file=f'{head_file_folder_path}/{hl_head_file_name}'
    
    # Copy the header file to the destination folder
    new_head_file_name=f'{patient}.h00'
    dest_file_path = os.path.join(save_path,patient,new_head_file_name)
    shutil.copy2(head_file, dest_file_path)
    
    # Modify the copied header file in the destination folder
    with open(dest_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(dest_file_path, 'w') as file:
        for line in lines:
            if line.strip() == f'!name of data file := mod_proj_da2130s100_obj_01927022_d1.a00':
                file.write(f'!name of data file := {patient}.a00\n')
            elif line.strip() == f'patient name := SMC_mod_proj_da2130s100_obj_01927022_d1.a00':
                file.write(f'patient name := SMC_mod_{patient}.a00\n')
            else:
                file.write(line)

### .hct    


for patient in patient_list:
    
    ct_hl_head_file_name='ct.hct'
    
    ct_head_file=f'{head_file_folder_path}/{ct_hl_head_file_name}'
    
    # Copy the header file to the destination folder
    ct_new_head_file_name=f'{patient}.hct'
    ct_dest_file_path = os.path.join(save_path,patient,ct_new_head_file_name)
    shutil.copy2(ct_head_file, ct_dest_file_path)
    
    # Modify the copied header file in the destination folder
    with open(ct_dest_file_path, 'r') as file:
        lines = file.readlines()
    
    with open(ct_dest_file_path, 'w') as file:
        for line in lines:
            if line.strip() == f'!name of data file := mod_proj_da2130s100_obj_01927022_d1.a00':
                file.write(f'!name of data file := {patient}.a00\n')
            elif line.strip() == f'patient name := SMC_mod_proj_da2130s100_obj_01927022_d1.a00':
                file.write(f'patient name := SMC_mod_{patient}.a00\n')
            else:
                file.write(line)
  
