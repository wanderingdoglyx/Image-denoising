import os
import numpy as np

def my_read_bin(cur_inp_file, data_type, input_shape):
  A = np.fromfile(cur_inp_file, dtype = data_type)
  A[np.isnan(A)] = 0
  A = np.reshape(A, input_shape)
  #A = np.transpose(A, [2, 1, 0])
  return A


def my_write_bin(cur_out_file, data_type, data):
  #data = np.transpose(data, [2, 1, 0])
  data.astype(data_type).tofile(cur_out_file)
  return


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


simind_collimator=['ge670','siemens_symbia','philips_precedence','ge_hawkeye']
num_hl=48

mode=[0,1]
severity=[25,50]
extension=[30,60]
location=['anterior','lateral','inferior']
gender=['male','female']

   
for mode_index in mode:   
    for severity_index in severity:
        for extension_index in extension:
            for location_index in location:
                for gender_index in gender:
                    for simind_collimator_index in simind_collimator:
                        for hl_index in range(num_hl):

                        
                            base_folder="/data01/user-storage/y.zezhang/image_trial_project"                            
                            save_folder="/data01/user-storage/y.zezhang/image_trial_project/phantom_upscale"                            
                            filename_base = "feas_param"


                            if mode_index ==0:
                                filename=f'{filename_base}_md{mode_index}_{gender_index}_nr{hl_index}'
                            elif mode_index ==1:
                                filename=f'{filename_base}_md{mode_index}_{gender_index}_e{extension_index}_s{severity_index}_{location_index}_nr{hl_index}'
                            

                            phantom_folder=base_folder+"/phantom/"+filename
                            
                            ct_file=phantom_folder+"/"+ simind_collimator_index+".ict"
                            
                            ct=my_read_bin(ct_file,np.float32, [64,64,64])
                            ct= np.transpose(ct, [0, 2, 1])
                            
                            my_write_bin(f"{save_folder}/{filename}/{simind_collimator_index}.ict", np.float32, ct)
                                                                                        
