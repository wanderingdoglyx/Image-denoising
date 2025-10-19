import numpy as np
import sys
import os
import time
import shutil
#========================================
# CLA
#========================================
def simind_exec(pat_id,mode,extension,severity,location,gender,simind_collimator):

    #mode=int(sys.argv[1])
    #hl_index=int(sys.argv[2])
    #severity=int(sys.argv[3])
    #extension=int(sys.argv[4])
    #location=sys.argv[5]
    #gender=sys.argv[6]
    #simind_collimator=sys.argv[7]

    #print(gender,'gender')
    #print(simind_collimator,'simind_collimator')

    #base_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image'
    #smc_folder='/data01/user-storage/y.zezhang/smc'
    save_folder_base='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/pre_projection'
    smc_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file'
    simind_program='/data01/user-storage/y.zezhang/simind_execute/simind'

    #filename_base = 'feas_param'
    ct_base_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100'
    
    if mode ==0:
        recon_base_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC'
        
        
        pre_full_filename=f'{pat_id}_it8.img'
        pre_filename=f'{pat_id}_it8'
        
        full_filename=f'{pre_filename}_obj_act_av.bin'
        filename=f'{pre_filename}_obj'
        
        ct_name= pat_id
        ct_full_name=f'{pat_id}_atn_av.bin'

        save_folder=f'{save_folder_base}/{pat_id}/hl'        
        os.makedirs(save_folder, exist_ok=True)
        
        pre_phantom=f'{recon_base_folder}/{pat_id}/{pre_full_filename}'
        phantom=f'{save_folder}/{full_filename}'
        
        ct=f'{ct_base_folder}/{pat_id}/{ct_full_name}'
        
        shutil.copy(pre_phantom, phantom)
        
    elif mode ==1:
        #filename=f'{filename_base}_md{mode}_{gender}_e{extension}_s{severity}_{location}_nr{hl_index}'
        recon_base_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image'
    
        full_filename=f'd{location}21{extension}s{severity}_obj_act_av.bin'
        filename=f'd{location}21{extension}s{severity}_obj'
        ct_name= pat_id
        ct_full_name=f'{pat_id}_atn_av.bin'
        
        
        save_folder=f'{save_folder_base}/{pat_id}/d{location}21{extension}s{severity}'        
        os.makedirs(save_folder, exist_ok=True)
        
        phantom=f'{recon_base_folder}/{pat_id}/{ full_filename}'
        ct=f'{ct_base_folder}/{pat_id}/{ct_full_name}'
        
        os.system(f'cp -r {phantom} {save_folder}/')
        
        
        smc_file=smc_folder+'/'+'simind_smc.smc'
            
            

            


        
    os.system(f'cp -r {smc_file} {save_folder}/')
    os.system(f'cp -r {smc_folder}/scattwin.win {save_folder}/')
    os.system(f'cp -r {ct} {save_folder}/')
    
    # change to phan folder
    #os.system(f'cd {phantom_folder}')
    #print(f'cd {phantom_folder}','phantom_folder')
    
    #scale_fector=0.004913

    #start_time = time.time()
    #os.system(f'echo "simind_collimator {smc_file}"')
    #print(f'{simind_program} {phantom_folder}/{simind_collimator} /FD:{filename}/FS:{filename}','operation')

    #os.system(f'cd {phantom_folder} && {simind_program} {simind_collimator} /FD:{filename}/FS:{filename}/NN:{scale_fector}')
    
    os.system(f'cd {save_folder} && {simind_program} {simind_collimator} /FD:{ct_name}/FS:{filename}')
    #end_time = time.time()
    
    #os.system(f'echo "Elapsed time: $(( $end_time - $start_time )) sec"')
    #print("Elapsed time: (( ",end_time - start_time, ")) sec")
    
    
    #os.system(f'rm {save_folder}/{simind_collimator}')
    #os.system(f'rm {save_folder}/scattwin.win')

'''
  if [ $organ_id -ne 1 ]
  then
    rm o${cur_organ}_nr${ind_nr}.ict
    rm o${cur_organ}_nr${ind_nr}.hct
    rm ${cur_organ}_nr${ind_nr}_act_av.bin

  fi

  rm o${cur_organ}_nr${ind_nr}.res
  rm o${cur_organ}_nr${ind_nr}.csv
  rm o${cur_organ}_nr${ind_nr}.bis
  rm o${cur_organ}_nr${ind_nr}_tot_w2*
  rm o${cur_organ}_nr${ind_nr}_tew_w3*
  rm o${cur_organ}_nr${ind_nr}_tot_w4*  
'''