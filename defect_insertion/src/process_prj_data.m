function prj = process_prj_data(pat_data_dir, prj_folder, prob)  
  fname = [pat_data_dir, filesep, prj_folder, filesep, '*.dcm'];
  A = dir(fname);
  prj = dicomread([A.folder, filesep, A.name]);
  prj = squeeze(prj);
  prj = binomial_subsampling(prj, prob);
  prj = permute(prj, [2,1,3]);
  prj = double(prj);
end