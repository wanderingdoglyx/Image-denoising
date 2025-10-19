clc; clear all; close all;


addpath('src/')
%%

% Set the root folder path
rootFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/pre_projection';  

% Get all items in the folder
items = dir(rootFolder);

% Filter only directories and exclude '.' and '..'
isSubfolder = [items.isdir] & ~ismember({items.name}, {'.', '..'});

% Get only the names of the first-level subfolders
pat_id_arr = {items(isSubfolder).name};

pat_range = 1:length(pat_id_arr);


%pat_id_arr = cellstr(readmatrix('data/test_pat_list_hd_mirirv3_mc_sa.txt', ...
%                      'OutputType', 'string'));

         
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
%sev_arr = [100, 250, 500];
%ext_arr = [45];
sev_arr = [375];
%sev_arr = [100,150, 175, 250, 330, 375, 400, 500,750, 1000];
ext_arr =  [15, 30, 45, 60, 90,120];
loc_arr = {'a'; 'i'; 'l'};
loc_arr_full = {'Ant'; 'Inf'; 'Lat'};

[X, Y] = meshgrid(1:128);

Nx = 48; 
Ny = 48;
Nz = 32; %original
%Nz = 30;
%Nz = 48;

for ind_pat = pat_range
pat_id = pat_id_arr{ind_pat};
tStart = tic;

%% calculate centroid
% fold = ['data/def_segments/' pat_id];
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
%   fold = ['data/def_segments/' pat_id];
  fname = [fold, '/_SA_def_' def_name '.mat'];
  load(fname);
  
  def_mask = imresize3(def_mask, ...
                        [res_factor_reorient / res_factor_seg, ...
                        res_factor_reorient / res_factor_seg,...
                        res_factor_reorient].*size(def_mask), ...
                        'Method', 'linear');
  try
    def_mask = def_mask(c_seg(2)-Ny/2:c_seg(2)+Ny/2-1, ...
                        c_seg(1)-Nx/2:c_seg(1)+Nx/2-1, ...
                        c_seg(3)-Nz/2:c_seg(3)+Nz/2-1);
  
  catch
    % Size of the input volume
    [H, W, D] = size(def_mask);
    % Desired size
    cropSize = [Ny, Nx, Nz];

    % Center coordinates
    cy = c_seg(2);
    cx = c_seg(1);
    cz = c_seg(3);

    % Compute the start and end indices
    ys = cy - floor(Ny/2); ye = ys + Ny - 1;
    xs = cx - floor(Nx/2); xe = xs + Nx - 1;
    zs = cz - floor(Nz/2); ze = zs + Nz - 1;

    % Initialize with zeros
    padded_crop = zeros(Ny, Nx, Nz, class(def_mask));

    % Determine valid ranges within bounds
    y_src = max(ys,1):min(ye,H);
    x_src = max(xs,1):min(xe,W);
    z_src = max(zs,1):min(ze,D);

    % Destination indices in the padded array
    y_dst = (y_src - ys + 1);
    x_dst = (x_src - xs + 1);
    z_dst = (z_src - zs + 1);

    % Assign cropped data
    padded_crop(y_dst, x_dst, z_dst) = def_mask(y_src, x_src, z_src);

    % Replace the original
    def_mask = padded_crop;
  end

  def_mask = def_mask > 0;
  cur_fold = fullfile(base_res_dir_new, pat_id);
  if ~isfolder(cur_fold); mkdir(cur_fold); end
  fname = fullfile(cur_fold, ['def_mask_' def_name_half '.bin']);
  my_fwrite(fname, def_mask, 'uint8');
  
end
end

fprintf('Progress: %d/%d || ET: %.4f\n', ind_pat, num_pat, toc(tStart));
fprintf('================================================\n');
end
              
