function save_aligned_seg_def_in_dicom(...
            di_ax, series_desc, series_desc_ax_recon, ...
            fdir, series_trail_id, S, ...
            mask)
    
    mask = mask > 0;
    di_ax.SeriesDescription = strip(series_desc, '_');  
    % change series
    sc_factor = 100;
    di_ax.SeriesInstanceUID = [di_ax.SeriesInstanceUID '.' num2str(series_trail_id)];
    di_ax.SeriesNumber = di_ax.SeriesNumber + series_trail_id;
    di_ax.RealWorldValueMappingSequence.Item_1.RealWorldValueSlope = 1/sc_factor;
    
    Nx = size(mask,1); Ny = size(mask,2); Nz = size(mask,3);
    mask = reshape(mask, [Nx, Ny, 1, Nz]);
    mask = uint16(mask * sc_factor);
  
    mod_str = strrep(S, series_desc_ax_recon, series_desc);
    new_fdir = [fdir, mod_str];
    if ~isdir(new_fdir); mkdir(new_fdir); end
  
    fname = [new_fdir filesep 'mask.dcm'];
    IOD = 'Secondary Capture Image Storage';
    dicomwrite(mask, fname, di_ax, 'CreateMode', 'Copy');

end