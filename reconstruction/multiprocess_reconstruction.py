import os
import shutil
import subprocess
from multiprocessing import Pool
import numpy as np

# Static variables
dose_levels = ['d25','d33', 'd100']
extension = [15, 30, 45, 60, 90,120]
severity = ['s100', 's175', 's250', 's500','s1000']
location = ['di', 'da']
mode = [0, 1]

# Paths
base_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data'
projection_base_hl = os.path.join(base_folder, 'projection/hl')
mod_proj_base_def = os.path.join(base_folder, 'projection_def')
mod_proj_base_hl = os.path.join(base_folder, 'projection_hl')

#patient_list_folder = os.path.join(projection_base_hl, 'dose_level_100')

CDPR_file = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file/CDRP.par'

# Utility function
def run_system(cmd):
    subprocess.run(cmd, shell=True, check=True)

# Core per-patient processing function
def process_patient(args):
    dose_level, patient_id = args
    save_folder = os.path.join(base_folder, 'mod_reconstruction', 'CTAC', patient_id)
    os.makedirs(save_folder, exist_ok=True)

    for mode_index in mode:
        if mode_index == 0:
            patient_folder = os.path.join(mod_proj_base_hl, patient_id)
            image_file_base = f"{patient_id}_{dose_level}"
            file_set = {
                'image': f"{image_file_base}.a00",
                'head': f"{image_file_base}.h00",
                'ct_img': f"{image_file_base}.ict",
                'ct_head': f"{image_file_base}.hct"
            }

            for key, fname in file_set.items():
                shutil.copy(os.path.join(patient_folder, fname), '.')

            run_system(f"smc2castor_new {file_set['head']} {image_file_base}")
            run_system(f"castor-recon_ESSE_v3 -df {image_file_base}.cdh -fout {image_file_base} "
                       f"-oit 8:8 -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 "
                       f"-atn {file_set['ct_head']} -conf /home/y.zezhang/castor/config "
                       f"-vb 1 -opti MLEM -proj classicSiddon -cdrf {CDPR_file}")

            for ext in ['_it8.img', '_it8.hdr', '.log', '.cdh', '.cdf', '.a00']:
                shutil.copy(f"{image_file_base}{ext}", save_folder)

            run_system(f"rm {image_file_base}_it8.img {image_file_base}_it8.hdr "
                       f"{image_file_base}.log {image_file_base}.cdh {image_file_base}.cdf "
                       f"{file_set['image']} castor_{image_file_base}_it2_su6.sh")
            for f in file_set.values():
                os.remove(f)

        elif mode_index == 1:
            patient_folder = os.path.join(mod_proj_base_def, patient_id)
            ict_folder = os.path.join(mod_proj_base_hl, patient_id)

            for sev in severity:
                for ext_val in extension:
                    for loc in location:
                        suffix = f"mod_proj_{loc}21{ext_val}{sev}_{patient_id}_{dose_level}"
                        files = {
                            'image': f"{suffix}.a00",
                            'head': f"{suffix}.h00",
                            'ct_img': f"{patient_id}_{dose_level}.ict",
                            'ct_head': f"{patient_id}_{dose_level}.hct"
                        }

                        for f, name in files.items():
                            src = os.path.join(patient_folder if 'ct' not in f else ict_folder, name)
                            shutil.copy(src, '.')

                        run_system(f"smc2castor_new {files['head']} {suffix}")
                        run_system(f"castor-recon_ESSE_v3 -df {suffix}.cdh -fout {suffix} "
                                   f"-oit 8:8 -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 "
                                   f"-atn {files['ct_head']} -conf /home/y.zezhang/castor/config "
                                   f"-vb 1 -opti MLEM -proj classicSiddon -cdrf {CDPR_file}")

                        for ext in ['_it8.img', '_it8.hdr', '.log', '.cdh', '.cdf', '.a00']:
                            shutil.copy(f"{suffix}{ext}", save_folder)

                        run_system(f"rm {suffix}_it8.img {suffix}_it8.hdr {suffix}.log {suffix}.cdh {suffix}.cdf "
                                   f"{files['image']} castor_{suffix}_it2_su6.sh")
                        for f in files.values():
                            os.remove(f)

# Main execution block
if __name__ == '__main__':
    pat_id_arr_fname = f'/datastore01/user-storage/y.zezhang/2025_high_dose_project/document/patient_list/patient_names06092025.txt'
    subfolders = np.loadtxt(pat_id_arr_fname, dtype = 'str', comments="#", delimiter=",", unpack=False)
    
    #subfolders = [f.name for f in os.scandir(patient_list_folder) if f.is_dir()]
    tasks = [(dose_level, patient_id) for dose_level in dose_levels for patient_id in subfolders]

    with Pool(processes=os.cpu_count() - 1) as pool:  # leave 1 core free
        pool.map(process_patient, tasks)
