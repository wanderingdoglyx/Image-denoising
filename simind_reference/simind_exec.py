import numpy as np
import sys
import os
import time
#========================================
# CLA
#========================================
mode=int(sys.argv[1])
hl_index=int(sys.argv[2])
severity=int(sys.argv[3])
extension=int(sys.argv[4])
location=sys.argv[5]
gender=sys.argv[6]
simind_collimator=sys.argv[7]

#print(gender,'gender')
print(simind_collimator,'simind_collimator')

base_folder='/data01/user-storage/y.zezhang/image_trial_project'
smc_folder='/data01/user-storage/y.zezhang/image_trial_project/smc'
simind_program='/data01/user-storage/y.zezhang/simind_execute/simind'

filename_base = 'feas_param'

if mode ==0:
    filename=f'{filename_base}_md{mode}_{gender}_nr{hl_index}'
elif mode ==1:
    filename=f'{filename_base}_md{mode}_{gender}_e{extension}_s{severity}_{location}_nr{hl_index}'
 

phantom_folder=base_folder+'/phantom/'+filename
smc_file=smc_folder+'/'+simind_collimator

# copy simind_smc file to the folder
#os.system(f'cd {smc_folder}')
os.system(f'cp {smc_file} {phantom_folder}/')
os.system(f'cp {smc_folder}/scattwin.win {phantom_folder}/')

# change to phan folder
#os.system(f'cd {phantom_folder}')
#print(f'cd {phantom_folder}','phantom_folder')

start_time = time.time()
#os.system(f'echo "simind_collimator {smc_file}"')
#print(f'{simind_program} {phantom_folder}/{simind_collimator} /FD:{filename}/FS:{filename}','operation')

os.system(f'cd {phantom_folder} && {simind_program} {simind_collimator} /FD:{filename}/FS:{filename}')
end_time = time.time()
#os.system(f'echo "Elapsed time: $(( $end_time - $start_time )) sec"')
print("Elapsed time: (( ",end_time - start_time, ")) sec")

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