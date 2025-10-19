clc; clear all; close all;

%addpath('../SPIE_8_3/src/');
addpath('src/')
%prev_folder = '../SPIE_10_31/';


%%
folderPath = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/LV_mask/LV_mask_v2'; % Specify the folder path
sag_filePattern = fullfile(folderPath, '*.mat'); % Search for .mat files
matFiles = dir(sag_filePattern); % Get all .mat files

sag_fileList = cell(length(matFiles), 1); % Initialize cell array for file paths

for k = 1:length(matFiles)
    sag_fileList{k} = fullfile(folderPath, matFiles(k).name); % Store full path
end


% list SA DCM subfolders

%SA_folderPath = 'D:\wustl\3.0\defect_insertion\ze_defect_insertion\tenp_sa3'; % Specify the main folder path
SA_folderPath = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match_v2'; % Specify the main folder path
SA_subfolders = dir(SA_folderPath); 


SA_folderList = {}; % Initialize empty cell array for folder paths

for k = 1:length(SA_subfolders)
    if SA_subfolders(k).isdir && ~startsWith(SA_subfolders(k).name, '.')
        SA_folderList{end+1} = fullfile(SA_folderPath, SA_subfolders(k).name);
    end
end
%%

%%

%pat_list_fname = [prev_folder 'data/test_all_pat_info_hd_mirirv3.mat'];
%[act_pat_id_arr, pat_id_arr, study_date_arr] = get_pat_list(pat_list_fname);

%month_flag = cellstr(readmatrix([prev_folder 'data/test_month_flag_hd_mirirv3.txt'], 'OutputType', 'string'));

%%
num_pat = length(SA_folderList);
pat_range = 1:num_pat;
%%

%% S1: 
%sc_factor_castor = 100;

hl_obj_prefix = 'hl';
ct_prefix = 'ctlow';

def_extend_z = 21;
def_extend_d_arr = [30, 60];
def_loc_full_arr = {'Ant'; 'Inf'; }; 
def_loc_short_arr = {'A'; 'I'; };
sev_arr =  [0, 0.375]; 



%def_extend_d_arr = [15, 30, 45, 60, 90,120];%total
%def_loc_full_arr = {'Ant'; 'Inf'; 'Lat'; 'Sep'; 'TAnt'; 'TInf'; 'AntLat'; 'InfLat';};
%def_loc_full_arr = {'Ant'; 'Inf'; 'Lat'; 'Sep'; 'TAnt'; 'TInf';}; %total
%def_loc_short_arr = {'A'; 'I'; 'L'; 'S'; 'TA'; 'TI'; 'AL'; 'IL'}; %total
%sev_arr =  [0, 0.1, 0.15, 0.175, 0.25, 0.33, 0.375, 0.40 ,0.5, 0.75, 1]; %total

%sev_arr =  [0.375]; 

save_folder = ...
  '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image/';
  %'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie_v2\test_mc_castor_mirirv3_apr3\';
if ~isfolder(save_folder); mkdir(save_folder); end

%castor_recon_folder = ...
%  '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/castor_recon/';
  %'Z:\Active\rahman.m\projects\dl_denoising\debug\db_defect_insertion\data_spie\test_data_mirirv3\';
%%
castor_recon_folder = ...
  '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC/';


sc_obj = 100;
save_hl_obj = 0;
save_ct = 0;

for ind_pat = pat_range                  %1:length(pat_id_arr) %ind_pat = 1:100
  tStart = tic;
%   fprintf('progress: %d/%d\n', ind_pat, length(pat_id_arr));

  %study_date = study_date_arr{ind_pat};
  %pat_id = pat_id_arr{ind_pat};
  %act_pat_id = act_pat_id_arr{ind_pat};

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  select_subfolderPath=SA_folderList{ind_pat};
  
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
  %act_pat_id = act_pat_id_arr{ind_pat};
  
  % Extract Study Date
  if isfield(dcmInfo, 'StudyDate')
      studyDate = dcmInfo.StudyDate; % Format: YYYYMMDD
      formattedDate = sprintf('%s-%s', studyDate(1:4), studyDate(5:6)); % Convert to YYYY-MM
  else
      studyDate = 'Unknown';
      formattedDate = 'Unknown';
  end
  
  study_date=studyDate;

  [~, pat_folderName] = fileparts(select_subfolderPath);

  % Split the filename by underscores
  parts = strsplit(pat_folderName, '_');
      
      % Extract the 3rd element (which contains the number)
  if length(parts) >= 3
      extractedNumber = parts{2}; 
      fprintf('Extracted Number: %s\n', extractedNumber);
  else
      fprintf('Filename format does not match expected structure.\n');
  end


  %pat_id = pat_id_arr{ind_pat};
  pat_id = extractedNumber;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


  %fdir = ['D:\MIM\MIRIR_data_' month_flag{ind_pat} '_mim_7\' study_date '__Studies\'];
  fdir='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/defect_inserted_image/';

  pat_folder = [save_folder pat_id '/'];
  if ~isfolder(pat_folder); mkdir(pat_folder); end
  data_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments_v2/', pat_id, '/'];
  if ~isfolder(data_dir); continue; end
  

  %castor_recon_fname = [castor_recon_folder, pat_id, filesep, 'orig_proj_hd_' num2str(pat_id) '_d1_it8.img'];
  castor_recon_fname = [castor_recon_folder, pat_id, '/', pat_id ,'_it8.img'];

  fname = castor_recon_fname;
  recon_cast = my_fread(fname, inf, 'float32');
  recon_cast = reshape(recon_cast, [64,64,64]);
  recon_cast = process_castor_recon(recon_cast);
  

  if (save_hl_obj)
    hl_recon = recon_cast;
    hl_recon = permute(hl_recon, [2,1,3]);
    hl_recon = round(hl_recon * sc_obj);

    my_fwrite([pat_folder hl_obj_prefix, '_obj_act_av.bin'], hl_recon, 'float32');
  end
  
  
%   sc_obj = sc_obj_arr{ind_pat};
  
  for ind_def = 1:length(def_loc_full_arr)
    %%
    def_loc_full = def_loc_full_arr{ind_def};
    def_loc = def_loc_short_arr{ind_def};
    
    %lv_template_fname = ['Aligned_SA_def_' def_loc_full 'Z28D170']; latest
    lv_template_fname = ['Aligned_SA_seg'];

    lv_template = load([data_dir, lv_template_fname, '_.mat']);
    fld = fieldnames(lv_template);
    lv_template = lv_template.(fld{1});
    
    for def_extend_d = def_extend_d_arr
      def_template_fname = ...
        ['Aligned_SA_def_' def_loc_full 'Z' num2str(def_extend_z) 'D' num2str(def_extend_d)];
      def_template = load([data_dir, def_template_fname, '_.mat']);
      fld = fieldnames(def_template);
      def_template = def_template.(fld{1});
      
      for sev = sev_arr
          def_obj_prefix = ['d' def_loc num2str(def_extend_z) num2str(def_extend_d) 's' num2str(sev*1000)];
          def_obj_prefix_half = ['d' def_loc num2str(def_extend_z) num2str(def_extend_d)];
          defect_insertion_v2(fdir, pat_id, ...
                              sev, hl_obj_prefix, def_obj_prefix, def_obj_prefix_half, ct_prefix, ...
                              lv_template, def_template, sc_obj, ...
                              save_folder, recon_cast ...
                            );
      end
    end
  end


  %% save ct map 
  if (save_ct)
    S = get_dir(fdir, 'RegCTLow', pat_id);
    S_dcm = dir(fullfile([fdir,S], '*.dcm'));
    CT = dicomreadVolume([fdir,S]);
    CT = process_ct_data(CT);
    pixel_size = 0.68;
    CT = CT * pixel_size;
    % figure;imshow3D(CT);colormap gray;

    my_fwrite([pat_folder ct_prefix '_atn_av.bin'], CT, 'float32')
  end
  fprintf('Progress: %d/%d || Pat: %s || Act Pat: %s || ET: %.4f\n', ...
    ind_pat, num_pat, pat_id, act_pat_id, toc(tStart));
end

