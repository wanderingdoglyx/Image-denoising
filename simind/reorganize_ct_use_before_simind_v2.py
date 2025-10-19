import os
import numpy as np
from scipy.ndimage import zoom

# Configuration
input_root_base = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100'
output_root_base = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image'

dtype = np.float32
shape_options = [(64, 128, 128), (128, 128, 128)]  # allowed shapes

def determine_shape(file_size, dtype_size):
    num_elements = file_size // dtype_size
    for shape in shape_options:
        if np.prod(shape) == num_elements:
            return shape
    return None

def downsample(image, new_size=(64, 64), target_slices=None):
    z, h, w = image.shape
    if target_slices is None:
        target_slices = z  # keep original z if not specified
    zoom_factors = (target_slices / z, new_size[0] / h, new_size[1] / w)
    return zoom(image, zoom=zoom_factors, order=1)  # bilinear interpolation

# Traverse patient folders
for pat in os.listdir(input_root_base):
    input_root = os.path.join(input_root_base, pat)
    output_root = os.path.join(output_root_base, pat)

    for root, _, files in os.walk(input_root):
        for file in files:
            if not file.endswith('.ict'):
                continue

            input_path = os.path.join(root, file)

            # Determine shape
            with open(input_path, 'rb') as f:
                raw = f.read()
            dtype_size = np.dtype(dtype).itemsize
            shape = determine_shape(len(raw), dtype_size)
            if shape is None:
                print(f"Skipping {input_path}: Unknown shape")
                continue

            # Read original image
            img_original = np.frombuffer(raw, dtype=dtype).reshape(shape)

            # If shape is (128, 128, 128), reduce to 64 slices
            target_slices = 64 if shape[0] == 128 else shape[0]

            # Downsample both versions
            #img_down = downsample(img_original, new_size=(64, 64), target_slices=target_slices) * 0.68
            img_flipped = img_original[::-1, :, ::-1]
            img_flipped_down = downsample(img_flipped, new_size=(64, 64), target_slices=target_slices) * 0.68

            # Output paths
            rel_dir = os.path.relpath(root, input_root)
            output_dir = os.path.join(output_root, rel_dir)
            os.makedirs(output_dir, exist_ok=True)

            base_name = os.path.splitext(file)[0]
            output_file_name = f"{base_name}_atn_av.bin"

            output_path = os.path.join(output_dir, output_file_name)  # flipped version
            same_folder_output_path = os.path.join(root, output_file_name)  # unflipped version

            # Save
            with open(output_path, 'wb') as f:
                f.write(img_flipped_down.astype(dtype).tobytes())
            with open(same_folder_output_path, 'wb') as f:
                f.write(img_flipped_down.astype(dtype).tobytes())

            print(f"Processed flipped: {input_path} → {output_path}")
            print(f"Processed original: {input_path} → {same_folder_output_path}")
