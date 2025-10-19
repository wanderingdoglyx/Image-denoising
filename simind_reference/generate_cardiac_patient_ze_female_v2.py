'''
@desc: generate a parameter file with random parameters for XCAT phantom
'''
from io import RawIOBase
import numpy as np
import sys
from random import randrange
import scipy.io as sio
import os
from scipy.stats import truncnorm
from scipy.stats import skewnorm


general_samp = 'general.samp.par'

#========================================
# Log
#========================================
# changed all unknown organs to background
# saving all data a to npy format

#========================================
# To Do
#========================================
# skin layer to control fatness
# Bloodpool activity: how to choose
# Heart rotations inside human
# use breaast setting in female phantom
#========================================


version = 14



#========================================
# FUNCION: truncated normal distribution
#========================================
def trnrm(mu, sigma, lower, upper, N):
	return truncnorm.rvs((lower - mu)/sigma, (upper - mu)/sigma, loc=mu, scale=sigma, size=N)


#========================================
# FUNCION: skewed normal distribution
#========================================
def output_phantom(mode,ThetaCenter, ThetaWidth, XCenterIndex, XWidthIndex, Wall_fract, motion_scale, border_zone_long, border_zone_radial,
                    core_xcat_folder,gender,gender_number,color_code,lung_scale,lv_radius_scale,lv_length_scale,phantom_height_scale,
                    torso_long_axis_scale,torso_short_axis_scale,breast_type,which_breast,rbreast_long_axis_scale,rbreast_short_axis_scale,
                    rbreast_height_scale,lbreast_long_axis_scale,lbreast_short_axis_scale,lbreast_height_scale,skin_thick_scale,pixel_width,slice_width,array_size,
                    startslice,endslice,myoLV_act,myoRV_act,myoLA_act,myoRA_act,trnrm_bg,liver_act,lung_act,defect_severity_scale,filename):
    
    
    command='./dxcat2_linux_64bit ./Ze_par/cardiac_patient.par '\
            f'--mode {mode} --ThetaCenter {ThetaCenter} --ThetaWidth {ThetaWidth} --XCenterIndex {XCenterIndex} '\
            f'--XWidthIndex {XWidthIndex} --Wall_fract {Wall_fract} --motion_scale {motion_scale} --border_zone_long {border_zone_long} --border_zone_radial {border_zone_radial} '\
            f'--heart_base {core_xcat_folder}v{gender}50_heart.nrb --heart_curve_file {core_xcat_folder}heart_curve.txt --dia_filename {core_xcat_folder}diaphragm_curve.dat '\
            f'--ap_filename {core_xcat_folder}ap_curve.dat --gender {gender_number} --organ_file {core_xcat_folder}v{gender}50.nrb '\
            f'--color_code {color_code} --lung_scale {lung_scale} --lv_radius_scale {lv_radius_scale} --lv_length_scale {lv_length_scale} '\
            f'--phantom_height_scale {phantom_height_scale} --torso_long_axis_scale {torso_long_axis_scale} --torso_short_axis_scale {torso_short_axis_scale} '\
            f'--breast_type {breast_type} --which_breast {which_breast} --rbreast_long_axis_scale {rbreast_long_axis_scale} --rbreast_short_axis_scale {rbreast_short_axis_scale} '\
            f'--rbreast_height_scale {rbreast_height_scale} --lbreast_long_axis_scale {lbreast_long_axis_scale} --lbreast_short_axis_scale {lbreast_short_axis_scale} --lbreast_height_scale {lbreast_height_scale} '\
            f'--thickness_skin {skin_thick_scale} --pixel_width {pixel_width} --slice_width {slice_width} --array_size{array_size} --startslice {startslice} --endslice {endslice} '\
            f'--myoLV_act {myoLV_act} --myoRV_act {myoRV_act} --myoLA_act {myoLA_act} --myoRA_act {myoRA_act} '\
            f'--bldplLV_act {trnrm_bg} --bldplRV_act {trnrm_bg} --bldplLA_act {trnrm_bg} --bldplRA_act {trnrm_bg} '\
            f'--coronary_art_activity {trnrm_bg} --coronary_vein_activity {trnrm_bg} --body_activity {trnrm_bg} --skin_activity {trnrm_bg} '\
            f'--rbreast_activity {trnrm_bg} --lbreast_activity {trnrm_bg} --muscle_activity {trnrm_bg} --liver_activity {liver_act} '\
            f'--r_lung_activity {lung_act} --l_lung_activity {lung_act} --esophagus_activity {trnrm_bg} --esophagus_cont_activity {trnrm_bg} '\
            f'--laryngopharynx_activity {trnrm_bg} --larynx_activity {trnrm_bg} --st_wall_activity {trnrm_bg} --st_cnts_activity {trnrm_bg} '\
            f'--pancreas_activity {trnrm_bg} --adrenal_activity {trnrm_bg} --r_renal_pelvis_activity {trnrm_bg} --l_renal_pelvis_activity {trnrm_bg} '\
            f'--spleen_activity {trnrm_bg} --rib_activity {trnrm_bg} --cortical_bone_activity {trnrm_bg} --spine_activity {trnrm_bg} --spinal_cord_activity {trnrm_bg} '\
            f'--bone_marrow_activity {trnrm_bg} --art_activity {trnrm_bg} --vein_activity {trnrm_bg} --bladder_activity {trnrm_bg} --prostate_activity {trnrm_bg} '\
            f'--asc_li_activity {trnrm_bg} --trans_li_activity {trnrm_bg} --desc_li_activity {trnrm_bg} --sm_intest_activity {trnrm_bg} --rectum_activity {trnrm_bg} '\
            f'--sem_activity {trnrm_bg} --vas_def_activity {trnrm_bg} --test_activity {trnrm_bg} --penis_activity {trnrm_bg} --epididymus_activity {trnrm_bg} '\
            f'--ejac_duct_activity {trnrm_bg} --pericardium_activity {trnrm_bg} --cartilage_activity {trnrm_bg} --intest_air_activity {trnrm_bg} --ureter_activity {trnrm_bg} '\
            f'--urethra_activity {trnrm_bg} --lymph_activity {trnrm_bg} --lymph_abnormal_activity {trnrm_bg} --trach_bronch_activity {trnrm_bg} --airway_activity {trnrm_bg} '\
            f'--uterus_activity {trnrm_bg} --vagina_activity {trnrm_bg} --right_ovary_activity {trnrm_bg} --left_ovary_activity {trnrm_bg} --fallopian_tubes_activity {trnrm_bg} '\
            f'--parathyroid_activity {trnrm_bg} --thyroid_activity {trnrm_bg} --thymus_activity {trnrm_bg} --salivary_activity {trnrm_bg} --pituitary_activity {trnrm_bg} '\
            f'--eye_activity {trnrm_bg} --lens_activity {trnrm_bg} '\
            f'--lesn_activity {myoRV_act/defect_severity_scale} --atten_table_filename {core_xcat_folder}atten_table.dat '\
            f'./phantom/female/{filename}'
            
    os.system(command)

##
def output_phantom_no_color_code(mode,ThetaCenter, ThetaWidth, XCenterIndex, XWidthIndex, Wall_fract, motion_scale, border_zone_long, border_zone_radial,
                core_xcat_folder,phantom_folder,gender,gender_number,color_code,lung_scale,lv_radius_scale,lv_length_scale,phantom_height_scale,
                torso_long_axis_scale,torso_short_axis_scale,breast_type,which_breast,rbreast_long_axis_scale,rbreast_short_axis_scale,
                rbreast_height_scale,lbreast_long_axis_scale,lbreast_short_axis_scale,lbreast_height_scale,skin_thick_scale,pixel_width,slice_width,array_size,
                startslice,endslice,myoLV_act,myoRV_act,myoLA_act,myoRA_act,trnrm_bg,liver_act,lung_act,defect_severity_scale,filename):


    command='./dxcat2_linux_64bit ./Ze_par/cardiac_patient.par '\
        f'--act_phan_each 1 --atten_phan_each 1 '\
        f'--mode {mode} --ThetaCenter {ThetaCenter} --ThetaWidth {ThetaWidth} --XCenterIndex {XCenterIndex} '\
        f'--XWidthIndex {XWidthIndex} --Wall_fract {Wall_fract} --motion_scale {motion_scale} --border_zone_long {border_zone_long} --border_zone_radial {border_zone_radial} '\
        f'--heart_base {core_xcat_folder}v{gender}50_heart.nrb --heart_curve_file {core_xcat_folder}heart_curve.txt --dia_filename {core_xcat_folder}diaphragm_curve.dat '\
        f'--ap_filename {core_xcat_folder}ap_curve.dat --gender {gender_number} --organ_file {core_xcat_folder}v{gender}50.nrb '\
        f'--lung_scale {lung_scale} --lv_radius_scale {lv_radius_scale} --lv_length_scale {lv_length_scale} '\
        f'--phantom_height_scale {phantom_height_scale} --torso_long_axis_scale {torso_long_axis_scale} --torso_short_axis_scale {torso_short_axis_scale} '\
        f'--breast_type {breast_type} --which_breast {which_breast} --rbreast_long_axis_scale {rbreast_long_axis_scale} --rbreast_short_axis_scale {rbreast_short_axis_scale} '\
        f'--rbreast_height_scale {rbreast_height_scale} --lbreast_long_axis_scale {lbreast_long_axis_scale} --lbreast_short_axis_scale {lbreast_short_axis_scale} --lbreast_height_scale {lbreast_height_scale} '\
        f'--thickness_skin {skin_thick_scale} --pixel_width {pixel_width} --slice_width {slice_width} --array_size {array_size} --startslice {startslice} --endslice {endslice} '\
        f'--myoLV_act {myoLV_act} --myoRV_act {myoRV_act} --myoLA_act {myoLA_act} --myoRA_act {myoRA_act} '\
        f'--bldplLV_act {trnrm_bg} --bldplRV_act {trnrm_bg} --bldplLA_act {trnrm_bg} --bldplRA_act {trnrm_bg} '\
        f'--coronary_art_activity {trnrm_bg} --coronary_vein_activity {trnrm_bg} --body_activity {trnrm_bg} --skin_activity {trnrm_bg} '\
        f'--rbreast_activity {trnrm_bg} --lbreast_activity {trnrm_bg} --muscle_activity {trnrm_bg} --liver_activity {liver_act} '\
        f'--r_lung_activity {trnrm_bg} --l_lung_activity {trnrm_bg} --esophagus_activity {trnrm_bg} --esophagus_cont_activity {trnrm_bg} '\
        f'--laryngopharynx_activity {trnrm_bg} --larynx_activity {trnrm_bg} --st_wall_activity {trnrm_bg} --st_cnts_activity {trnrm_bg} '\
        f'--pancreas_activity {trnrm_bg} --adrenal_activity {trnrm_bg} --r_renal_pelvis_activity {trnrm_bg} --l_renal_pelvis_activity {trnrm_bg} '\
        f'--spleen_activity {trnrm_bg} --rib_activity {trnrm_bg} --cortical_bone_activity {trnrm_bg} --spine_activity {trnrm_bg} --spinal_cord_activity {trnrm_bg} '\
        f'--bone_marrow_activity {trnrm_bg} --art_activity {trnrm_bg} --vein_activity {trnrm_bg} --bladder_activity {trnrm_bg} --prostate_activity {trnrm_bg} '\
        f'--asc_li_activity {trnrm_bg} --trans_li_activity {trnrm_bg} --desc_li_activity {trnrm_bg} --sm_intest_activity {trnrm_bg} --rectum_activity {trnrm_bg} '\
        f'--sem_activity {trnrm_bg} --vas_def_activity {trnrm_bg} --test_activity {trnrm_bg} --penis_activity {trnrm_bg} --epididymus_activity {trnrm_bg} '\
        f'--ejac_duct_activity {trnrm_bg} --pericardium_activity {trnrm_bg} --cartilage_activity {trnrm_bg} --intest_air_activity {trnrm_bg} --ureter_activity {trnrm_bg} '\
        f'--urethra_activity {trnrm_bg} --lymph_activity {trnrm_bg} --lymph_abnormal_activity {trnrm_bg} --trach_bronch_activity {trnrm_bg} --airway_activity {trnrm_bg} '\
        f'--uterus_activity {trnrm_bg} --vagina_activity {trnrm_bg} --right_ovary_activity {trnrm_bg} --left_ovary_activity {trnrm_bg} --fallopian_tubes_activity {trnrm_bg} '\
        f'--parathyroid_activity {trnrm_bg} --thyroid_activity {trnrm_bg} --thymus_activity {trnrm_bg} --salivary_activity {trnrm_bg} --pituitary_activity {trnrm_bg} '\
        f'--eye_activity {trnrm_bg} --lens_activity {trnrm_bg} '\
        f'--gall_bladder_activity {trnrm_bg} --r_kidney_cortex_activity {trnrm_bg} '\
        f'--r_kidney_medulla_activity {trnrm_bg} --l_kidney_cortex_activity {trnrm_bg} --l_kidney_medulla_activity {trnrm_bg} '\
        f'--lesn_activity {myoRV_act/defect_severity_scale} --atten_table_filename {core_xcat_folder}atten_table.dat '\
        f'{phantom_folder}/{filename}'
        #f'./phantom/female/{filename}'                    
    os.system(command) 

##
def test(mode,ThetaCenter, ThetaWidth, XCenterIndex, XWidthIndex, Wall_fract, motion_scale, border_zone_long, border_zone_radial,
                core_xcat_folder,gender,gender_number,color_code,lung_scale,lv_radius_scale,lv_length_scale,phantom_height_scale,
                torso_long_axis_scale,torso_short_axis_scale,breast_type,which_breast,rbreast_long_axis_scale,rbreast_short_axis_scale,
                rbreast_height_scale,lbreast_long_axis_scale,lbreast_short_axis_scale,lbreast_height_scale,skin_thick_scale,pixel_width,slice_width,array_size,
                startslice,endslice,myoLV_act,myoRV_act,myoLA_act,myoRA_act,trnrm_bg,liver_act,lung_act,defect_severity_scale,filename):


    command='./dxcat2_linux_64bit ./Ze_par/cardiac_patient.par '\
        f'--act_phan_each 1 --atten_phan_each 1 '\
        f'--mode {mode} --ThetaCenter {ThetaCenter} --ThetaWidth {ThetaWidth} --XCenterIndex {XCenterIndex} '\
        f'--XWidthIndex {XWidthIndex} --Wall_fract {Wall_fract} --motion_scale {motion_scale} --border_zone_long {border_zone_long} --border_zone_radial {border_zone_radial} '\
        f'--heart_base {core_xcat_folder}v{gender}50_heart.nrb --heart_curve_file {core_xcat_folder}heart_curve.txt --dia_filename {core_xcat_folder}diaphragm_curve.dat '\
        f'--ap_filename {core_xcat_folder}ap_curve.dat --gender {gender_number} --organ_file {core_xcat_folder}v{gender}50.nrb '\
        f'--lung_scale {lung_scale} --lv_radius_scale {lv_radius_scale} --lv_length_scale {lv_length_scale} '\
        f'--phantom_height_scale {phantom_height_scale} --torso_long_axis_scale {torso_long_axis_scale} --torso_short_axis_scale {torso_short_axis_scale} '\
        f'--breast_type {breast_type} --which_breast {which_breast} --rbreast_long_axis_scale {rbreast_long_axis_scale} --rbreast_short_axis_scale {rbreast_short_axis_scale} '\
        f'--rbreast_height_scale {rbreast_height_scale} --lbreast_long_axis_scale {lbreast_long_axis_scale} --lbreast_short_axis_scale {lbreast_short_axis_scale} --lbreast_height_scale {lbreast_height_scale} '\
        f'--thickness_skin {skin_thick_scale} --pixel_width {pixel_width} --slice_width {slice_width} --array_size {array_size} --startslice {startslice} --endslice {endslice} '\
        f'./phantom/female/{filename}'
        
    os.system(command) 
    

def sknrm(alpha, loc, scale, N):
    return skewnorm.rvs(alpha, loc, scale, N)

#================================================
# FUNCTION: limit LV dimensions by min and max
#================================================
def limit_lv_dim( lv_radius_scale_arr, lv_length_scale_arr, lv_radius_default, lv_length_default, lv_len_by_rad, lv_length_max, lv_length_min):

    lv_length_arr = lv_radius_scale_arr * lv_radius_default * lv_len_by_rad 
    lv_length_scale_arr[lv_length_arr > lv_length_max] = lv_length_max / lv_length_default
    lv_radius_scale_arr[lv_length_arr > lv_length_max] = lv_length_max / lv_len_by_rad / lv_radius_default
    lv_length_scale_arr[lv_length_arr < lv_length_min] = lv_length_min / lv_length_default
    lv_radius_scale_arr[lv_length_arr < lv_length_min] = lv_length_min / lv_len_by_rad / lv_radius_default

    return lv_radius_scale_arr, lv_length_scale_arr

#================================================
# FUNCTION: limit heart within phantom dimension
#================================================
def mod_big_hrt(lv_radius_scale_arr, lv_length_scale_arr, 
                torso_long_axis_scale_arr, phantom_LATlen_default,
                max_hrt_to_LAT,
                lv_radius_default, lv_length_default, lv_len_by_rad):

    hrt_rad_by_LAT = (lv_radius_scale_arr * lv_radius_default) / (torso_long_axis_scale_arr * phantom_LATlen_default)
    mod_indices = hrt_rad_by_LAT > max_hrt_to_LAT

    #print(f"modifying indices: {np.where(mod_indices)} || total number: {np.shape(np.where(mod_indices))}")
    #print(f"LAT dim: {torso_long_axis_scale_arr[mod_indices]*phantom_LATlen_default}")
    # print(f"LV rad: {lv_radius_scale_arr[mod_indices]*lv_radius_default}")

  # new_rad_scale = LATlen * max_ratio / default_radius
    lv_radius_scale_arr[mod_indices] = torso_long_axis_scale_arr[mod_indices] * phantom_LATlen_default * max_hrt_to_LAT / lv_radius_default
  # new_len_scale = new_rad_scale * default_radius *len_by_rad / default_length
    lv_length_scale_arr[mod_indices] = lv_radius_scale_arr[mod_indices] * lv_radius_default * lv_len_by_rad / lv_length_default

    return lv_radius_scale_arr, lv_length_scale_arr



def parameter_setting_output(mode,num_image,gender,gender_number,core_xcat_folder,num_of_phantom_to_gen,phantom_folder,filename,extension,severity,location,activity_scale):
        
    #========================================
    # Phantom Size
    #========================================


    #RUN FIRST AND SEE IF THEY NEED TO BE EDITED
    phantom_APlen_default = 21.99078
    phantom_APlen_min = 19.60
    phantom_APlen_max = 28.80
    phantom_APlen_mean = 23.50
    phantom_APlen_std = 2.08

    phantom_LATlen_default = 31.42126
    phantom_LATlen_min = 26.70
    phantom_LATlen_max = 40.90
    phantom_LATlen_mean = 34.37
    phantom_LATlen_std = 3.25

    LAT_to_AP_ratio = 1.47

    torso_long_axis_scale_arr = trnrm(phantom_LATlen_mean, phantom_LATlen_std, phantom_LATlen_min, phantom_LATlen_max, num_image) / phantom_LATlen_default

    torso_short_axis_scale_arr = torso_long_axis_scale_arr * phantom_LATlen_default / LAT_to_AP_ratio / phantom_APlen_default


    #========================================
    # Left Ventricle
    #========================================
    lv_radius_default = 26.6032
    lv_radius_min = 16.0
    lv_radius_max = 35.0
    lv_radius_mean = 23.2 
    lv_radius_std = 3.3 
    lv_radius_scale_arr = trnrm(lv_radius_mean, lv_radius_std, lv_radius_min, lv_radius_max, num_image)
    lv_radius_scale_arr = lv_radius_scale_arr/lv_radius_default

    lv_length_default = 79.2621
    lv_length_min = 57.0
    lv_length_max = 105.0
    lv_length_mean = 73.9
    lv_length_std = 9.2

    lv_len_by_rad = 3.17
    lv_length_scale_arr = lv_radius_scale_arr * lv_radius_default * lv_len_by_rad / lv_length_default


    #===========================================================================
    # Processing LV params based on individual distribution, LAT AP dimensions
    #===========================================================================

    # Limit LV min max
    lv_radius_scale_arr, lv_length_scale_arr = limit_lv_dim(lv_radius_scale_arr, lv_length_scale_arr, 
                                                            lv_radius_default, lv_length_default, 
                                                            lv_len_by_rad, lv_length_max, lv_length_min)

    # Heart radius to lateral dimension
    max_hrt_to_LAT = 0.92
    lv_radius_scale_arr, lv_length_scale_arr = mod_big_hrt( lv_radius_scale_arr, lv_length_scale_arr, 
                                                            torso_long_axis_scale_arr, phantom_LATlen_default,
                                                            max_hrt_to_LAT,
                                                            lv_radius_default, lv_length_default, lv_len_by_rad)

    # Limit LV min max
    lv_radius_scale_arr, lv_length_scale_arr = limit_lv_dim(lv_radius_scale_arr, lv_length_scale_arr, 
                                                            lv_radius_default, lv_length_default, 
                                                            lv_len_by_rad, lv_length_max, lv_length_min)

    # compensate for torso effect
    lv_radius_scale_arr = lv_radius_scale_arr / torso_short_axis_scale_arr
    lv_length_scale_arr = lv_length_scale_arr / torso_short_axis_scale_arr


    #========================================
    # Phantom Height
    #========================================
    phantom_height_default = 163.04417
    phantom_height_min = 149.86
    phantom_height_max = 177.80
    phantom_height_mean = 163.45
    phantom_height_std = 7.34
    phantom_height_scale_arr = trnrm(phantom_height_mean, phantom_height_std, phantom_height_min, phantom_height_max, num_image) / phantom_height_default


    #=====================================
    # Heart Orientation Settings - DELTA NOT EXACT ANGLE
    #====================================

    d_xz_mean = 0
    d_xz_std = 10

    d_yx_mean = 0
    d_yx_std = 11

    d_xz_arr = trnrm(d_xz_mean, d_xz_std, d_xz_mean-2*d_xz_std, d_xz_mean+2*d_xz_std,num_image)
    d_yx_arr = trnrm(d_yx_mean, d_yx_std, d_yx_mean-2*d_yx_std, d_yx_mean+2*d_yx_std,num_image)

    #to prevent dextrocardia, pass translation array

    X_tr_arr = np.zeros(num_image)

    for i in range(num_image):
        if d_yx_arr[i] < 0:
            X_tr_arr[i] = d_yx_arr[i] * -1.7


    #=====================================
    # Breast Settings
    #====================================
    rbreast_short_axis_scale_min = 0.97
    rbreast_short_axis_scale_max = 1.03
    rbreast_short_axis_scale_arr = np.random.uniform(rbreast_short_axis_scale_min, rbreast_short_axis_scale_max, num_image)
    lbreast_short_axis_scale_arr = rbreast_short_axis_scale_arr

    rbreast_long_axis_scale_min = 0.97
    rbreast_long_axis_scale_max = 1.03
    rbreast_long_axis_scale_arr = np.random.uniform(rbreast_long_axis_scale_min, rbreast_long_axis_scale_max, num_image)
    lbreast_long_axis_scale_arr = rbreast_long_axis_scale_arr

    rbreast_height_scale_min = 0.97
    rbreast_height_scale_max = 1.03
    rbreast_height_scale_arr = np.random.uniform(rbreast_height_scale_min, rbreast_height_scale_max, num_image)
    lbreast_height_scale_arr = rbreast_height_scale_arr


    #=====================================
    # Skin thickness 
    #====================================
    skin_thick_min = 0.5
    skin_thick_max = 1.5
    skin_thick_scale_arr = np.random.uniform(skin_thick_min, skin_thick_max, num_image)
    #=====================================

    #=====================================
    # Slice settings
    #====================================
    slice_base = 729
    #slice_base = 300##################
    span_slice_up = 80
    span_slice_down = 175
    mod_slice_base = np.ceil(phantom_height_scale_arr * slice_base).astype('int')
    startslice_arr = mod_slice_base - span_slice_down
    endslice_arr = mod_slice_base + span_slice_up
    #startslice_arr = np.random.randint(act_startslice_arr, act_endslice_arr + 1, dtype=np.uint32)
    #endslice_arr = startslice_arr
    #=====================================
    # Activity ratio settings
    #=====================================

    #WE HAVE MADE AN ADJUSTMENT RELATIVE TO THE KIDNEYS AND GB - REMOVE THEM FOR ACCURACY.
    
    # Heart
    heart_base = 1419 / 1000
    myoVA_act_mean = activity_scale*1419 / heart_base #1000
    myoVA_act_std = activity_scale*810 / heart_base #571
    myoVA_act_min = activity_scale*490 / heart_base #345
    myoVA_act_max = activity_scale*4236 / heart_base #2985.20085

    myoVA_act_arr = trnrm(myoVA_act_mean, myoVA_act_std, myoVA_act_min, myoVA_act_max, num_image)

    # background
    bg_mean = 0.11
    bg_std = 0.05
    bg_min = 0.02
    bg_max = 0.29

    trnrm_bg = trnrm(bg_mean, bg_std, bg_min, bg_max, num_image) * myoVA_act_arr

    # liver, kidney, gall bladder
    max_act_mean = 0.44
    max_act_std = 0.19
    max_act_min = 0.16
    max_act_max = 1.30

    liver_act_arr = trnrm(max_act_mean, max_act_std, max_act_min, max_act_max, num_image) * myoVA_act_arr
    r_kidney_act_arr = trnrm(max_act_mean, max_act_std, max_act_min, max_act_max, num_image) * myoVA_act_arr
    l_kidney_act_arr = trnrm(max_act_mean, max_act_std, max_act_min, max_act_max, num_image) * myoVA_act_arr
    gallblad_act_arr = trnrm(max_act_mean, max_act_std, max_act_min, max_act_max, num_image) * myoVA_act_arr * 60 / 75

    # lung
    lng_act_mean = 0.14
    lng_act_std = 0.04
    lng_act_min = 0.05
    lng_act_max = 0.25

    lung_act_arr = trnrm(lng_act_mean, lng_act_std, lng_act_min, lng_act_max, num_image) * myoVA_act_arr

    #=====================================
    # Pixel size setting
    #=====================================
    pixel_width = 0.17 #0.01429*(0.17/0.3125) =0.0077736
    slice_width = 0.17 
    #slice_width = 0.5 #0.01429*(0.17/0.3125) =0.0077736
    array_size = 256
    #array_size = 512############################

    #=====================================
    # Defect settings
    #=====================================
    #defect_severity_scale = 1.0

    defect_severity_scale = 100/(100-severity)
    #=====================================
    # Parameters I might want to tune
    #=====================================
    color_code = 1
    lung_scale = 1.0
    breast_type = 1
    which_breast = 1
    # changing skin might be used to control fat

    #=====================================
    # Heart lesion setting
    #=====================================
    #severity
    #extension
    #location
    #extension,serverity,location
    
    if location == 'anterior':
        ThetaCenter = 0.0
    elif location == 'lateral':
        ThetaCenter = 90
    elif location == 'inferior':
        ThetaCenter = 180
        
    #ThetaCenter = 0.0		# theta center in deg. (between 0 and 360) \n")
    ThetaWidth = extension		# theta width in deg., total width (between 0 and 360 deg.)\n")
    XCenterIndex = 0.5		# x center (0.0=base, 1.0=apex, other fractions=distances in between)\n")
    XWidthIndex = 60		# x width, total in mms\n")
    Wall_fract = 1.0		# wall_fract, fraction of the outer wall transgressed by the lesion\n")
    motion_scale = 0.0		# scales the motion of the defect region (1 = normal motion, < 1 = reduced motion), altered motion blends with normal \n")
    border_zone_long = 10		# longitudinal width (in terms of number of control points) of transition between abnormal and normal motion\n")
    border_zone_radial = 5		# radial width (in terms of number of control points) of transition between abnormal and normal motion\n")

#9: Creates lesion (defect) for the LEFT VENTRICLE ONLY.
#
#--------------------------------
#  theta_center: location of lesion center in circumferential dimension
#
#  theta center =    0.0  => anterior wall
#  theta center =  +90.0  => lateral   "
#  theta center = +180.0  => inferior  "
#  theta center = +270.0  => septal    "
#--------------------------------
#  theta_width : lesion width in circumferential dimension
#
#  TOTAL width of defect in degrees. So for example a width of 90 deg.
#  means that the width is 45 deg. on either side of theta center.
#--------------------------------
#  x center :   lesion center in long-axis dimension
#
#  x center = 0    -> base of LV
#  x center = 1.0  -> apex of LV
#--------------------------------
#  x width:  lesion width in long-axis dimension
#
#  total width. Defect extend half the total width on either side of the
#  x_center.
#
# : if the specified width extends beyond the boundaries of the LV
#        then the defect is cut off and the effective width is less than the
#        specified width. So for example...
#
#--------------------------------
#  Wall_fract : fraction of the LV wall that the lesion transgresses
#  Wall_fract = 0.0 => transgresses none of the wall
#  Wall_fract = 0.5 => transgresses the inner half of the wall
#  Wall_fract = 1.0 => trangresses the entire wall
#--------------------------------
#
#

    #if not os.path.exists(param_folder):
            # If not, create the folder
            #os.makedirs(param_folder)
    #filename_base = 'feas_param'
    #param_filename=f'{param_folder}fs{version}_rand_params_{genders[0]}.npy'
    #np.save(param_filename, all_params)
    filename_base=filename
    for ind_nr in range(num_of_phantom_to_gen):
        filename=f'{filename_base}_nr{ind_nr}'
        output_phantom_no_color_code(mode,ThetaCenter, ThetaWidth, XCenterIndex, XWidthIndex, Wall_fract, motion_scale, border_zone_long, border_zone_radial,
                        core_xcat_folder,phantom_folder,gender,gender_number,color_code,lung_scale,lv_radius_scale_arr[ind_nr],lv_length_scale_arr[ind_nr],phantom_height_scale_arr[ind_nr],
                        torso_long_axis_scale_arr[ind_nr],torso_short_axis_scale_arr[ind_nr],breast_type,which_breast,rbreast_long_axis_scale_arr[ind_nr],rbreast_short_axis_scale_arr[ind_nr],
                        rbreast_height_scale_arr[ind_nr],lbreast_long_axis_scale_arr[ind_nr],lbreast_short_axis_scale_arr[ind_nr],lbreast_height_scale_arr[ind_nr],skin_thick_scale_arr[ind_nr],pixel_width,slice_width,array_size,
                        startslice_arr[ind_nr],endslice_arr[ind_nr],myoVA_act_arr[ind_nr],myoVA_act_arr[ind_nr],myoVA_act_arr[ind_nr],myoVA_act_arr[ind_nr],trnrm_bg[ind_nr],liver_act_arr[ind_nr],lung_act_arr[ind_nr],defect_severity_scale,filename)


#========================================
# CLA
#========================================



#========================================
# Directories and NR setting
#========================================
filename_base = 'feas_param'
param_folder = './dist_files_female/'
core_xcat_folder = '/home/y.zezhang/xcat/'
num_image_per_class = 10000
num_image = num_image_per_class
phantom_folder='/data01/user-storage/y.zezhang/xcat/patient'
mode = 0
gender = 'female'
gender_number=1

num_of_phantom_to_gen=48

if mode ==0:
    filename=f'{filename_base}_md{mode}_{gender}'
else:
    filename=f'defect/{filename_base}_md{mode}_{gender}'
            
activity_scale=0.015

extension=[30,60]
severity=[25,50]
location=['anterior','lateral','inferior']

extension_hl=0
severity_hl=0
location_hl='anterior'

parameter_setting_output(mode,num_image,gender,gender_number,core_xcat_folder,num_of_phantom_to_gen,phantom_folder,filename,extension_hl,severity_hl,location_hl,activity_scale)

for ext in extension:
    for sev in severity:
        for loc in location:
            mode=1
            filename=f'defect/{filename_base}_md{mode}_{gender}_e{ext}_s{sev}_{loc}'
            parameter_setting_output(mode,num_image,gender,gender_number,core_xcat_folder,num_of_phantom_to_gen,phantom_folder,filename,ext,sev,loc,activity_scale)
