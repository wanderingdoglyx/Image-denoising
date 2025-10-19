import os
import time 
import multiprocessing
import simind_exec3


processes = []



#simind_collimator=['GE670.smc','Siemens_Symbia.smc','Philips_Precedence.smc','GE_Hawkeye.smc']
simind_collimator=['simind_smc.smc']
num_hl=48
#num_of_serverity=2
#num_of_extention=2
#num_of_location=3

'''
mode=[1,0]
severity=[25,50]
extension=[30,60]
location=['inferior','lateral','anterior']
gender=['male','female']
'''

real_patient_data_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC"

mode=[1]

severity=[0, 100, 150 ,175, 250, 330,375, 400, 500, 750,1000] #total
extension=[15, 30, 45, 60,90,120] #total

#location=['Ant', 'Inf', 'Lat', 'Sep', 'TAnt', 'TInf']
#location=['A', 'I', 'L', 'S', 'TA', 'TI', 'AL', 'IL']
location=['A', 'I']
#gender=['male','female']
gender=['male']

patient_list = os.listdir(real_patient_data_path)
patient_list.reverse()
patient_list=patient_list
patient_list=patient_list[600:]

def initial_simind_pipline(pat_id,mode_index,extension,severity,location,gender_index,simind_collimator_index):
    
  
    if mode_index==0:

                    p = multiprocessing.Process(target=simind_exec3.simind_exec,args=(pat_id,mode_index,extension_index,severity_index,location_index,gender_index,simind_collimator_index))
                    if __name__ == "__main__":
                        p.start()
                        processes.append(p)

    elif mode_index==1:   
        for severity_index in severity:
            for extension_index in extension:
                for location_index in location:
                    p = multiprocessing.Process(target=simind_exec3.simind_exec,args=(pat_id,mode_index,extension_index,severity_index,location_index,gender_index,simind_collimator_index))
                    if __name__ == "__main__":
                        p.start()
                        processes.append(p)

    for p in processes:
        p.join()




#########################################################
for mode_index in mode:   
    if  mode_index==0:
        for gender_index in gender:
            for pat_id in patient_list:
                for simind_collimator_index in simind_collimator:
                    initial_simind_pipline(pat_id,mode_index,'none','none','none',gender_index,simind_collimator_index) 
                    
    elif mode_index==1:
      #  for severity_index in severity:
      #      for extension_index in extension:
      #          for location_index in location:
                    for gender_index in gender:
                        for simind_collimator_index in simind_collimator:
                            for pat_id in patient_list:
                                initial_simind_pipline(pat_id,mode_index,extension,severity,location,gender_index,simind_collimator_index)
                    