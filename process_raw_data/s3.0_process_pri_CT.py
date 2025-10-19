import numpy as np
from scipy.ndimage import zoom
import os
from skimage.transform import resize

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


# Function to process a single file
def process_file(input_filepath, output_filepath):

    try:
        data = my_read_bin(input_filepath, np.float32, [30, 128, 128])
        print("Read with shape [30, 128, 128]")
        compression_factor = (1, 64 / 128, 64 / 128)
        compressed_data = zoom(data, compression_factor, order=1)
        compressed_data=compressed_data*4
        
    except Exception as e:
        print(f"Failed with [30, 128, 128]: {e}")
        try:
            data = my_read_bin(input_filepath, np.float32, [60, 128, 128])
            print("Read with shape [60, 128, 128]")
            compression_factor = (30/60, 64 / 128, 64 / 128)
            compressed_data = zoom(data, compression_factor, order=1)
            compressed_data=compressed_data*8
        except Exception as e2:
            print(f"Failed with [60, 128, 128]: {e2}")
            
            try:
                data = my_read_bin(input_filepath, np.float32, [60, 64, 64])
                print("Read with shape [60, 64, 64]")
                compression_factor = (30/60, 64 / 64, 64 / 64)
                compressed_data = zoom(data, compression_factor, order=1)
                compressed_data=compressed_data*2
            except Exception as e2:
                print(f"Failed with [60, 64, 64]: {e2}")       
                try:
                    data = my_read_bin(input_filepath, np.float32, [30, 64, 64])
                    print("Read with shape [30, 64, 64]")
                    compression_factor = (30/30, 64 / 64, 64 / 64)
                    compressed_data = zoom(data, compression_factor, order=1)
                    compressed_data=compressed_data*1
                except Exception as e2:
                    print(f"Failed with [30, 64, 64]: {e2}")
                    data = None  
                    
                    
                    
  
    '''
    compression_factor = (1, 64 / 128, 64 / 128)
    compressed_data = zoom(data, compression_factor, order=1)

    compressed_data=compressed_data*4
    '''

    
    compressed_data.tofile(output_filepath)
    #my_write_bin(compressed_data, np.float32, data)
    print(f"Compressed data saved to {output_filepath}")

    
def process_CT_file(input_filepath, output_filepath):

    try:
        data = my_read_bin(input_filepath, np.float32, [64, 446, 446])
        print("Read with shape [64, 446, 446]")
        compression_factor = (1, 128 / 446, 128 / 446)
        compressed_data = zoom(data, compression_factor, order=1)
        #compressed_data=compressed_data*4
        
    except Exception as e:
        print(f"Failed with [64, 446, 446]: {e}")
        try:
            data = my_read_bin(input_filepath, np.float32, [128, 446, 446])
            print("Read with shape [128, 446, 446]")
            compression_factor = (1, 128 / 446, 128 / 446)
            compressed_data = zoom(data, compression_factor, order=1)
            #compressed_data=compressed_data*8
        except Exception as e2:
            print(f"Failed with [128, 446, 446]: {e2}")
            data = None 
            
def process_CT_file_v2(input_filepath, output_filepath):

    try:
        data = my_read_bin(input_filepath, np.float32, [64, 512, 512])
        print("Read with shape [64, 512, 512]")
        compression_factor = (1, 128 / 512, 128 / 512)
        compressed_data = zoom(data, compression_factor, order=1)
        #compressed_data=compressed_data*4
        
    except Exception as e:
        print(f"Failed with [64, 512, 512]: {e}")
        try:
            data = my_read_bin(input_filepath, np.float32, [128,512, 512])
            print("Read with shape [128, 512, 512]")
            compression_factor = (1, 128 / 512, 128 / 512)
            compressed_data = zoom(data, compression_factor, order=1)
            #compressed_data=compressed_data*8
        except Exception as e2:
            print(f"Failed with [128, 512, 512]: {e2}")
            data = None 
                                
                    
  
    '''
    compression_factor = (1, 64 / 128, 64 / 128)
    compressed_data = zoom(data, compression_factor, order=1)

    compressed_data=compressed_data*4
    '''

    
    compressed_data.tofile(output_filepath)
    #my_write_bin(compressed_data, np.float32, data)
    print(f"Compressed data saved to {output_filepath}")
    
        
    

# Define the input and output directories
input_directory = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100'
output_directory ='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100'

#output_directory = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/processed_hl/dose_level_100'

patient_list = os.listdir(input_directory )
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Process each .a00 file in the input directory
for pat_id in patient_list:
    
    input_directory_folder=os.path.join(input_directory,pat_id)
    
    for filename in os.listdir(input_directory_folder):
        if filename.endswith('.a00'):
            input_filepath = os.path.join(input_directory_folder, filename)
            output_directory_folder = os.path.join(output_directory,pat_id )
            os.makedirs(output_directory_folder, exist_ok=True)
            output_filepath = os.path.join(output_directory_folder,filename)
            process_file(input_filepath, output_filepath)
            
            
for pat_id in patient_list:
    
    input_directory_folder=os.path.join(input_directory,pat_id)
    
    for filename in os.listdir(input_directory_folder):
        if filename.endswith('.ict'):
            input_filepath = os.path.join(input_directory_folder, filename)
            output_directory_folder = os.path.join(output_directory,pat_id )
            os.makedirs(output_directory_folder, exist_ok=True)
            output_filepath = os.path.join(output_directory_folder,filename)
            process_CT_file_v2(input_filepath, output_filepath)