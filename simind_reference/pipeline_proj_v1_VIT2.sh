#!/bin/bash

#===================================================================================================
# custom function
#===================================================================================================
my_mkdir () {
  if [ ! -d ${1} ]
  then
    mkdir -p ${1}
  fi
}

#===================================================================================================
# set path
#===================================================================================================
PATH=/home/nuri.choi/simind_base/:$PATH
export PATH

SMC_DIR=/home/nuri.choi/simind_base/smc_dir/
export SMC_DIR

#===================================================================================================
# param default
#===================================================================================================
fs_version=13
run_version=3

scat_order=5
num_proj=60
scoring_routine=1
#===================================================================================================
# param selction
#===================================================================================================

job_ind=${1}
ind_nr=$(( job_ind-1 ))
#ind_nr=$(( (job_ind-1) / 2 ))
#mf_ind=$(( job_ind % 2 ))

mf_ind=1

mf_arr=(
  male
  female
)
mf=${mf_arr[${mf_ind}]}

#ENSURE THAT GEN_DIST HAS BEEN RUN FIRST!


#===================================================================================================
# folders and files
#===================================================================================================
base_folder=/data/nuri.choi/VIT_v2


param_folder=${base_folder}/param_out_v${run_version}/${mf}
phan_out_folder=${base_folder}/phan_out_v${run_version}/${mf}/nr${ind_nr}
sin_out_folder=${base_folder}/sin_out_v${run_version}/${mf}/nr${ind_nr}
my_mkdir ${param_folder}
my_mkdir ${phan_out_folder}
my_mkdir ${sin_out_folder}

#changed cur_pwd to be the main folder .../gen_proj
cur_pwd=${PWD%/*}
xcat_exe=dxcat2_linux_64bit
xcat_folder=${cur_pwd}/gen_synth_phantom_v${run_version}

echo "======================================================================================="
echo "NR: ${ind_nr} || MF: ${mf}"
echo "Working Dir: ${phan_out_folder}"
echo "======================================================================================="
#===================================================================================================
# Part-1: 
#   - generate the xcat phantom healthy
#   - save the organ specific projection
#   - delete the activity phantom, keep attenuation phantom for defect
#   - remove unncecessary simind generated file
#===================================================================================================



echo "---------------------------"
echo "Healthy"
echo "---------------------------"
cd ${xcat_folder}
#--------------------------------------------------------------------------------------------
# step-1: generate the parameter file for healthy
#--------------------------------------------------------------------------------------------
python3 ${xcat_folder}/python_scripts/gen_param_files_${mf}.py ${param_folder} ${ind_nr} 0 ${xcat_folder}
param_fname=${param_folder}/feas_param_md0_nr${ind_nr}_${mf}.par

#--------------------------------------------------------------------------------------------
# step-2: generate the xcat attenuation and activity
#--------------------------------------------------------------------------------------------
echo "generating xcat phantom ..."
echo 
./${xcat_exe} ${param_fname} ${phan_out_folder}/nr${ind_nr}_hl 1> temp_out/temp_log_nr${ind_nr}_${mf}.out 2> temp_out/temp_log_nr${ind_nr}_${mf}.err

rm temp_out/temp_log_nr${ind_nr}_${mf}.{out,err}
#rm ${phan_out_folder}/nr${ind_nr}_hl_log

# process attenuation map
#python3 ${xcat_folder}/python_scripts/process_attn_map.py ${phan_out_folder} nr${ind_nr}_hl_atn_1.bin
#rm ${phan_out_folder}/nr${ind_nr}_hl_atn_1.bin
#mv ${phan_out_folder}/pp_nr${ind_nr}_hl_atn_1.bin ${phan_out_folder}/nr${ind_nr}_hl_atn_av.bin

mv ${phan_out_folder}/nr${ind_nr}_hl_atn_1.bin ${phan_out_folder}/nr${ind_nr}_hl_atn_av.bin

#--------------------------------------------------------------------------------------------
# step-3: save organ color file in int 16
#--------------------------------------------------------------------------------------------
python3 ${xcat_folder}/python_scripts/opt_organ_file_v2.py ${phan_out_folder} nr${ind_nr}_hl_act_1.bin
rm ${phan_out_folder}/nr${ind_nr}_hl_act_1.bin


#--------------------------------------------------------------------------------------------
# step-4: 
#   for each organ
#     extract organ mask
#     generate simind projection
#     remove unnecessary projections
#--------------------------------------------------------------------------------------------

# copy simind_smc file to the folder
cd ${cur_pwd}
cp simind_smc_tv.smc ${phan_out_folder}/
cp scattwin.win ${phan_out_folder}/

# change to phan folder
cd ${phan_out_folder}

#organs=(myo liver lung gallb kidney bg)
organs=(myo liver lung bg)

#scale_factor_arr=(100 10 10 100 10 4)
scale_factor_arr=(100 10 10 4)
#scale_factor_arr=(1 1 1 1 1 1)

#for organ_id in {1..6}
for organ_id in {1..4}
do
  organ_id_m1=$(( organ_id-1 ))
  scale_factor=${scale_factor_arr[${organ_id_m1}]}
  cur_organ=${organs[$organ_id_m1]}

  echo "---------------------------------------------------------------------------------"
  echo "generating simind projection of: ${cur_organ}"
  # generate organ mask

  python3 ${xcat_folder}/python_scripts/gen_organ_mask.py ${phan_out_folder} opt_nr${ind_nr}_hl_act_1.bin ${organ_id} ${ind_nr}

  # run simind projection
  start_time=`date +%s`
  echo "simind simind_smc_tv.smc o${cur_organ}_nr${ind_nr}/NN:${scale_factor}/SC:${scat_order}/FD:nr${ind_nr}_hl/FS:${cur_organ}_nr${ind_nr}/29:${num_proj}/84:${scoring_routine}/FA:1"
  simind simind_smc_tv.smc o${cur_organ}_nr${ind_nr}/NN:${scale_factor}/SC:${scat_order}/FD:nr${ind_nr}_hl/FS:${cur_organ}_nr${ind_nr}/29:${num_proj}/84:${scoring_routine}/FA:1
  end_time=`date +%s`
  echo "Elapsed time: $(( $end_time - $start_time )) sec"
  echo

  # move projection data to sin_out_folder
  mv o${cur_organ}_nr${ind_nr}_tot_w1.a00 ${sin_out_folder}
  mv o${cur_organ}_nr${ind_nr}_tot_w1.h00 ${sin_out_folder}

  # remove
  # KEEP ICT, HCT FILE AND ORGAN MASK IF MYO

  if [ $organ_id -ne 1 ]
  then
    rm o${cur_organ}_nr${ind_nr}.ict
    rm o${cur_organ}_nr${ind_nr}.hct
    rm ${cur_organ}_nr${ind_nr}_act_av.bin

  fi

  rm o${cur_organ}_nr${ind_nr}.res
  rm o${cur_organ}_nr${ind_nr}.csv
  rm o${cur_organ}_nr${ind_nr}.bis
  rm o${cur_organ}_nr${ind_nr}_tot_w2*
  rm o${cur_organ}_nr${ind_nr}_tew_w3*
  rm o${cur_organ}_nr${ind_nr}_tot_w4*  

done




#===================================================================================================
# Part-2: 
# for each extent and location
#   - generate the defect mask using xcat
#   - save the defect-specific projection
#   - remove unncecessary simind generated file
#===================================================================================================
ext_arr=(30 45 60)
#ext_arr=(30 45 60)
#loc_ang_arr=(0 180 90)  # anterior, inferior, lateral
#loc_arr=(a i l)
loc_ang_arr=(0 180 90)  # anterior, inferior, lateral
loc_arr=(a i l)


num_ext=${#ext_arr[@]}
num_loc=${#loc_arr[@]} #length of array notation

scale_factor_def=100
#scale_factor_def=10
for ind_ext in $(seq 0 1 $(( num_ext-1 )))
do
for ind_loc in $(seq 0 1 $(( num_loc-1 )))
do
  cur_ext=${ext_arr[${ind_ext}]}
  cur_loc_ang=${loc_ang_arr[${ind_loc}]}
  cur_loc=${loc_arr[${ind_loc}]}
  def_name=d${cur_loc}${cur_ext}

  echo "---------------------------"
  echo "Def: ${def_name}"
  echo "---------------------------"
  cd ${xcat_folder} 
  #--------------------------------------------------------------------------------------------
  # step-1: generate the parameter file for healthy
  #--------------------------------------------------------------------------------------------
  python3 ${xcat_folder}/python_scripts/gen_param_files_${mf}.py ${param_folder} ${ind_nr} 1 ${xcat_folder}
  param_fname=${param_folder}/feas_param_md1_nr${ind_nr}_${mf}.par

  #--------------------------------------------------------------------------------------------
  # step-2: generate the xcat attenuation and activity
  #--------------------------------------------------------------------------------------------
  echo "generating xcat phantom ..."
  echo 
  echo "./${xcat_exe} ${param_fname} --ThetaCenter ${cur_loc_ang} --ThetaWidth ${cur_ext} ${phan_out_folder}/nr${ind_nr}_${def_name} 1> temp_out/temp_log_nr${ind_nr}_${mf}.out 2> temp_out/temp_log_nr${ind_nr}_${mf}.err"
  ./${xcat_exe} ${param_fname} --ThetaCenter ${cur_loc_ang} --ThetaWidth ${cur_ext} ${phan_out_folder}/nr${ind_nr}_${def_name} 1> temp_out/temp_log_nr${ind_nr}_${mf}.out 2> temp_out/temp_log_nr${ind_nr}_${mf}.err

  rm temp_out/temp_log_nr${ind_nr}_${mf}.{out,err}
  #rm ${phan_out_folder}/nr${ind_nr}_${def_name}_log
  #rm ${phan_out_folder}/nr${ind_nr}_${def_name}_atn_1.bin

  #--------------------------------------------------------------------------------------------
  # step-3: change defect activity to a mask
  #--------------------------------------------------------------------------------------------
  python3 ${xcat_folder}/python_scripts/make_defect_mask_v2.py ${phan_out_folder} nr${ind_nr}_${def_name}_act_1.bin ${def_name}

  #rm ${phan_out_folder}/nr${ind_nr}_${def_name}_act_1.bin
  mv ${phan_out_folder}/mask_nr${ind_nr}_${def_name}_act_1.bin ${phan_out_folder}/nr${ind_nr}_${def_name}_act_av.bin

  #--------------------------------------------------------------------------------------------
  # step-4: run simind projection
  #--------------------------------------------------------------------------------------------
  cd ${phan_out_folder}
  echo "generating simind projection of: ${def_name}"
  start_time=`date +%s`
  echo "simind simind_smc_tv.smc o${def_name}_nr${ind_nr}/NN:${scale_factor_def}/SC:${scat_order}/FD:nr${ind_nr}_hl/FS:nr${ind_nr}_${def_name}/29:${num_proj}/84:${scoring_routine}/FA:1"
  simind simind_smc_tv.smc o${def_name}_nr${ind_nr}/NN:${scale_factor_def}/SC:${scat_order}/FD:nr${ind_nr}_hl/FS:nr${ind_nr}_${def_name}/29:${num_proj}/84:${scoring_routine}/FA:1
  end_time=`date +%s`
  echo "Elapsed time: $(( $end_time - $start_time )) sec"
  echo

  # move projection data to sin_out_folder
  mv o${def_name}_nr${ind_nr}_tot_w1.a00 ${sin_out_folder}
  mv o${def_name}_nr${ind_nr}_tot_w1.h00 ${sin_out_folder}

  # remove 

  # CHANGE BACK ONLY COMMENTED TO SEE THE DEFECT MASK
  rm o${def_name}_nr${ind_nr}.ict
  rm o${def_name}_nr${ind_nr}.hct
  rm o${def_name}_nr${ind_nr}.res
  rm o${def_name}_nr${ind_nr}.csv
  rm o${def_name}_nr${ind_nr}.bis
  rm o${def_name}_nr${ind_nr}_tot_w2*
  rm o${def_name}_nr${ind_nr}_tew_w3*
  rm o${def_name}_nr${ind_nr}_tot_w4*  
  rm nr${ind_nr}_${def_name}_act_1.bin
  rm nr${ind_nr}_${def_name}_atn_1.bin

  

done
done

# remove everything
rm ${phan_out_folder}/nr${ind_nr}_hl_atn_av.bin
rm ${phan_out_folder}/opt_nr${ind_nr}_hl_act_1.bin
#FOR PURPOSE OF ROTATING MYO MAP, CHANGE NAME TO PREROTATE. WILL BE ROTATED TO ATTEN.ICT
mv ${phan_out_folder}/omyo_nr${ind_nr}.ict ${phan_out_folder}/prerotate.ict
