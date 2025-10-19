import os
import time 
import multiprocessing
import simind_exec2





processes = []



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


#severity=[25]
#extension=[30]
#location=['anterior']
#gender=['female']

for mode_index in mode:
    if mode_index==0:
        for num_hl_index in range(num_hl):
            for gender_index in gender:
                for simind_collimator_index in simind_collimator:
                    p = multiprocessing.Process(target=simind_exec2.simind_exec,args=(mode_index,num_hl_index,extension[0],severity[0],location[0],gender_index,simind_collimator_index))
                    if __name__ == "__main__":
                        p.start()
                        processes.append(p)

    elif mode_index==1:   
        for num_hl_index in range(num_hl):
            for severity_index in severity:
                for extension_index in extension:
                    for location_index in location:
                        for gender_index in gender:
                            for simind_collimator_index in simind_collimator:
                                    p = multiprocessing.Process(target=simind_exec2.simind_exec,args=(mode_index,num_hl_index,extension_index,severity_index,location_index,gender_index,simind_collimator_index))
                                    if __name__ == "__main__":
                                        p.start()
                                        processes.append(p)

for p in processes:
    p.join()
