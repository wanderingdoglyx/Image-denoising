function def_mask = ze_get_def_mask_newdef_fixed(...
                        fdir, pat_id, fwd_rat, sc_factor, lv_mask, ...
                        defect_extent_z, defect_extent_d, ...
                        DI_resliced_base, series_desc, ...
                        defect_type, series_desc_sa_recon, series_trail_id, flag_save)

DI_resliced = DI_resliced_base;
%% defect location
stats = regionprops(lv_mask);
centroid = round(stats.Centroid);

%in mm
shift_slice = 0;
slice_extent = round(defect_extent_z/DI_resliced.SliceThickness);
start_slice = centroid(3) + shift_slice - slice_extent;
end_slice = centroid(3) + shift_slice + slice_extent;

defect_mask = zeros(size(lv_mask));

[X, Y] = meshgrid(1:size(lv_mask,1), flip(1:size(lv_mask,2)));
X = X - centroid(1);
Y = Y - (size(lv_mask,1) - centroid(2)+1);

X_by_Y_base = abs(atand(Y./X));
X_by_Y = X_by_Y_base;
X_by_Y(X < 0 & Y > 0) = 180 - X_by_Y(X < 0 & Y > 0);
X_by_Y(X < 0 & Y < 0) = 180 + X_by_Y(X < 0 & Y < 0);
X_by_Y(X > 0 & Y < 0) = 360 - X_by_Y(X > 0 & Y < 0);
X_by_Y(X == 0 & Y < 0) = 270;
X_by_Y(X == 0 & Y > 0) = 90;
X_by_Y(Y == 0 & X < 0) = 180;
X_by_Y(Y == 0 & X > 0) = 0;

%%
switch defect_type
  case 'Ant'
    start_ang = 80;
    end_ang = start_ang - defect_extent_d;
    
    if (end_ang < 0)
      end_ang = 360 + end_ang;
      mask = X_by_Y < start_ang | X_by_Y > end_ang;
    else
      mask = X_by_Y < start_ang & X_by_Y > end_ang;
    end
   for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
  case 'Inf'
    start_ang = 280;
    end_ang = start_ang + defect_extent_d;
    if (end_ang > 360)
      end_ang = mod(end_ang, 360);
      mask = X_by_Y > start_ang | X_by_Y < end_ang;
    else
      mask = X_by_Y > start_ang & X_by_Y < end_ang;
    end
    
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
  case 'Lat'
    mask = X_by_Y_base <  defect_extent_d/2;
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z) & (X > 0);
    end
  case 'Sep'
    mask = X_by_Y_base <  defect_extent_d/2;
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z) & (X < 0);
    end
  case 'TAnt'
    mask = (X_by_Y >  90 - defect_extent_d/2) ...
            & (X_by_Y <  90 + defect_extent_d/2);
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
  case 'TInf'
    mask = (X_by_Y >  270 - defect_extent_d/2) ...
            & (X_by_Y <  270 + defect_extent_d/2);
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
  case 'AntLat'
    start_ang = 45 + defect_extent_d/2;
    end_ang = 45 - defect_extent_d/2;
    
    if (end_ang < 0)
      end_ang = 360 + end_ang;
      mask = X_by_Y < start_ang | X_by_Y > end_ang;
    else
      mask = X_by_Y < start_ang & X_by_Y > end_ang;
    end
   for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
  case 'InfLat'
    start_ang = 315 - defect_extent_d/2;
    end_ang = 315 + defect_extent_d/2;
    if (end_ang > 360)
      end_ang = mod(end_ang, 360);
      mask = X_by_Y > start_ang | X_by_Y < end_ang;
    else
      mask = X_by_Y > start_ang & X_by_Y < end_ang;
    end
    
    for ind_z = start_slice:end_slice
      defect_mask(:, :, ind_z) = mask .* lv_mask(:, :, ind_z);
    end
end
  
def_mask = defect_mask;
% figure(1); imagesc(mask+squeeze(lv_mask(:,:,centroid(3)))); 
% colormap gray; title(pat_id);waitforbuttonpress; 
% figure; imshow3D(defect_mask);
%% save in dicom
if flag_save
  DI_resliced.SeriesDescription = strip(series_desc, '_');
  DI_resliced.Width = DI_resliced.Width * fwd_rat;
  DI_resliced.Height = DI_resliced.Height * fwd_rat;
  DI_resliced.Rows = DI_resliced.Rows * fwd_rat;
  DI_resliced.Columns = DI_resliced.Columns * fwd_rat;
  DI_resliced.PixelSpacing = DI_resliced.PixelSpacing/fwd_rat;

  % change series
  DI_resliced.SeriesInstanceUID = [DI_resliced.SeriesInstanceUID '.' num2str(series_trail_id)];
  DI_resliced.SeriesNumber = DI_resliced.SeriesNumber + series_trail_id;

  Nx = size(defect_mask,1); Ny = size(defect_mask,2); Nz = size(defect_mask,3);
  defect_mask = reshape(defect_mask, [Nx, Ny, 1, Nz]);
  defect_mask = uint16(defect_mask * sc_factor);

  S = get_dir(fdir, series_desc_sa_recon, pat_id);
  mod_str = strrep(S, series_desc_sa_recon, series_desc);
  new_fdir = [fdir, filesep, mod_str];
  if ~isfolder(new_fdir); mkdir(new_fdir); end

  fname = [new_fdir '/lv_def.dcm'];
  dicomwrite(defect_mask, fname, DI_resliced, 'CreateMode', 'Copy');
end
end