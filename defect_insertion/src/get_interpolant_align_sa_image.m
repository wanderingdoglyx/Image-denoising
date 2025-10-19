function [Fint, Xq, Yq, Zq] = get_interpolant_align_sa_image(di_sa_recon, sa_recon, di_ax_recon, method)


  %% keep notations
  F = flip(reshape(di_sa_recon.ImageOrientationPatient, 3, 2), 2);
  del_r = di_sa_recon.PixelSpacing(1);
  del_c = di_sa_recon.PixelSpacing(1);
  S_xyz = di_sa_recon.ImagePositionPatient;
  del_s = di_sa_recon.SliceThickness;
  num_cols = double(di_sa_recon.Columns);
  num_rows = double(di_sa_recon.Rows);
  nv = cross(F(:,2), F(:,1));
  
  A_transform = eye(4,4);
  
  A_single = [ ...
      F(1,1)*del_r,   F(1,2)*del_c,   del_s * nv(1),    S_xyz(1);
      F(2,1)*del_r,   F(2,2)*del_c,   del_s * nv(2),    S_xyz(2);
      F(3,1)*del_r,   F(3,2)*del_c,   del_s * nv(3),    S_xyz(3);
      0,              0,              0,                1       ];
  
  num_slices = di_sa_recon.NumberOfFrames;
  
  [Col_coord, Row_coord] = ...
    meshgrid(0:num_cols-1, 0:num_rows-1);
  ALL_COORD = [
                Row_coord(:)';
                Col_coord(:)';
                zeros(1, numel(Row_coord));
                ones(1, numel(Col_coord));];
  %% get coordinates in mm
  ref_coord = [];
  for d = 0:num_slices-1
    A_transform(3, 4) = d;
    A_mod = A_single * A_transform;
    P = A_mod * double(ALL_COORD);
    ref_coord = [ref_coord; P(1:3, :)'];
  end
  
  %% do interpolation
  num_cols_ax = double(di_ax_recon.Columns);
  num_rows_ax = double(di_ax_recon.Rows);
  S_xyz = di_ax_recon.ImagePositionPatient;
  num_slices_ax = double(di_ax_recon.NumberOfFrames);
  del_r_ax = di_ax_recon.PixelSpacing(1);
  del_c_ax = di_ax_recon.PixelSpacing(1);
  del_s_ax = di_ax_recon.SliceThickness;
  
  [Xq, Yq, Zq] = ...
    meshgrid((0:num_cols_ax-1)*del_c_ax+S_xyz(1), ...
    (0:num_rows_ax-1)*del_r_ax+S_xyz(2), ...
    (0:num_slices_ax-1)*del_s_ax+S_xyz(3));
%   Fint = scatteredInterpolant(ref_coord(:,1), ref_coord(:,2), ref_coord(:,3), sa_recon(:), method);
  Fint = scatteredInterpolant(ref_coord, sa_recon(:), method);
  
end