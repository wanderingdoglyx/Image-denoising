import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
import os
from tempfile import TemporaryFile
import pandas as pd
import shutil 
import pydicom


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

dose_level='dose_level_100'

outputFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2'

# Get the list of target patient 
hl_patient_list_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments_v2"
hl_patient_list = os.listdir(hl_patient_list_path)

# Get the list of patient data and directories
real_patient_data_path = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_v2"
patient_list = os.listdir(real_patient_data_path)

# select useful_data
useful_patient_list=[]
for hl_patient in hl_patient_list:
  for count, ele in enumerate(patient_list):
      if hl_patient in ele and 'PriPrj' in ele:
        
          #useful_patient_list.append(ele)
          useful_patient_path=os.path.join(real_patient_data_path, ele)
          patient_file_list = os.listdir(useful_patient_path)
          patient_file_list.remove('metacache.mim')
          patient_file=os.path.join(useful_patient_path, patient_file_list[0])  
          ds = dicom.dcmread(patient_file)
          
          Real_World_Value_Intercept=ds[0x00409096][0][0x00409224].value
          Real_World_Value_Slope=ds[0x00409096][0][0x00409225].value
          
          real_patient_image=ds.pixel_array*Real_World_Value_Slope+Real_World_Value_Intercept
          
          tem_fname=hl_patient+'.a00'
          #current_outputfolder=os.path.join(outputFolder, hl_patient)
          
          os.makedirs(outputFolder, exist_ok=True)
          outputFileName = os.path.join(outputFolder, dose_level, hl_patient)
          os.makedirs(outputFileName, exist_ok=True)
          outputFileName = os.path.join(outputFileName, tem_fname)
          my_write_bin(outputFileName, np.float32, real_patient_image)


'''
      if hl_patient  in ele and 'RegCT' in ele:
        
                
        useful_patient_path=os.path.join(real_patient_data_path, ele)
        # patient_file_list = os.listdir(useful_patient_path)
        #patient_file_list.remove('metacache.mim')
        #patient_file_list=sorted(patient_file_list)
        
        
        ct_dicom_files = [os.path.join(useful_patient_path, f) for f in os.listdir(useful_patient_path) if f.endswith('.dcm')]
        
        files_with_slice_location = []
        for ct_file in ct_dicom_files:
            ct_ds = dicom.dcmread(ct_file)
            if 'SliceLocation' in ct_ds:
                slice_location = ct_ds.SliceLocation
                files_with_slice_location.append((ct_file, slice_location))
            else:
                print(f"File {ct_file} does not contain Slice Location and will be ignored.")
  
        # use mip 
        # imgconv -rR input.dcm output.ictac
        
        # Sort files by Slice Location
        
        files_with_slice_location.sort(key=lambda x: x[1])
        
        images = []
        for ct_file, _ in files_with_slice_location:
          
          ct_file_path=os.path.join(useful_patient_path, ct_file)
          ct_ds = dicom.dcmread(ct_file_path)
          images.append(ct_ds.pixel_array.astype(np.float32))
          #current_outputfolder=os.path.join(outputFolder, hl_patient)
          os.makedirs(outputFolder, exist_ok=True)
          outputFileName = os.path.join(outputFolder, dose_level, hl_patient)
          #outputFileName = os.path.join(outputFolder, hl_patient)
          os.makedirs(outputFileName, exist_ok=True)
          outputFileName = os.path.join(outputFileName, hl_patient+'_ct.ict')
            
        my_write_bin(outputFileName,np.float32,np.array(images))
        
 '''  


    