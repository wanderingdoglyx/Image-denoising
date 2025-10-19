function [lv_mask, DI_resliced_base, flag_seg] = ze_get_lv_seg(...
            fdir, pat_id, act_pat_id, seg_date, fwd_rat, ...
            sc_factor, series_desc, series_desc_sa_recon, flag_save, ...
            segment_folder, series_trail_id)
  flag_seg = 1;
  %% read resliced dicominfo
  S = get_dir(fdir, series_desc_sa_recon, pat_id);
  S_dcm = dir(fullfile([fdir,'/', S],'*.dcm'));
  S_dcm = S_dcm(1).name;
  fname = [fdir,'/', S, filesep, S_dcm];
  
  DI_resliced_base = dicominfo(fname);
  DI_resliced = DI_resliced_base;
  
  %% step-1: get the segmented LV
  for ind_date = 1:length(seg_date)

    file_name=ze_get_the_specific_mat_file(segment_folder, act_pat_id);
    fprintf('LV mask name: %s\n', file_name{1});
    fname = [segment_folder, '/',file_name{1}];

    if isfile(fname)
      load(fname);
      break;
    end
    if ind_date == length(seg_date)
      fprintf('Could not find: %s\n', fname);
      lv_mask = [];
      DI_resliced_base = [];
      flag_seg = 0;
      return;
    end
  end
  
  Yall = {setstruct.Roi.Y};
  Xall = {setstruct.Roi.X};
  Zall = {setstruct.Roi.Z};
  Name_all = {setstruct.Roi.Name};
  
  Nx = setstruct.XSize;
  Ny = setstruct.YSize;
  Nz = setstruct.ZSize;
  
  im_endo = zeros(Nx*fwd_rat, Ny*fwd_rat, Nz);
  im_epi = zeros(Nx*fwd_rat, Ny*fwd_rat, Nz);
  im = zeros(Nx*fwd_rat, Ny*fwd_rat, Nz);
  
  im_endo_fill = zeros(Nx*fwd_rat, Ny*fwd_rat, Nz);
  im_epi_fill = zeros(Nx*fwd_rat, Ny*fwd_rat, Nz);
  conn = 4;
  for i = 1:length(Zall)
    X = round(Xall{i}*fwd_rat);
    Y = round(Yall{i}*fwd_rat);
    Z = round(Zall{i});
    for j = 1:length(X)
      if strcmp(Name_all{i}, 'epicardium')
        im_epi(X(j), Y(j), Z) = 1;
      elseif strcmp(Name_all{i}, 'endocardium')
        im_endo(X(j), Y(j), Z) = 1;
      end
      im(X(j), Y(j), Z) = 1;
    end
    cur_im_epi = bwconvhull(squeeze(im_epi(:, :, Z)));
    cur_im_endo = bwconvhull(squeeze(im_endo(:, :, Z)));
    im_epi_fill(:, :, Z) = imfill(cur_im_epi, conn, 'holes');
    im_endo_fill(:, :, Z) = imfill(cur_im_endo, conn, 'holes');
    
  end
  
  im_epi_fill = double(im_epi_fill);
  im_endo_fill = double(im_endo_fill);
  lv_mask = im_epi_fill - im_endo_fill;
  
  % figure; imshow3D(im_epi);
  % figure; imshow3D(im_endo);
  % figure; imshow3D(im);
  % figure; imshow3D(im_endo_fill);
  % figure; imshow3D(im_epi_fill);
%   figure; imshow3D(lv_mask);
  lv_mask = flip(lv_mask, 3);
%   my_fwrite([segment_folder 'lv_mask_' act_pat_id '.bin'], lv_mask, 'float32')
  
  %%
  if (flag_save)
    DI_resliced.SeriesDescription = strip(series_desc, '_');
  
    DI_resliced.Width = DI_resliced.Width * fwd_rat;
    DI_resliced.Height = DI_resliced.Height * fwd_rat;
    DI_resliced.Rows = DI_resliced.Rows * fwd_rat;
    DI_resliced.Columns = DI_resliced.Columns * fwd_rat;
    DI_resliced.PixelSpacing = DI_resliced.PixelSpacing/fwd_rat;
  
    % change series
    DI_resliced.SeriesInstanceUID = [DI_resliced.SeriesInstanceUID '.' num2str(series_trail_id)];
    DI_resliced.SeriesNumber = DI_resliced.SeriesNumber + series_trail_id;

    Nx = size(lv_mask,1); Ny = size(lv_mask,2); Nz = size(lv_mask,3);
    lv_mask_dcm = reshape(lv_mask, [Nx, Ny, 1, Nz]);

    lv_mask_dcm = uint16(lv_mask_dcm * sc_factor);% origin ####################################################
  
    mod_str = strrep(S, series_desc_sa_recon, series_desc);
    new_fdir = [fdir, mod_str];
    if ~isdir(new_fdir); mkdir(new_fdir); end
  
    fname = [new_fdir filesep 'lv_mask.dcm'];
    IOD = 'Secondary Capture Image Storage';
    dicomwrite(lv_mask_dcm, fname, DI_resliced, 'CreateMode', 'Copy');
  end
end