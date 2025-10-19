function proj_data_ss = binomial_subsampling(proj_data, prob)
  
    proj_data = round(proj_data); 
    number_of_proj_bins = length(proj_data(:));
    proj_data_ss = zeros(size(proj_data));

    for i = 1:number_of_proj_bins
      if (~proj_data(i)); continue; end
        thresh = rand(proj_data(i), 1);
        proj_data_ss(i) = sum(thresh > prob);

    end
   
  end