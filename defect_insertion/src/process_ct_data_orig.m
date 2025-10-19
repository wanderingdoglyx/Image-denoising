function mu = process_ct_data_orig(fname)
  CT = dicomreadVolume(fname);
  CT = CT - 1024;
  mu = double(CT);
  mu(CT<0) = double(CT(CT<0))*1.52e-4+0.15;
  mu(CT>=0) = double(CT(CT>=0))*1.14e-4+0.15;
  mu(CT==-2000-1024) = 0;
  mu(mu<0) = 0;
  mu = flip(mu,4);
  mu = flip(mu,2);
  mu = squeeze(mu);
  mu = permute(mu, [2,1,3]);
  mu = double(mu);
end