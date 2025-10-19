clc;clear all; close all;


defect_type_arr = {'Ant', 'Inf', 'Lat', 'Sep', 'TAnt', 'TInf', 'AntLat', 'InfLat',};
defect_extent_d_arr = [15, 30, 45, 60, 90]; 
defect_extent_d_arr_baseline = [120, 150, 170];

pat_id = '86930108';
load(['data/def_segments/' pat_id '/_SA_seg_.mat']);
imshow3D(lv_mask);

figure;
for ind_loc = 1:length(defect_type_arr)
  for ind_ext = 1:length(defect_extent_d_arr)
    def_name = [defect_type_arr{ind_loc} 'Z21D' num2str(defect_extent_d_arr(ind_ext))];
    load(['data/def_segments/' pat_id '/_SA_def_' def_name '_.mat']);
    
    imshow3D(def_mask);
    title(def_name) 
    waitforbuttonpress;
  end
end