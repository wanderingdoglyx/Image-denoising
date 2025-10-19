clc; clear all; close all;

%addpath('../SPIE_8_3/src/');

addpath('src/')

%prev_folder = '../SPIE_10_31/';


% list SA DCM subfolders

%SA_folderPath = 'D:\wustl\3.0\defect_insertion\ze_defect_insertion\tenp_sa3'; % Specify the main folder path
SA_folderPath = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match'; % Specify the main folder path
SA_subfolders = dir(SA_folderPath); 


SA_folderList = {}; % Initialize empty cell array for folder paths

for k = 1:length(SA_subfolders)
    if SA_subfolders(k).isdir && ~startsWith(SA_subfolders(k).name, '.')
        SA_folderList{end+1} = fullfile(SA_folderPath, SA_subfolders(k).name);
    end
end

% Set the root folder path
rootFolder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/pre_projection';  

% Get all items in the folder
items = dir(rootFolder);

% Filter only directories and exclude '.' and '..'
isSubfolder = [items.isdir] & ~ismember({items.name}, {'.', '..'});

% Get only the names of the first-level subfolders
pat_id_arr = {items(isSubfolder).name};

%%

%pat_list_fname = [prev_folder 'data/test_all_pat_info_hd_mirirv3_mc.mat'];
%[act_pat_id_arr, pat_id_arr, study_date_arr] = get_pat_list(pat_list_fname);
%month_flag = cellstr(readmatrix([prev_folder 'data/test_month_flag_hd_mirirv3_mc.txt'], ...
%                      'OutputType', 'string'));



%%
%def_loc_full_arr = {'Ant'; 'Inf'; 'Lat'; 'Sep'; 'TAnt'; 'TInf'; 'AntLat'; 'InfLat';}; %total
%def_loc_obj_arr = {'A'; 'I'; 'L'; 'S'; 'TA'; 'TI'; 'AL'; 'IL'}; %: total
def_loc_full_arr = {'Ant'; 'Inf';};
def_loc_obj_arr = {'A'; 'I'; }; %Asheq: 9/5/22
def_loc_arr = lower(def_loc_obj_arr);


sev_arr =  [0, 0.1, 0.15, 0.175, 0.25, 0.33,0.375, 0.40 ,0.5, 0.75, 1]; %total
def_extent_d_arr = [15, 30, 45, 60, 90,120]; %total


%sev_arr =  [0.375]; 
%def_extent_d_arr = [30, 60]; 


def_extent_z = 21;

sc_obj = 1e-4;
max_scale = 10;

%base_res_dir = ...
%  'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie_v2\';

%base_res_dir_prev = ...
%  'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie\';

castor_recon_folder = ...
  '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC/';

data_dir = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments/';

pat_range = 1:length(pat_id_arr);

%prob_reject_arr = 1 - [1, 3/4, 1/2, 1/4, 1/8, 1/16];
%num_dose_levels = 8;
%prob_reject_arr = 1 - [1,1/3];
num_dose_levels = [100,33,25];

for ind_pat = pat_range %1

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  pat_id = pat_id_arr{ind_pat};

  matches = contains(SA_folderList, pat_id);

  % Extract the matched elements
  matchedElements = SA_folderList(matches);
  select_subfolderPath=matchedElements{1};

  % Find the DICOM file in the subfolder
  dcmFiles = dir(fullfile(select_subfolderPath, '*.dcm'));
  
  if isempty(dcmFiles)
      fprintf('No DICOM file found in %s\n', select_subfolderPath);
      continue;
  end
  
  dcmFilePath = fullfile(select_subfolderPath, dcmFiles(1).name); % Assume first DICOM file


  % Read DICOM file and extract Patient's Name
  dcmInfo = dicominfo(dcmFilePath);
  if isfield(dcmInfo, 'PatientName')
      patientName = dcmInfo.PatientName.FamilyName; % Extract patient name
  else
      fprintf('No Patient Name found in %s\n', dcmFilePath);
      continue;
  end

  act_pat_id = patientName;


  % Extract Study Date
  if isfield(dcmInfo, 'StudyDate')
    studyDate = dcmInfo.StudyDate; % Format: YYYYMMDD
    formattedDate = sprintf('%s-%s', studyDate(1:4), studyDate(5:6)); % Convert to YYYY-MM
  else
    studyDate = 'Unknown';
    formattedDate = 'Unknown';
  end

  study_date=studyDate;

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  tStart = tic;
  
  %study_date = study_date_arr{ind_pat};
  %pat_id = pat_id_arr{ind_pat};

  fdir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/high_dose_reg_PriPrj_ScaPrj_RegCT_DICOM_total/'];

  pre_projection_res_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/pre_projection' filesep pat_id];
  recostruction_res_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC' filesep pat_id];
  defect_insertion_res_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image' filesep pat_id];
  ori_prejection_res_dir=['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100',filesep pat_id];
  %res_dir_prev = [base_res_dir_prev 'test_data_mirirv3' filesep pat_id];
  new_res_dir = [ '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_def' filesep pat_id ];
  
%   if isempty(find(strcmp(pat_not_fin, pat_id))); continue; end
  
  %% save for castor pipeline
%   fname = [res_dir '/orig_proj_' num2str(pat_id) '.a00'];
%   orig_proj = permute(orig_proj, [2,1,3]);
%   my_fwrite(fname, orig_proj, 'float32');
%   

  %% code for mean activity (read hl recon)
  %castor_recon_fname = [castor_recon_folder, pat_id, filesep, 'orig_proj_hd_' num2str(pat_id) '_d1_it8.img'];
  castor_recon_fname = [castor_recon_folder, pat_id, filesep, num2str(pat_id) '_it8.img'];

  fname = castor_recon_fname;
  recon_cast = my_fread(fname, inf, 'float32');
  recon_cast = reshape(recon_cast, [64,64,64]);
  recon_cast = process_castor_recon(recon_cast);


  
  %% read original projection
  S = ze_get_dir(fdir, '_PriPrj_', pat_id);
  S_dcm = dir(fullfile([fdir, S],'*.dcm'));
  S_dcm = S_dcm(1).name;
  fname = [fdir, S, filesep, S_dcm];
  
  di = dicominfo(fname);
  %num_of_projection = di.RotationInformationSequence.Item_1.NumberOfFramesInRotation;
  num_of_projection =30;

  %% hl
  fname = [pre_projection_res_dir '/dA2115s0/simind_smc_tot_w1.a00'];
  hl_proj = my_fread(fname, inf, 'float32');
  hl_proj = reshape(hl_proj, [64,64,num_of_projection]);
  hl_proj = permute(hl_proj, [2,1,3]);
  
  %fname = [defect_insertion_res_dir '/hl_obj_act_av.bin'];
  fname = [defect_insertion_res_dir '/dA2115s0_obj_act_av.bin'];
  hl_obj = my_fread(fname, inf, 'float32');
  
  %hl_proj = sum(hl_obj) * sc_obj * hl_proj; %origin
    
  %% def
  for ind_def_loc = 1:length(def_loc_obj_arr)
    def_loc_obj = def_loc_obj_arr{ind_def_loc};

    for def_extent_d = def_extent_d_arr
      
      def_name_obj_half = ...
        ['d' def_loc_obj num2str(def_extent_z) num2str(def_extent_d)]; 
      %def_name_half = [lower(def_name_obj_half) 's1e4'];

      %% read LV mask
      %lv_template_fname = ['Aligned_SA_def_' def_loc_full_arr{ind_def_loc} 'Z28D170'];%latest
      lv_template_fname = ['Aligned_SA_seg'];

      lv_template = load([data_dir, filesep, pat_id, filesep, lv_template_fname, '_.mat']);
      fld = fieldnames(lv_template);
      lv_template = lv_template.(fld{1});
      
      %% read objects and simind projections
      %fname = [pre_projection_res_dir '/out_' def_name_half '_tot_w1.a00'];
      for sev = sev_arr
        def_name_full= [def_name_obj_half 's' num2str(sev*1000)];

        fname = [pre_projection_res_dir '/' def_name_full '/' 'simind_smc_tot_w1.a00'];

        def_proj = my_fread(fname, inf, 'float32');
        def_proj = reshape(def_proj, [64,64,num_of_projection]);
        def_proj = permute(def_proj, [2,1,3]);
        
        fname = [defect_insertion_res_dir '/' def_name_obj_half '_act_av.bin'];
        def_obj = my_fread(fname, inf, 'float32');
        def_obj = double(def_obj>0);

      %for sev = sev_arr
        def_name_obj = ...
        ['d' def_loc_obj num2str(def_extent_z) num2str(def_extent_d) ...
          's' num2str(sev*1000)]; 
        def_name = lower(def_name_obj);
        %% compute defect-present projection
        def_activity = sev * get_mean_lv_uptake(recon_cast, lv_template);
        cur_def_proj = sum(def_obj) * def_activity * ...
                    sc_obj * def_proj;
        def_pr_proj = hl_proj - cur_def_proj;
        def_pr_proj(def_pr_proj<0) = 0;

        %% process scale factor
       % scaled_factor = def_pr_proj./hl_proj; %origin
        scaled_factor = def_proj./hl_proj;
        scaled_factor(isnan(scaled_factor)) = 1;
        scaled_factor(isinf(scaled_factor)) = 1;
        scaled_factor(scaled_factor == 0) = 1;
        scaled_factor(scaled_factor > max_scale) = 1;

        %% modify projection
        %for ind_prob = 1:num_dose_levels
        for ind_prob =  num_dose_levels

          dose_name = ['d' num2str(ind_prob)];
          %fname = [res_dir_prev '/orig_proj_hd_' num2str(pat_id) '_' dose_name '.a00'];
          fname = [ori_prejection_res_dir '/' num2str(pat_id) '.a00'];

          orig_proj = my_fread(fname, inf, 'float32');
          orig_proj = reshape(orig_proj, [64,64,num_of_projection]);
          orig_proj = permute(orig_proj, [2,1,3]);
          
          mod_proj = orig_proj .* scaled_factor;
          

          %% save for castor pipeline
          new_dir = new_res_dir;
          if ~isfolder(new_dir); mkdir(new_dir); end

          
          mod_proj = permute(mod_proj, [2, 1, 3]);
          
          proj_data_ss = binomial_subsampling(mod_proj, 1-ind_prob/100);
          

          fname = [new_dir '/mod_proj_' def_name '_' num2str(pat_id) '_' dose_name  '.a00'];
          my_fwrite(fname, proj_data_ss, 'float32');
          
        end
      end
    end
  end
  tEnd = toc(tStart);
  fprintf('progress: %d/%d || Elapsed time: %.4f\n', ind_pat, length(pat_id_arr), tEnd);
end
