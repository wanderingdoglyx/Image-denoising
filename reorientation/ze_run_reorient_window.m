clear,clc

%ext_arr = [30,60,90];
%sev_arr = [175,375];
%loc_arr = {'da','di','dl'};
%AC_arr = {'CTAC','NAC','ScatLAC_rec'};

%dose_level=30;
%ext_arr = [15, 30,45,60,90];
%sev_arr = {'s100','s150','s175','s250','s330','s400','s500','s750','s1000'};%total
ext_arr = [30,60];
%ext_arr = [15,30,45,60,90];%total
sev_arr = {'s375','s500'};
loc_arr = {'da','di'};
AC_arr = {'CTAC'};


% Read the file line by line into a cell array
filename = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/document/patient_list/patient_names_total.txt';
patient_list = {};
fid = fopen(filename, 'r');
if fid == -1
    error('Cannot open file: %s', filename);
end

tline = fgetl(fid);
while ischar(tline)
    patient_list{end+1} = strtrim(tline); % Remove any leading/trailing whitespace
    tline = fgetl(fid);
end
fclose(fid);

patient_list = patient_list.';

dose_levels= {'d25','d100','d33'};
%dose_levels= {'d100','d33'};

for dose_level_idx = 1:length(dose_levels)
    dose_level=dose_levels(dose_level_idx);
    dose_level=dose_level{1};
%% healthy patient


    
    for AC_method_id = 1:length(AC_arr)
        AC_method = AC_arr{AC_method_id};

        %% healthy patient
        def_name = ['hl'];
        file_path=['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_reconstruction','/',AC_method];

        %patient_list_path='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC';
        %patient_list = split(ls(patient_list_path));
        %patient_list = patient_list(1:end-1);

        ze_s1_reorient_func(patient_list,def_name, AC_method,'healthy',num2str(dose_level))

    


        %% disease patient
        for location_idx = 1:length(loc_arr)
            location_index=loc_arr{location_idx};
            %loc_prefix = loc_arr{location};
            for def_ext = ext_arr 
                for severity_idx = 1:length(sev_arr)
                    severity_index=sev_arr(severity_idx);

                    def_name = append(location_index,'21',num2str(def_ext),severity_index);
                    def_name=def_name{1};

%                    for AC_method_id = 1:length(AC_arr)
%                        AC_method = AC_arr{AC_method_id};


                    file_path=['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_reconstruction','/',AC_method];

                    %patient_list_path='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC';
                    %patient_list = split(ls(patient_list_path));
                    %patient_list = patient_list(1:end-1);


                    ze_s1_reorient_func(patient_list,def_name, AC_method, 'diseased',num2str(dose_level));

                    %end
                end
            end
        end

        for c = {'diseased','healthy'}

            %file_path=['/data01/user-storage/y.zezhang/2024_subsample_project/SA_images/',c{1},'/10'];

            file_path=['/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_SA_images/',AC_method,'/',c{1}];

            %patient_list_path='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/reconstruction/dose_level_100/CTAC';
            %patient_list = split(ls(patient_list_path));
            %patient_list = patient_list(1:end-1);

            % for AC_method_id = 1:length(AC_arr)
            %    AC_method = AC_arr{AC_method_id}; 

            for  ind_pat =1:length(patient_list)     
                ze_s2_window_process_data(c{1},AC_method,ind_pat,patient_list,num2str(dose_level));
            end
            % end

        end 

    end
end