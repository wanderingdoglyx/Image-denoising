clc; clear all; close all;
%addpath('../SPIE_8_3/src/');
addpath('src/')

%prev_folder = 'C:\Users\y.zezhang\Documents\SPIE_10_31';
%%

%hd_flag = ['_hd_mirirv3'];
%pat_list_fname = [prev_folder 'data/test_all_pat_info' hd_flag '.mat'];
%[act_pat_id_arr, pat_id_arr, study_date_arr] = get_pat_list('F:\wustl\3.0\defect_insertion\data\test_all_pat_info.mat');
%month_flag = cellstr(readmatrix([prev_folder '/data/test_month_flag' hd_flag '.txt'], 'OutputType', 'string'));

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

%seg_date = {'2022-11-02'};
%series_desc_sa_recon = '_Short.Axis.ReconSA_';
%segment_folder = [prev_folder 'data/segments_sa_mim_renamed/'];


defect_type_arr = {'Ant', 'Inf', 'Lat', 'Sep', 'TAnt', 'TInf'};
defect_extent_d_arr = [15, 30, 45, 60, 90,120];
defect_extent_d_arr_baseline = [120, 150, 170];

num_pat = length(SA_folderList);

pat_range = 1:num_pat;
flag_save_dicom = 0;

%% 
series_desc_sa_recon = '_Short.Axis.ReconSA_';
%series_desc_sa_recon = '_SA_seg_';
% series_desc_sa_recon = '_SA.DS_';
series_desc_ax_recon = '_ReconPrimDS_';

num_pat = length(SA_folderList);

pat_range = 1:num_pat;

%%
for ind_pat = pat_range %101:195

    series_trail_id = 2000; %Asheq: 7/5/22 - 7/18/22

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
    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  tStart = tic;
  %%
  %act_pat_id = act_pat_id_arr{ind_pat};
  %pat_id = pat_id_arr{ind_pat};
  %study_date = study_date_arr{ind_pat};

  %fdir = ['D:\MIM\MIRIR_data_' month_flag{ind_pat} '_mim_7\' study_date '__Studies\'];
  %series_desc_sa_recon = ['seg__SA_seg_'];
    fdir='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/';
  %% read di_tx, di_sa

    fdir_sa='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match_v2/';
%   try
    S = ze_get_dir(fdir_sa, series_desc_sa_recon, pat_id);
    S_dcm = dir(fullfile([fdir_sa, S],'*.dcm'));
    S_dcm = S_dcm(1).name;
    fname = [fdir_sa, S, filesep, S_dcm];
    di_sa = dicominfo(fname);
%   catch
%     continue;
%   end
  fdir_tx='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/TX_folder_match_v2/';
  
  S = ze_get_dir(fdir_tx, series_desc_ax_recon, pat_id);
  S_dcm = dir(fullfile([fdir_tx, S],'*.dcm'));
  S_dcm = S_dcm(1).name;
  fname = [fdir_tx, S, filesep, S_dcm];
  di_ax = dicominfo(fname);
  
  S_ax = S;
  
  %% S1: load seg
  series_desc = '_SA_seg_';
  data_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/def_segments_v2/' pat_id];
  if ~isfolder(data_dir); continue; end
  load([data_dir, filesep, series_desc], 'lv_mask');
  
  lv_mask = imresize3(lv_mask, [di_sa.Rows, di_sa.Columns, di_sa.NumberOfSlices], 'Method', 'nearest');
  method = 'linear';
  [Fint, Xq, Yq, Zq] = get_interpolant_align_sa_image(di_sa, lv_mask, di_ax, method);
  aligned_sa_recon = align_sa_image_acc(Xq, Yq, Zq, lv_mask, Fint);
%   aligned_sa_recon = align_sa_image(di_sa, lv_mask, di_ax);

  % save aligned
  save_data_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/aligned_def_segments_v2/' pat_id];
  if ~isfolder(save_data_dir); mkdir(save_data_dir); end
  save([save_data_dir, filesep, 'Aligned' series_desc], 'aligned_sa_recon');
  
  if (flag_save_dicom)
    new_series_desc = ['_Aligned' series_desc];
    save_aligned_seg_def_in_dicom(...
            di_ax, new_series_desc, series_desc_ax_recon, ...
            fdir, series_trail_id, S_ax, ...
            aligned_sa_recon)
    series_trail_id = series_trail_id + 1;
  end
  %%
  for ind_def = 1:numel(defect_type_arr)
    defect_type = defect_type_arr{ind_def};
    defect_extent_z = 21; %in mm
    %defect_extent_d = 60;
    
    for defect_extent_d = defect_extent_d_arr
      series_desc = ['_SA_def_' defect_type 'Z' num2str(defect_extent_z) 'D' num2str(defect_extent_d) '_'];
      load([data_dir, filesep, series_desc], 'def_mask');
      
      def_mask = imresize3(def_mask, [di_sa.Rows, di_sa.Columns, di_sa.NumberOfSlices], 'Method', 'nearest');
%       aligned_sa_recon = align_sa_image(di_sa, def_mask, di_ax);
      aligned_sa_recon = align_sa_image_acc(Xq, Yq, Zq, def_mask, Fint);
      save([save_data_dir, filesep, 'Aligned' series_desc], 'aligned_sa_recon');
      
      if (flag_save_dicom)
        new_series_desc = ['_Aligned' series_desc];
        save_aligned_seg_def_in_dicom(...
                di_ax, new_series_desc, series_desc_ax_recon, ...
                fdir, series_trail_id, S_ax, ...
                aligned_sa_recon);
        series_trail_id = series_trail_id + 1;
      end
    end
    
    % baseline
    defect_extent_z = 28; %in mm
    for defect_extent_d = defect_extent_d_arr_baseline
      series_desc = ['_SA_def_' defect_type 'Z' num2str(defect_extent_z) 'D' num2str(defect_extent_d) '_'];
      load([data_dir, filesep, series_desc], 'def_mask');

      def_mask = imresize3(def_mask, [di_sa.Rows, di_sa.Columns, di_sa.NumberOfSlices], 'Method', 'nearest');
  %     aligned_sa_recon = align_sa_image(di_sa, def_mask, di_ax);
      aligned_sa_recon = align_sa_image_acc(Xq, Yq, Zq, def_mask, Fint);
      save([save_data_dir, filesep, 'Aligned' series_desc], 'aligned_sa_recon');

      if (flag_save_dicom)
        new_series_desc = ['_Aligned' series_desc];
        save_aligned_seg_def_in_dicom(...
                di_ax, new_series_desc, series_desc_ax_recon, ...
                fdir, series_trail_id, S_ax, ...
                aligned_sa_recon)
        series_trail_id = series_trail_id + 1;
      end
    end
  end
  fprintf('Progress: %d/%d || Pat: %s || Act Pat: %s || ET: %.4f\n', ind_pat, num_pat, pat_id, act_pat_id, toc(tStart));
  
end
