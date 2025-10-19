import os
import numpy as np
from scipy.ndimage import zoom

def resize_to_512x512(volume):
    x, h, w = volume.shape
    if (h, w) == (512, 512):
        return volume  # already correct shape

    zoom_factors = [1, 512 / h, 512 / w]
    resized = zoom(volume, zoom_factors, order=1)  # linear interpolation
    return resized

def guess_shape_and_reshape(flat_data):
    size = flat_data.size
    possible_shapes = [
        (64, 64, 64),
        (64, 446, 446),
        (64, 512, 512),
        (128, 64, 64),
        (128, 446, 446),
        (128, 512, 512),
        (128,128,128),
        (64,128,128)
    ]

    for shape in possible_shapes:
        if np.prod(shape) == size:
            return flat_data.reshape(shape)

    return None  # Unknown shape

def process_ict_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            flat_data = np.fromfile(f, dtype=np.float32)

        volume = guess_shape_and_reshape(flat_data)

        if volume is None:
            print(f"Skipping {filepath}: unknown or unsupported shape")
            return

        if volume.shape[1:] == (512, 512):
            print(f"Skipping {filepath}: already (x,512,512)")
            return

        volume_resized = resize_to_512x512(volume)

        with open(filepath, 'wb') as f:
            volume_resized.astype(np.float32).tofile(f)

        print(f"Processed {filepath}: shape {volume.shape} -> {volume_resized.shape}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.ict'):
                filepath = os.path.join(dirpath, filename)
                process_ict_file(filepath)



if __name__ == "__main__":
    root_folder = "/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl_v2/dose_level_100"
    process_directory(root_folder)


    