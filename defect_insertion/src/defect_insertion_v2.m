function defect_insertion_v2(fdir, pat_id, ...
                    sev, hl_obj_prefix, def_obj_prefix, def_obj_prefix_half, ct_prefix, ...
                    lv_template, def_template, sc_obj, ...
                    save_folder, recon_cast ...
)
% change:
% fixed the dimension in saving defect mask
% looked at different lv_template (partila, full seg)
% only save mask, dont depend on severity

pat_folder = [save_folder pat_id '/'];


%% Load recon castor
% S = get_dir(fdir, 'ReconPrimOrigCastor', pat_id);
% cur_dir = [fdir, S, '/castor_recon.dcm'];
% di = dicominfo(cur_dir);
% sc_factor_castor2 = di.RealWorldValueMappingSequence.Item_1.RealWorldValueSlope;
% rec_base = double(squeeze(dicomread(cur_dir)))*sc_factor_castor2;
% % sum(rec_base(:))

%% read mod recon
% fname = castor_recon_fname;
% recon_cast = my_fread(fname, inf, 'float32');
% recon_cast = reshape(recon_cast, [64,64,64]);
% rec_base = process_castor_recon(recon_cast);
rec_base = recon_cast;

%% Load tx LV seg
tx_lv_seg = lv_template>0;

%% Load tx def
tx_def = def_template>0;

%%
% figure;imshow3D(rec_base); colormap gray;
% figure;imshow3D(tx_lv_seg); colormap gray;
% figure;imshow3D(tx_def); colormap gray;

%%
mean_lv_uptake = sum(rec_base.*tx_lv_seg, 'all') / sum(tx_lv_seg(:));
def_recon = rec_base - mean_lv_uptake * sev * tx_def;
def_recon(def_recon < 0) = 0;
% figure; imshow3D(def_recon); colormap gray;
% figure; imshow3D(rec_base - def_recon); colormap gray;
% fprintf("Def: %s || Mean LV uptake: %.4f\n", def_obj_prefix, mean_lv_uptake);

%% save defect object
def_recon = permute(def_recon, [2, 1, 3]);
def_recon = round(def_recon * sc_obj);

tx_def = permute(tx_def, [2, 1, 3]);
tx_def = round(tx_def);
% hl_recon = rec_base;
% hl_recon = permute(hl_recon, [2,1,3]);
% hl_recon = round(hl_recon * sc_obj);
% 
% my_fwrite([pat_folder hl_obj_prefix, '_obj_act_av.bin'], hl_recon, 'float32')
%saving this def_obj just for redundancy, sev can be added post-mc
my_fwrite([pat_folder def_obj_prefix, '_obj_act_av.bin'], def_recon, 'float32') 
if sev == 0.1 % save mask only for first severity
  my_fwrite([pat_folder def_obj_prefix_half, '_act_av.bin'], tx_def, 'float32')
end

%% save ct map
% S = get_dir(fdir, 'RegCTLow', pat_id);
% S_dcm = dir(fullfile([fdir,S], '*.dcm'));
% CT = dicomreadVolume([fdir,S]);
% CT = process_ct_data(CT);
% pixel_size = 0.68;
% CT = CT * pixel_size;
% % figure;imshow3D(CT);colormap gray;
% 
% my_fwrite([pat_folder ct_prefix '_atn_av.bin'], CT, 'float32')

if strcmp(def_obj_prefix, 'dA2130s100')
  fprintf('pat: %s || hl sum: %.4f || def sum: %.4f \n', ...
            pat_id, sum(rec_base(:)), sum(def_recon(:))/sc_obj);
end

end