import os
import numpy as np
from scipy.ndimage import zoom

# Configuration
input_root_base = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100'
output_root_base = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image'


patient_list = os.listdir(input_root_base)

dtype = np.float32
shape_options = [(64, 128, 128), (128, 128, 128)]

def determine_shape(file_size, dtype_size):
    num_elements = file_size // dtype_size
    for shape in shape_options:
        if np.prod(shape) == num_elements:
            return shape
    return None

def downsample(image, new_size=(64, 64)):
    z, h, w = image.shape
    zoom_factors = (1.0, new_size[0] / h, new_size[1] / w)
    return zoom(image, zoom=zoom_factors, order=1)  # bilinear interpolation

# Traverse all .ict files
for pat in patient_list:
    input_root=os.path.join(input_root_base,pat)
    output_root=os.path.join(output_root_base,pat)
    # Traverse all .ict files
    for root, _, files in os.walk(input_root):
        for file in files:
            if file.endswith('.ict'):
                input_path = os.path.join(root, file)

                # Determine relative path (excluding filename)
                rel_dir = os.path.relpath(root, input_root)
                output_dir = os.path.join(output_root, rel_dir)
                os.makedirs(output_dir, exist_ok=True)

                # Construct new filename
                base_name = os.path.splitext(file)[0]  # remove .ict
                output_file_name = f"{base_name}_atn_av.bin"
                output_path = os.path.join(output_dir, output_file_name)
                
                same_folder_output_path = os.path.join(input_root,rel_dir, output_file_name)
                
                # Read and infer shape
                with open(input_path, 'rb') as f:
                    raw = f.read()
                dtype_size = np.dtype(dtype).itemsize
                shape = determine_shape(len(raw), dtype_size)

                if shape is None:
                    print(f"Skipping {input_path}: Unknown shape")
                    continue

                # Process image
                img = np.frombuffer(raw, dtype=dtype).reshape(shape)
                img = img[::-1, :, ::-1]
                img = downsample(img, new_size=(64, 64))     # downsample
                
                img2=np.frombuffer(raw, dtype=dtype).reshape(shape)
                img2=downsample(img2, new_size=(64, 64)) 
                
                # Save to output path
                with open(output_path, 'wb') as f:
                    f.write(img.astype(dtype).tobytes())
                with open(same_folder_output_path, 'wb') as f:
                    f.write(img2.astype(dtype).tobytes())

                print(f"Processed: {input_path} → {output_path}")
                print(f"Processed: {input_path} → {same_folder_output_path}")