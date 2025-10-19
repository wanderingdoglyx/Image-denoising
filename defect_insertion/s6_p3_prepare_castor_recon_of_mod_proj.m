clc; clear all; close all;

addpath('../SPIE_8_3/src/');
addpath('src/')
prev_folder = '../SPIE_10_31/';
%%
pat_list_fname = [prev_folder 'data/test_all_pat_info_hd_mirirv3_mc.mat'];
[act_pat_id_arr, pat_id_arr, study_date_arr] = get_pat_list(pat_list_fname);
month_flag = cellstr(readmatrix([prev_folder 'data/test_month_flag_hd_mirirv3_mc.txt'], ...
                      'OutputType', 'string'));
%%

pat_range = 1:length(act_pat_id_arr);
base_res_dir = 'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie_v2\test_mc_castor_mirirv3_apr3\';
base_res_dir_prev = 'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie\test_data_mirirv3\';

for ind_pat = pat_range
  
  fprintf('progress: %d/%d\n', ind_pat, length(pat_id_arr));
  study_date = study_date_arr{ind_pat};
  pat_id = pat_id_arr{ind_pat};
  fdir = ['D:\MIM\MIRIR_data_' month_flag{ind_pat} '_mim_7\' study_date '__Studies\'];

  res_dir = [base_res_dir_prev pat_id];
  if ~isfolder(res_dir); continue; end
  
  mod_res_dir = [base_res_dir pat_id, filesep, 'mod_proj', filesep];
  if ~isfolder(mod_res_dir); mkdir(mod_res_dir); end
  
%   delete([mod_res_dir, '*']);
%   continue;
  %% copy ct
  fname = 'ct.hct';
  src_file = [res_dir, filesep, fname];
  dest_file = [mod_res_dir, filesep, fname];
  copyfile(src_file, dest_file);
  
  fname = 'ct.ict';
  src_file = [res_dir, filesep, fname];
  dest_file = [mod_res_dir, filesep, fname];
  copyfile(src_file, dest_file);
  
  fname = 'CDRP.par';
  src_file = [res_dir, filesep, fname];
  dest_file = [mod_res_dir, filesep, fname];
  copyfile(src_file, dest_file);
  
  
end