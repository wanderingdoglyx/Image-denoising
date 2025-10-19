function aligned_sa_recon = align_sa_image_acc(Xq, Yq, Zq, sa_recon, F)

  F.Values = sa_recon(:);
  aligned_sa_recon = F(Xq, Yq, Zq);
  
end