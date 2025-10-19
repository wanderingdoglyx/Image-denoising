import os
import numpy as np
from glob import iglob
from collections import defaultdict
import matplotlib.pyplot as plt
from pytomography.io.SPECT import simind
import matplotlib.pyplot as plt



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


#activity_scale=0.002
file = open("upscale_ratio.txt", "r")
activity_scale = float(file.read())
file.close()

simind_collimator=['ge670','siemens_symbia','philips_precedence','ge_hawkeye']
num_hl=48
#num_of_serverity=2
#num_of_extention=2
#num_of_location=3

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
                            
                            phantom_file_pri= phantom_folder+"/"+simind_collimator_index+"_tot_w1.a00"
                            phantom_file_sca= phantom_folder+"/"+simind_collimator_index+"_tot_w2.a00"
                            
                            pri_win=my_read_bin(phantom_file_pri, np.float32, [30,64,64])
                            sca_win=my_read_bin(phantom_file_sca, np.float32, [30,64,64])
                            
                            pri_win=pri_win*activity_scale
                            sca_win=sca_win*activity_scale
                            
                            create_folder(f"{save_folder}/{filename}")
                            
                            my_write_bin(f"{save_folder}/{filename}/{simind_collimator_index}_tot_w1.a00", np.float32, pri_win)
                            my_write_bin(f"{save_folder}/{filename}/{simind_collimator_index}_tot_w2.a00", np.float32, sca_win)
                            
                            
                            
                            os.system(f"cp -r {phantom_folder}/{simind_collimator_index}_tot_w1.h00 {save_folder}/{filename}/")
                            os.system(f"cp -r {phantom_folder}/{simind_collimator_index}_tot_w2.h00 {save_folder}/{filename}/")
                            os.system(f"cp -r {phantom_folder}/{filename}_atn_av.bin {save_folder}/{filename}/")
                            os.system(f"cp -r {phantom_folder}/{simind_collimator_index}.hct {save_folder}/{filename}/")
                            #os.system(f"cp -r {phantom_folder}/{simind_collimator_index}.ict {save_folder}/{filename}/")
