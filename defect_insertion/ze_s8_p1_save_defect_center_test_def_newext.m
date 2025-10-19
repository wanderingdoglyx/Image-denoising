clc; clear all; close all;


addpath('src/')
%%
%pat_id_arr = cellstr(readmatrix('data/test_pat_list_hd_mirirv3_mc_sa.txt', ...
 %                     'OutputType', 'string'));

% Set the root folder path
rootFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/pre_projection';  

% Get all items in the folder
items = dir(rootFolder);

% Filter only directories and exclude '.' and '..'
isSubfolder = [items.isdir] & ~ismember({items.name}, {'.', '..'});

% Get only the names of the first-level subfolders
pat_id_arr = {items(isSubfolder).name};

pat_range = 1:length(pat_id_arr);

%base_res_dir  = ['Z:\Active\rahman.m\projects\dl_denoising\debug\' ...
%                'db_defect_insertion\data_spie\test_data_mirirv3_sa'];
%base_res_dir_new  = ['Z:\Active\rahman.m\projects\dl_denoising\debug\' ...
%                'db_defect_insertion\data_spie\test_data_mirirv3_sa_wd'];

base_res_dir_new  = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/def_centroid'];

%%
N = 128;
num_pat = length(pat_range);
res_factor_seg = 4;
res_factor_reorient = 2;
%%
sev_arr =[375];
%sev_arr = [100,150, 175, 250, 330,375, 400, 500,750, 1000]; %total

ext_arr =  [15, 30, 45, 60, 90,120]; %total
loc_arr = {'a'; 'i'; 'l'};
loc_arr_full = {'Ant'; 'Inf'; 'Lat'};

%ext_arr =  [30, 60]; %total
%loc_arr = {'a'; 'i'; };
%loc_arr_full = {'Ant'; 'Inf'; };

Nx = 48; 
Ny = 48;
Nz = 32;
%Nz = 48;

[X, Y] = meshgrid(1:128);

for ind_pat = 1:num_pat
  pat_id = pat_id_arr{ind_pat};
  tStart = tic;
  %% calculate centroid
  fold = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/def_segments/' pat_id];
  fname = [fold, '/_SA_seg_.mat'];
  load(fname);
  c_seg = regionprops(lv_mask, 'centroid');
  c_seg = round(c_seg.Centroid);
  c_seg(3) = c_seg(3) * res_factor_reorient;
  c_seg(2) = c_seg(2) * res_factor_reorient / res_factor_seg;
  c_seg(1) = c_seg(1) * res_factor_reorient / res_factor_seg;
  c_seg = round(c_seg);

  for ind_loc = 1:length(loc_arr)
      def_loc = loc_arr_full{ind_loc};
      for def_ext = ext_arr
        def_name = [def_loc 'Z21D' num2str(def_ext) '_'];
        def_name_half = ['d' loc_arr{ind_loc} '21' num2str(def_ext)];
        
        %% calculate defect centroid
        fold = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/def_segments/' pat_id];
        fname = [fold, '/_SA_def_' def_name '.mat'];
        load(fname);
        c_def_ar = regionprops(def_mask>0, 'Area');
        idx = find([c_def_ar.Area] ==  max([c_def_ar.Area]));
        c_def = regionprops(def_mask>0, 'centroid');
      %   c_def = c_def.Centroid;
        c_def = round(c_def(idx).Centroid);
        c_def(3) = c_def(3) * res_factor_reorient;
        c_def(2) = c_def(2) * res_factor_reorient / res_factor_seg;
        c_def(1) = c_def(1) * res_factor_reorient / res_factor_seg;
        c_def = round(c_def);
        
        c_def_mod = c_def - (c_seg - [Nx/2, Ny/2, Nz/2]-1); %origin
        %c_def_mod = c_def - (c_seg - [Nx/2, Ny/2, Nz/2]);
        
        cur_fold = fullfile(base_res_dir_new, pat_id);
        if ~isfolder(cur_fold); mkdir(cur_fold); end
        fname = fullfile(cur_fold, ['def_centroid_' def_name_half '_mod.bin']);
        my_fwrite(fname, c_def_mod, 'float32');
        if c_def_mod(3) ~= 17 && c_def_mod(3) ~= 19
          fprintf('Def: %s || Center Slice: %d \n', def_name, c_def_mod(3));
        end
      end
  end
  fprintf('Progress: %d/%d || ET: %.4f\n', ind_pat, num_pat, toc(tStart));
  fprintf('================================================\n');
  
end
              
