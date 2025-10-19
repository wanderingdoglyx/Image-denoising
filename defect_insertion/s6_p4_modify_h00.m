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
def_loc_full_arr = {'Ant'; 'Inf'; 'Lat'; 'Sep'; 'TAnt'; 'TInf'; 'AntLat'; 'InfLat';};
def_loc_obj_arr = {'A'; 'I'; 'L'; 'S'; 'TA'; 'TI'; 'AL'; 'IL'}; %Asheq: 9/5/22
def_loc_arr = lower(def_loc_obj_arr);
def_extent_d_arr = [15, 30, 45, 60, 90];
sev_arr = [0.1, 0.175, 0.25, 0.5 1];
def_extent_z = 21;

pat_range = 1:length(act_pat_id_arr);
base_res_dir = 'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie_v2\';
prob_reject_arr = 1:8;

for ind_pat = 1%pat_range
  
  tStart = tic;
  study_date = study_date_arr{ind_pat};
  pat_id = pat_id_arr{ind_pat};
  fdir = ['D:\MIM\MIRIR_data_' month_flag{ind_pat} '_mim_7\' study_date '__Studies\'];

  res_dir = [base_res_dir, 'test_mc_castor_mirirv3_apr3', filesep, pat_id];
  if ~isfolder(res_dir); continue; end
  
  mod_res_dir = [res_dir, filesep, 'mod_proj'];
  
  %% Read base file
  base_file = [res_dir '/out_hl_obj_tot_w1.h00'];
  fid = fopen(base_file, 'r');
  i = 1;
  tline = fgetl(fid);
  A_base{i} = tline;
  while ischar(tline)
    i = i+1;
    tline = fgetl(fid);
    A_base{i} = tline;
  end
  fclose(fid);
  
  %% read original projection
  S = get_dir(fdir, '_PriPrj_', pat_id);
  S_dcm = dir(fullfile([fdir, S], '*.dcm'));
  S_dcm = S_dcm(1).name;
  fname = [fdir, S, filesep, S_dcm];

  di = dicominfo(fname);
  
  num_of_projection = di.RotationInformationSequence.Item_1.NumberOfFramesInRotation;
  start_angle = di.RotationInformationSequence.Item_1.StartAngle;
  
 %% def
  for ind_def_loc = 1:length(def_loc_obj_arr)
    def_loc_obj = def_loc_obj_arr{ind_def_loc};
    def_loc = def_loc_arr{ind_def_loc};
    for def_extent_d = def_extent_d_arr
      for sev = sev_arr
        def_name_obj = ...
          ['d' def_loc_obj num2str(def_extent_z) num2str(def_extent_d) ...
            's' num2str(sev*1000) '_obj']; 
        def_name = lower(def_name_obj);
        for ind_prob = 1:length(prob_reject_arr)
          dose_name = ['d' num2str(ind_prob)];
          %% modify h00
          A = A_base;
          A{13} = sprintf('!name of data file := mod_proj_%s_%s_%s.a00', def_name, pat_id, dose_name);
          A{14} = sprintf('patient name := SMC_mod_proj_%s_%s_%s.a00', def_name, pat_id, dose_name);
          A{32} = sprintf('!total number of images := %d', num_of_projection);
          A{46} = sprintf('scaling factor (mm/pixel) [3] := 6.800');
          A{49} = sprintf('!number of projections := %d', num_of_projection);
          A{50} = sprintf('!number of images/energy window := %d', num_of_projection);
          A{62} = sprintf('start angle := %.3f', start_angle);  
          if (num_of_projection ~= 30)
%             fprintf('Pat: %s || Proj: %d', pat_id, num_of_projection);
          end
          %% save
          fname = ['mod_proj_' def_name '_' num2str(pat_id) '_' dose_name '.h00'];
          dest_file = fullfile(mod_res_dir, fname);
          fid = fopen(dest_file, 'w');
          for i = 1:numel(A)
             if A{i+1} == -1
                 fprintf(fid,'%s', A{i});
                 break
             else
                 fprintf(fid,'%s\n', A{i});
             end
          end
          fclose(fid);
        end
      end
    end
  end
  fprintf('progress: %d/%d || ET: %.4f\n', ind_pat, length(pat_id_arr), toc(tStart));
end