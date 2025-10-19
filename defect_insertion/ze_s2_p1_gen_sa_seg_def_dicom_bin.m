clc; clear all; close all;

%addpath('../SPIE_8_3/src/');
addpath('./src');

%prev_folder = '../SPIE_10_31/';

% list sag mat files
%folderPath = 'D:\wustl\3.0\defect_insertion\ze_defect_insertion\tenp_sa3'; % Specify the folder path

folderPath = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/LV_mask/LV_mask_all'; % Specify the folder path
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

seg_date = {'2025-04-24'};
series_desc_sa_recon = '_Short.Axis.ReconSA_';
segment_folder = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/LV_mask/LV_mask_v2'];
%segment_folder = [prev_folder 'data/segments_sa_mim_renamed/'];

defect_type_arr = {'Ant', 'Inf', 'Lat', 'Sep', 'TAnt', 'TInf', 'AntLat', 'InfLat'};

defect_extent_d_arr = [15, 30, 45, 60, 90,120]; 
defect_extent_d_arr_baseline = [120, 150, 170];

num_pat = length(SA_folderList);

pat_range = 1:num_pat;


for ind_pat = pat_range
    series_trail_id=100;
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
    
    study_date = formattedDate;
    %fdir = ['D:\MIM\MIRIR_data_' month_flag{ind_pat} '_mim_7\' study_date '__Studies\'];
    fdir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/SA_folder_match']; 
    %% S1: do segment -> save -> load hr seg
    fwd_rat = 4;
    sc_factor = 1000;
    series_desc = '_SA_seg_';
     flag_save = 0;
     series_trail_id = series_trail_id + 1;

    % [lv_mask, DI_resliced_base, flag_seg] = ze_get_lv_seg_resized(...
    %          fdir, pat_id, act_pat_id, seg_date, fwd_rat, ...
    %          sc_factor, series_desc, series_desc_sa_recon, flag_save, ...
    %         segment_folder,series_trail_id);

    [lv_mask, DI_resliced_base, flag_seg] = ze_get_lv_seg(...
            fdir, pat_id, act_pat_id, seg_date, fwd_rat, ...
            sc_factor, series_desc, series_desc_sa_recon, flag_save, ...
            segment_folder,series_trail_id);

    if ~flag_seg; continue; end
    %fprintf('progress: %d/%d || sum_seg: %d\n', ind_pat, length(pat_id_arr), sum(lv_mask(:)));
    fprintf('progress: %d/%d || sum_seg: %d\n', ind_pat, num_pat, sum(lv_mask(:)));
    data_dir = ['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/def_segments_v2/' pat_id];
     if ~isfolder(data_dir); mkdir(data_dir); end
    %save([data_dir, filesep, series_desc], 'lv_mask');
    save([data_dir, filesep, series_desc], 'lv_mask');
%   figure; imshow3D(double(lv_mask>0) - double(lv_mask>0.5))
  %%
%   lv_mask = double(lv_mask>0);
     flag_save = 0;
     for ind_def = 1:numel(defect_type_arr)
         defect_type = defect_type_arr{ind_def};
         defect_extent_z = 21; %in mm
          %defect_extent_d = 60;
    
        for defect_extent_d = defect_extent_d_arr
          series_desc = ['_SA_def_' defect_type 'Z' num2str(defect_extent_z) 'D' num2str(defect_extent_d) '_'];
          series_trail_id = series_trail_id + 1;
          def_mask = ze_get_def_mask_newdef_fixed(...
                        fdir, pat_id, fwd_rat, sc_factor, lv_mask, ...
                        defect_extent_z, defect_extent_d, ...
                        DI_resliced_base, series_desc, ...
                        defect_type, series_desc_sa_recon, series_trail_id, flag_save);
        %  save([data_dir, filesep, series_desc], 'def_mask');
          save([data_dir, filesep, series_desc], 'def_mask');
    %       sum(def_mask(:))
    %       sum(def_mask>0 & def_mask<0.2, 'all')
        end
    
    %
        % baseline
        defect_extent_z = 28; %in mm
        for defect_extent_d = defect_extent_d_arr_baseline
          series_desc = ['_SA_def_' defect_type 'Z' num2str(defect_extent_z) 'D' num2str(defect_extent_d) '_'];
          series_trail_id = series_trail_id + 1;
          def_mask = ze_get_def_mask_newdef_fixed(...
                        fdir, pat_id, fwd_rat, sc_factor, lv_mask, ...
                        defect_extent_z, defect_extent_d, ...
                        DI_resliced_base, series_desc, ...
                        defect_type, series_desc_sa_recon, series_trail_id, flag_save);
          %save([data_dir, filesep, series_desc], 'def_mask');
         save([data_dir, filesep, series_desc], 'def_mask');
    %       sum(def_mask(:))
    %       sum(def_mask>0 & def_mask<0.2, 'all')
        end
      end
  
  
end

