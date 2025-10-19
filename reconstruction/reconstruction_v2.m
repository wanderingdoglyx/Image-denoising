clear;
close all;
clc;

dose_levels={'d25','d33','d100'};

% Set paths
base_folder ='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data';

% Set paths
pro_projection_base_folder ='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl';
%save_folder = append('/data01/user-storage/y.zezhang/2024_subsample_project/mod_reconstruction/',num2str(does_level),'/CTAC');
mod_proj_base_folder_def='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_def_375';
mod_proj_base_folder_hl='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection_hl';


CDPR_file='/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file/CDRP.par';


extension = [15, 30, 45, 60, 90];
severity={'s100','s175','s250','s500'};
location={'di','da'};
mode=[0, 1];


patient_list_folder='/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/projection/hl/dose_level_100';
%brench_folder_name=append(base_folder,'/',num2str(dose_level));

% Get a list of all files and folders in this folder
filesAndFolders = dir(patient_list_folder);

% Get a logical vector that tells which is a directory
dirFlags = [filesAndFolders.isdir];

% Extract only those that are directories
subFolders = filesAndFolders(dirFlags);

% Remove '.' and '..' from the list
subFolders = subFolders(~ismember({subFolders.name}, {'.', '..'}));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read the file line by line into a cell array
%filename = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/document/patient_list/patient_names06092025.txt';
%patient_list = {};
%fid = fopen(filename, 'r');
%if fid == -1
%    error('Cannot open file: %s', filename);
%end

%tline = fgetl(fid);
%while ischar(tline)
%    patient_list{end+1} = strtrim(tline); % Remove any leading/trailing whitespace
%    tline = fgetl(fid);
%end
%fclose(fid);

%patient_list = patient_list.';
%subFolders =patient_list;

for dose_idx=1 : length(dose_levels)
    dose_level=dose_levels{dose_idx};

%   save_folder = append('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_reconstruction',dose_level,'/CTAC');
%    if ~exist(save_folder, 'dir')    
%        mkdir(save_folder);
%    end
    
    for k = 1 : length(subFolders)

        %  save_folder = append('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_reconstruction',dose_level,'/CTAC/',patient_id );
        % if ~exist(save_folder, 'dir')    
        %     mkdir(save_folder);
        %  end

        
        patient_id=subFolders(k).name;

        save_folder = append('/datastore01/user-storage/y.zezhang/2025_high_dose_project/data/mod_reconstruction','/CTAC/',patient_id );
        if ~exist(save_folder, 'dir')    
            mkdir(save_folder);
        end

        for mode_idx = 1:length(mode)
            mode_index=mode(mode_idx);

            if mode_index==0 

                patient_folder=fullfile(mod_proj_base_folder_hl,subFolders(k).name);


                image_file_name_base=append(patient_id,'_',dose_level);
                image_file_name=append(patient_id,'_',dose_level,'.a00');
                head_file_name=append(patient_id,'_',dose_level,'.h00');
                image_file= fullfile(patient_folder,image_file_name);   
                head_file= fullfile(patient_folder,head_file_name);

                CT_image_file_name=append(patient_id,'_',dose_level,'.ict');
                CT_head_file_name=append(patient_id,'_',dose_level,'.hct');
                CT_image_file=fullfile(patient_folder,CT_image_file_name); 
                CT_head_file=fullfile(patient_folder,CT_head_file_name);
                

                % Copying files
                copyfile(image_file,'./');
                copyfile(head_file,'./');
                copyfile(CT_image_file,'./');
                copyfile(CT_head_file,'./');


                system(['smc2castor_new ',head_file_name,' ',image_file_name_base]);
                %system(['castor-recon_ESSE_v3 -df ',image_file_name_base,'.cdh -fout ',image_file_name_base,' -oit 8:8  -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ',CT_head_file_name,' -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf /data01/user-storage/y.zezhang/2024_subsample_project/supporting_file_reconstruction/CDRP',num2str(dose_level),'.par']);
                system(['castor-recon_ESSE_v3 -df ',image_file_name_base,'.cdh -fout ',image_file_name_base,' -oit 8:8  -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ',CT_head_file_name,' -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf ',CDPR_file]);


                priprj_name = image_file_name_base;

                cur_folder = save_folder;
                %cur_folder=cur_folder{1};
                if ~exist(cur_folder, 'dir')
                    mkdir(cur_folder);
                end

                system(['cp ',priprj_name,'_it8.img ',cur_folder]);
                system(['cp ',priprj_name,'_it8.hdr ',cur_folder]);
                system(['cp ',priprj_name,'.log ',cur_folder]);
                system(['cp ',priprj_name,'.cdh ',cur_folder]);
                system(['cp ',priprj_name,'.cdf ',cur_folder]);
                system(['cp ',priprj_name,'.a00 ',cur_folder]);
                system(['cp castor_',priprj_name,'_it2_su6.sh ',cur_folder]);

                system(['rm ',priprj_name,'_it8.img ']);
                system(['rm ',priprj_name,'_it8.hdr ']);
                system(['rm ',priprj_name,'.log ']);
                system(['rm ',priprj_name,'.cdh ']);
                system(['rm ',priprj_name,'.cdf ']);
                %system(['rm ',priprj_name,'.a00 ']);
                system(['rm castor_',priprj_name,'_it2_su6.sh ']);



                %%%%%%%%%%%%%%%%%%%%%% remove initial files %%%%%%%%%%%%%%%%%%%%%%%%%%%%% 



                system(['rm ', image_file_name]);
                system(['rm ',head_file_name]);
                system(['rm ',CT_image_file_name]);
                system(['rm ', CT_head_file_name]);

                
                    
            elseif mode_index==1 

                patient_folder=fullfile(mod_proj_base_folder_def,subFolders(k).name);
                ict_patient_folder=fullfile(mod_proj_base_folder_hl,subFolders(k).name);
            
                for severity_idx = 1:length(severity)
                    severity_index=severity(severity_idx);
                    severity_index=severity_index{1};
                    for extension_idx = 1:length(extension)
                        extension_index=extension(extension_idx);
                        extension_index=num2str(extension_index);
                        for location_idx = 1:length(location)
                            location_index=location(location_idx);
                            location_index=location_index{1};

                            image_file_name_base=append('mod_proj_',location_index,'21',extension_index,severity_index,'_',patient_id,'_',dose_level);
                            image_file_name=append('mod_proj_',location_index,'21',extension_index,severity_index,'_',patient_id,'_',dose_level,'.a00');
                            head_file_name=append('mod_proj_',location_index,'21',extension_index,severity_index,'_',patient_id,'_',dose_level,'.h00');

                            image_file= fullfile(patient_folder,image_file_name);   
                            head_file= fullfile(patient_folder,head_file_name);
                
                            %CT_image_file_name=append(patient_id,'_ct.ict');
                            %CT_head_file_name=append(patient_id,'_ct.hct');
                            %CT_image_file=fullfile(patient_folder,CT_image_file_name); 
                            %CT_head_file=fullfile(patient_folder,CT_head_file_name);
                            
                            CT_image_file_name=append(patient_id,'_',dose_level,'.ict');
                            CT_head_file_name=append(patient_id,'_',dose_level,'.hct');
                            CT_image_file=fullfile(ict_patient_folder,CT_image_file_name); 
                            CT_head_file=fullfile(ict_patient_folder,CT_head_file_name);


                            % Copying files
                            copyfile(image_file,'./');
                            copyfile(head_file,'./');
                            copyfile(CT_image_file,'./');
                            copyfile(CT_head_file,'./');
                
                
                            %system(['smc2castor_new ',head_file_name,' ',image_file_name_base]);
                            %system(['castor-recon_ESSE_v3 -df ',image_file_name_base,'.cdh -fout ',image_file_name_base,' -oit 8:8  -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ',CT_head_file_name,' -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf /data01/user-storage/y.zezhang/2024_subsample_project/supporting_file_reconstruction/CDRP',num2str(dose_level),'.par']);
                            system(['smc2castor_new ',head_file_name,' ',image_file_name_base]);
                            %system(['castor-recon_ESSE_v3 -df ',image_file_name_base,'.cdh -fout ',image_file_name_base,' -oit 8:8  -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ',CT_head_file_name,' -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf /data01/user-storage/y.zezhang/2024_subsample_project/supporting_file_reconstruction/CDRP',num2str(dose_level),'.par']);
                            system(['castor-recon_ESSE_v3 -df ',image_file_name_base,'.cdh -fout ',image_file_name_base,' -oit 8:8  -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ',CT_head_file_name,' -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf ',CDPR_file]);
            
                
                
                            priprj_name = image_file_name_base;
                
                            cur_folder = fullfile(save_folder);
                            %cur_folder=cur_folder{1};
                            if ~exist(cur_folder, 'dir')
                                mkdir(cur_folder);
                            end
                
                            system(['cp ',priprj_name,'_it8.img ',cur_folder]);
                            system(['cp ',priprj_name,'_it8.hdr ',cur_folder]);
                            system(['cp ',priprj_name,'.log ',cur_folder]);
                            system(['cp ',priprj_name,'.cdh ',cur_folder]);
                            system(['cp ',priprj_name,'.cdf ',cur_folder]);
                            system(['cp ',priprj_name,'.a00 ',cur_folder]);
                            system(['cp castor_',priprj_name,'_it2_su6.sh ',cur_folder]);
                
                            system(['rm ',priprj_name,'_it8.img ']);
                            system(['rm ',priprj_name,'_it8.hdr ']);
                            system(['rm ',priprj_name,'.log ']);
                            system(['rm ',priprj_name,'.cdh ']);
                            system(['rm ',priprj_name,'.cdf ']);
                            %system(['rm ',priprj_name,'.a00 ']);
                            system(['rm castor_',priprj_name,'_it2_su6.sh ']);
                
                
                
                            %%%%%%%%%%%%%%%%%%%%%% remove initial files %%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

                
                            system(['rm ', image_file_name]);
                            system(['rm ',head_file_name]);
                            system(['rm ',CT_image_file_name]);
                            system(['rm ', CT_head_file_name]);
                
                        
                            
                        end
                    end
                end    
            end

        end
    end
    
end