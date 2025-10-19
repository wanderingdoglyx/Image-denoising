import os

simind_collimator=['GE670.smc','Siemens_Symbia.smc','Philips_Precedence.smc','GE_Hawkeye.smc']
num_hl=48
#num_of_serverity=2
#num_of_extention=2
#num_of_location=3

mode=[0,1]
severity=[25,50]
extension=[30,60]
location=['anterior','lateral','inferior']
gender=['male','female']

mode=[0]
severity=[25]
extension=[30]
location=['anterior']
gender=['female']

for mode_index in mode:
    for num_hl_index in range(num_hl):
        for severity_index in severity:
            for extension_index in extension:
                for location_index in location:
                    for gender_index in gender:
                        for simind_collimator_index in simind_collimator:
                            os.system(f'screen -d -m -S simind_sys{mode_index}_{num_hl_index}_s{severity_index}_e{extension_index}_{location_index}_{gender_index}_{simind_collimator_index}')
                            os.system('sleep 3s')
                            os.system(f'screen -r simind_sys{mode_index}_{num_hl_index}_s{severity_index}_e{extension_index}_{location_index}_{gender_index}_{simind_collimator_index} -X exec python3 /home/y.zezhang/20240110image_trial_simind/simind/simind_exec.py {mode_index} {num_hl_index} {severity_index} {extension_index} {location_index} {gender_index} {simind_collimator_index}')


            

