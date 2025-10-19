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

import numpy as np
import sys

#========================================
# CLA
#========================================
param_folder = sys.argv[1]
ind_nr = int(sys.argv[2])
mode = int(sys.argv[3])
dist_folder_base = sys.argv[4]

#version = 12
version=13
genders = ['female']

#========================================
# Directories and NR setting
#========================================
filename_base = 'feas_param'
dist_folder = f'{dist_folder_base}/dist_files/'
#param_folder = f'param_files/feas_study_v{version}/'
core_xcat_folder = 'xcat_files/'
num_image_per_class = 10000
num_image = num_image_per_class
modes = [mode]

#=====================================
# Pixel size setting
#=====================================
pixel_width = 0.17
slice_width = 0.17
array_size = 256

#=====================================
# Defect settings
#=====================================
defect_severity_scale = 2.0

#=====================================
# Parameters I might want to tune
#=====================================
color_codes = [1, 0]
lung_scale = 1.0
breast_type = 0 #SUPINE NOT PRONE
which_breast = 1
# changing skin might be used to control fat

#==========================================
# save all random parameters setting
#==========================================
param_filename=f'{dist_folder}fs{version}_rand_params_{genders[0]}.npy'
all_params = np.load(param_filename, allow_pickle=True)

all_params = all_params.item()
skin_thick_scale_arr = all_params['skin_thick_scale_arr'] #change
lv_radius_scale_arr = all_params['lv_radius_scale_arr']
lv_length_scale_arr = all_params['lv_length_scale_arr']
phantom_height_scale_arr = all_params['phantom_height_scale_arr']
torso_long_axis_scale_arr = all_params['torso_long_axis_scale_arr']
torso_short_axis_scale_arr = all_params['torso_short_axis_scale_arr']

#NEWLY ADDED HEART ROTATION ARR
d_xz_arr = all_params['d_xz_arr']
d_yx_arr = all_params['d_yx_arr']
X_tr_arr = all_params['X_tr_arr']
#NEWLY ADDED BREAST VOL ARR
lbreast_vol_scale_arr = all_params['lbreast_vol_scale_arr']
rbreast_vol_scale_arr = all_params['rbreast_vol_scale_arr']
#lbreast_short_axis_scale_arr = all_params['lbreast_short_axis_scale_arr']
#lbreast_long_axis_scale_arr = all_params['lbreast_long_axis_scale_arr']
#lbreast_height_scale_arr = all_params['lbreast_height_scale_arr']
#rbreast_short_axis_scale_arr = all_params['rbreast_short_axis_scale_arr']
#rbreast_long_axis_scale_arr = all_params['rbreast_long_axis_scale_arr']
#rbreast_height_scale_arr = all_params['rbreast_height_scale_arr']
myoVA_act_arr = all_params['myoVA_act_arr']
trnrm_bg = all_params['trnrm_bg']
liver_act_arr = all_params['liver_act_arr']
#r_kidney_act_arr = all_params['r_kidney_act_arr']
#l_kidney_act_arr = all_params['l_kidney_act_arr']
#gallblad_act_arr = all_params['gallblad_act_arr']
lung_act_arr = all_params['lung_act_arr']
startslice_arr = all_params['startslice_arr']
endslice_arr = all_params['endslice_arr']
defect_params = all_params['defect']

ThetaCenter = defect_params['ThetaCenter']
ThetaWidth = defect_params['ThetaWidth']
XCenterIndex = defect_params['XCenterIndex']
XWidthIndex = defect_params['XWidthIndex']
Wall_fract = defect_params['Wall_fract']
motion_scale = defect_params['motion_scale']
border_zone_long = defect_params['border_zone_long']
border_zone_radial = defect_params['border_zone_radial']

#=====================================
# Write parameters files
#=====================================
for gender in genders:
  for mode in modes:
    color_code = color_codes[mode]
    filename = f'{param_folder}/{filename_base}_md{mode}_nr{ind_nr}_{gender}.par'
    with open(filename,'w') as fid:

      fid.write(f"mode = {mode}\n")
      fid.write(f"\n")
      fid.write(f"act_phan_each = 1\n")
      fid.write(f"atten_phan_each = 1\n")
      fid.write(f"\n")
      fid.write(f"out_period = 1\n")
      fid.write(f"time_per_frame = 0\n")
      fid.write(f"out_frames = 1\n")
      fid.write(f"\n")
      fid.write(f"heart_base = {core_xcat_folder}v{gender}50_heart.nrb\n")
      fid.write(f"heart_curve_file = {core_xcat_folder}heart_curve.txt\n")
      fid.write(f"\n")
      fid.write(f"uniform_heart = 0\n")
      fid.write(f"\n")
      fid.write(f"dia_filename = {core_xcat_folder}diaphragm_curve.dat\n")
      fid.write(f"ap_filename = {core_xcat_folder}ap_curve.dat\n")
      fid.write(f"\n")
      fid.write(f"arms_flag = 0\n")
      fid.write(f"gender = {0 if gender == 'male' else 1}\n")
      fid.write(f"organ_file = {core_xcat_folder}v{gender}50.nrb\n")
      fid.write(f"\n")
      fid.write(f"phan_rotx = 0.0\n")
      fid.write(f"phan_roty = 0.0\n")
      fid.write(f"phan_rotz = 0.0\n")
      fid.write(f"\n")
      fid.write(f"nurbs_save = 0\n")
      fid.write(f"ct_output = 0\n")
      fid.write(f"color_code = {color_code}\n")
      fid.write(f"iodine_flag = 0\n")
      fid.write(f"mesh_save = 0\n")
      fid.write(f"\n")
      fid.write(f"lung_scale = {lung_scale}\n")
      fid.write(f"lv_radius_scale = {lv_radius_scale_arr[ind_nr]}\n")
      fid.write(f"lv_length_scale = {lv_length_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"phantom_long_axis_scale = 1.0\n")
      fid.write(f"phantom_short_axis_scale = 1.0\n")
      fid.write(f"phantom_height_scale = {phantom_height_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"torso_long_axis_scale = {torso_long_axis_scale_arr[ind_nr]}\n")
      fid.write(f"torso_short_axis_scale = {torso_short_axis_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"chest_skin_long_axis_scale = 1.0\n")
      fid.write(f"chest_skin_short_axis_scale = 1.0\n")
      fid.write(f"\n")
      fid.write(f"abdomen_skin_long_axis_scale = 1.0\n")
      fid.write(f"abdomen_skin_short_axis_scale = 1.0\n")
      fid.write(f"\n")
      fid.write(f"pelvis_skin_long_axis_scale = 1.0\n")
      fid.write(f"pelvis_skin_short_axis_scale = 1.0\n")
      fid.write(f"\n")
      fid.write(f"bones_scale = 1.0\n")
      fid.write(f"\n")
      fid.write(f"head_torso_muscle_scale = 1.0 \n")
      fid.write(f"\n")
      fid.write(f"hrt_scale_x = 1.0\n")
      fid.write(f"hrt_scale_y = 1.0\n")
      fid.write(f"hrt_scale_z = 1.0\n")
      fid.write(f"\n")
      fid.write(f"breast_type = {breast_type}\n")
      fid.write(f"which_breast = {which_breast}\n")
      fid.write(f"breast_to_compress = 0\n")
      fid.write(f"compression_type = 0\n")
      fid.write(f"compression_factor = 0.5\n")
      fid.write(f"\n")
      fid.write(f"# breast settings\n")
      #fid.write(f"rbreast_long_axis_scale = {rbreast_long_axis_scale_arr[ind_nr]}\n")
      #fid.write(f"rbreast_short_axis_scale = {rbreast_short_axis_scale_arr[ind_nr]}\n")
      #fid.write(f"rbreast_height_scale = {rbreast_height_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"vol_rbreast = {rbreast_vol_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"rbr_theta = 10.0\n")
      fid.write(f"rbr_phi = 0.0\n")
      fid.write(f"r_br_tx = 0.0\n")
      fid.write(f"r_br_ty = 0.0\n")
      fid.write(f"r_br_tz = 0.0\n")
      fid.write(f"\n")
      #fid.write(f"lbreast_long_axis_scale = {lbreast_long_axis_scale_arr[ind_nr]}\n")
      #fid.write(f"lbreast_short_axis_scale = {lbreast_short_axis_scale_arr[ind_nr]}\n")
      #fid.write(f"lbreast_height_scale = {lbreast_height_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"vol_lbreast = {lbreast_vol_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"lbr_theta = 10.0\n")
      fid.write(f"lbr_phi = 0.0\n")
      fid.write(f"l_br_tx = 0.0\n")
      fid.write(f"l_br_ty = 0.0\n")
      fid.write(f"l_br_tz = 0.0\n")
      fid.write(f"\n")
      fid.write(f"rdiaph_liv_scale = 1.0\n")
      fid.write(f"ldiaph_scale = 1.0\n")
      fid.write(f"\n")
      fid.write(f"marrow_flag = 1\n")
      fid.write(f"\n")
      fid.write(f"thickness_skin = {skin_thick_scale_arr[ind_nr]}\n")
      fid.write(f"\n")
      #fid.write(f"thickness_ribs = 1.0\n")
      #fid.write(f"thickness_backbone = 1.0\n")
      #fid.write(f"thickness_esoph = 1.0\n")
      #fid.write(f"thickness_trachea = 0.0\n")
      fid.write(f"\n")
      fid.write(f"use_res = 0\n")
      fid.write(f"\n")
      fid.write(f"\n")
      fid.write(f"#VOLUMES\n")
      fid.write(f"\n")
      fid.write(f"vol_liver = 0.0\n")
      fid.write(f"vol_stomach = 0.0\n")
      fid.write(f"vol_trachea = 0.0\n")
      fid.write(f"vol_esoph = 0.0\n")
      fid.write(f"\n")
      fid.write(f"# Pixel\n")
      fid.write(f"\n")
      fid.write(f"pixel_width = {pixel_width}\n")
      fid.write(f"slice_width = {slice_width}\n")
      fid.write(f"array_size = {array_size}\n")
      fid.write(f"subvoxel_index = 1\n")
      fid.write(f"startslice = {startslice_arr[ind_nr]}\n")
      fid.write(f"endslice = {endslice_arr[ind_nr]}\n")
      fid.write(f"\n")

      #INCLUDE ROTATION STUFF HERE
      #fid.write(f"d_ZY_rotation = {d_zy_arr[ind_nr]}\n")
      fid.write(f"d_XZ_rotation = {d_xz_arr[ind_nr]}\n")
      fid.write(f"d_YX_rotation = {d_yx_arr[ind_nr]}\n")
      #fid.write(f"zy_rot = {zy_arr[ind_nr]}\n")
      #fid.write(f"xz_rot = {xz_arr[ind_nr]}\n")
      #fid.write(f"yx_rot = {yx_arr[ind_nr]}\n")

      fid.write(f"X_tr = {X_tr_arr[ind_nr]}\n")
      fid.write(f"Y_tr = 0.0\n")
      fid.write(f"Z_tr = 0.0\n")
      fid.write(f"\n")
      fid.write(f"\n")
      fid.write(f"# Activity\n")
      fid.write(f"\n")
      fid.write(f"activity_unit = 0\n")
      fid.write(f"\n")
      fid.write(f"myoLV_act = {myoVA_act_arr[ind_nr]}\n")
      fid.write(f"myoRV_act = {myoVA_act_arr[ind_nr]}\n")
      fid.write(f"myoLA_act = {myoVA_act_arr[ind_nr]}\n")
      fid.write(f"myoRA_act = {myoVA_act_arr[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"bldplLV_act = {trnrm_bg[ind_nr]}\n")
      fid.write(f"bldplRV_act = {trnrm_bg[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"bldplLA_act = {trnrm_bg[ind_nr]}\n")
      fid.write(f"bldplRA_act = {trnrm_bg[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"coronary_art_activity =  {trnrm_bg[ind_nr]}\n")
      fid.write(f"coronary_vein_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"valve_thickness = 0.1\n")
      fid.write(f"\n")
      fid.write(f"\n")
      fid.write(f"body_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"skin_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"rbreast_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"lbreast_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"muscle_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"liver_activity = {liver_act_arr[ind_nr]}\n")
      fid.write(f"gall_bladder_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"r_lung_activity = {lung_act_arr[ind_nr]}\n")
      fid.write(f"l_lung_activity = {lung_act_arr[ind_nr]}\n")
      fid.write(f"esophagus_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"esophagus_cont_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"laryngopharynx_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"larynx_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"st_wall_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"st_cnts_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"pancreas_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"r_kidney_cortex_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"r_kidney_medulla_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"l_kidney_cortex_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"l_kidney_medulla_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"adrenal_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"r_renal_pelvis_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"l_renal_pelvis_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"spleen_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"rib_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"cortical_bone_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"spine_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"spinal_cord_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"bone_marrow_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"art_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"vein_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"bladder_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"prostate_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"asc_li_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"trans_li_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"desc_li_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"sm_intest_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"rectum_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"sem_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"vas_def_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"test_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"penis_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"epididymus_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"ejac_duct_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"pericardium_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"cartilage_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"intest_air_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"ureter_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"urethra_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"lymph_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"lymph_abnormal_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"trach_bronch_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"airway_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"uterus_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"vagina_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"right_ovary_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"left_ovary_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"fallopian_tubes_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"parathyroid_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"thyroid_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"thymus_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"salivary_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"pituitary_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"eye_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"lens_activity = {trnrm_bg[ind_nr]}\n")
      fid.write(f"\n")
      fid.write(f"lesn_activity = {myoVA_act_arr[ind_nr]/defect_severity_scale}\n")
      fid.write(f"\n")
      fid.write(f"energy = 140\n")
      fid.write(f"atten_table_filename = {core_xcat_folder}atten_table.dat\n")
      fid.write(f"\n")
      fid.write(f"motion_defect_flag = 0\n")
      fid.write(f"#---------------------Heart lesion parameters------------------------------SEE NOTE 9\n")
      fid.write(f"ThetaCenter = {ThetaCenter}		# theta center in deg. (between 0 and 360) \n")
      fid.write(f"ThetaWidth = {ThetaWidth}		# theta width in deg., total width (between 0 and 360 deg.)\n")
      fid.write(f"XCenterIndex = {XCenterIndex}		# x center (0.0=base, 1.0=apex, other fractions=distances in between)\n")
      fid.write(f"XWidthIndex = {XWidthIndex}		# x width, total in mms\n")
      fid.write(f"Wall_fract = {Wall_fract}		# wall_fract, fraction of the outer wall transgressed by the lesion\n")
      fid.write(f"motion_scale = {motion_scale}		# scales the motion of the defect region (1 = normal motion, < 1 = reduced motion), altered motion blends with normal \n")
      fid.write(f"\n")
      fid.write(f"border_zone_long = {border_zone_long}		# longitudinal width (in terms of number of control points) of transition between abnormal and normal motion\n")
      fid.write(f"border_zone_radial = {border_zone_radial}		# radial width (in terms of number of control points) of transition between abnormal and normal motion\n")
      fid.write(f"#--------------------------------------------------------------------------\n")
      fid.write(f"\n")
      fid.write(f"#---------------------Spherical lesion parameters--------------------------SEE NOTE 10\n")
      fid.write(f"x_location = 102		# x coordinate (pixels) to place lesion\n")
      fid.write(f"y_location = 124		# y coordinate (pixels) to place lesion \n")
      fid.write(f"z_location = 26			# z coordinate (pixels) to place lesion \n")
      fid.write(f"lesn_diameter = 10.0		# Diameter of lesion (mm)\n")
      fid.write(f"tumor_motion_flag = 0		# Sets tumor motion (0 = default motion based on lungs, 1 = motion defined by user curve below)\n")
      fid.write(f"tumor_motion_filename = {core_xcat_folder}tumor_curve.dat		# Name of user defined motion curve for tumor\n")
      fid.write(f"#--------------------------------------------------------------------------\n")
      fid.write(f"\n")
      fid.write(f"#---------------------Heart plaque parameters------------------------------SEE NOTE 11\n")
      fid.write(f"p_center_v = 0.2		# plaque center along the length of the artery (between 0 and 1)\n")
      fid.write(f"p_center_u = 0.5		# plaque center along the circumference of the artery (between 0 and 1)\n")
      fid.write(f"p_height = 1.0			# plaque thickness in mm.\n")
      fid.write(f"p_width = 2.0			# plaque width in mm.\n")
      fid.write(f"p_length = 5.0			# plaque length in mm.\n")
      fid.write(f"p_id = aorta			# vessel ID to place the plaque in \n")
      fid.write(f"#--------------------------------------------------------------------------\n")
      fid.write(f"\n")
      fid.write(f"#---------------------Vector parameters------------------------------------SEE NOTE 12\n")
      fid.write(f"vec_factor = 2		# higher number will increase the precision of the vector output\n")
      fid.write(f"#--------------------------------------------------------------------------\n")

