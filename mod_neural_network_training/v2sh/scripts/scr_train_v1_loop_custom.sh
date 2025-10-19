#!/bin/bash

version=2sh #old
#version=29

job_ind=${1}
lambda_val_ind_mdiff=${2}

num_lambda=10
lambda_val_ind_chdiff=$(( (job_ind - 1) % num_lambda ))
dose_level_ind=$(( (job_ind - 1) / num_lambda -1))
dose_level_arr=(
  33
  
  
  
)

dose_level=${dose_level_arr[${dose_level_ind}]}

#echo ${dose_level}

epochs=200

batch_size_arr=(32)
#source activate tf-gpu2

base_folder=/datastore01/user-storage/y.zezhang/2025_high_dose_project/mod_neural_network_training ################################################
#learning_folder='den_3d_v'+str(version)
#full_learning_folder=base_folder+'/learning/'

#base_folder=/data/rahman.m/projects/dl_denoising/debug/db_defect_insertion/data_spie/
learning_folder=highdose_3d_v${version} #########################################################
full_learning_folder=${base_folder}/learning/${learning_folder}

for subfolder in weights losses pred
do
  if [[ ! -d $full_learning_folder/${subfolder} ]]
  then
    mkdir -p $full_learning_folder/${subfolder}
    echo "Making dir: $full_learning_folder/${subfolder}"
  fi
done

lambda_val_ind_mdiff_arr=(0 1 2 3 4 5 6 7 8 9)
#for lambda_val_ind_mdiff in ${lambda_val_ind_mdiff_arr[@]}
#do
  for batch_size in ${batch_size_arr[@]}
  do
    arglist=(
      --weights_name wt_v${version}
      --loss_fn_name ls_v${version}
      --base_folder ${base_folder}
      --dose_level ${dose_level}
      --num_iter 8
      --batch_size ${batch_size}
      --epochs ${epochs}
      --learning_folder ${learning_folder}
      --lambda_val_ind_chdiff ${lambda_val_ind_chdiff}
      --lambda_val_ind_mdiff ${lambda_val_ind_mdiff}
    )

    echo "python3 train_3Dden_AR_v${version}_custom_loop.py ${arglist[@]}"
    python3 train_3Dden_AR_v${version}_custom_loop.py ${arglist[@]}

  done
#done
