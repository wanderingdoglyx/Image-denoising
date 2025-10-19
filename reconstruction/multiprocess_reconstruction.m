% Set up parameters
dose_levels = {'d33', 'd100'};
%dose_levels = {'d100'};
extensions = [15, 30, 45, 60, 90];
severities = {'s100', 's175', 's250', 's500'};
locations = {'di', 'da'};
modes = [0, 1];

% Path setup
base_folder = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/data';
mod_proj_base_folder_def = fullfile(base_folder, 'projection_def');
mod_proj_base_folder_hl = fullfile(base_folder, 'projection_hl');
CDRP_file = '/datastore01/user-storage/y.zezhang/2025_high_dose_project/supporting_file/CDRP.par';
patient_list_folder = fullfile(base_folder, 'projection/hl/dose_level_100');

patient_list_struct = dir(patient_list_folder);
patient_list = {patient_list_struct([patient_list_struct.isdir] & ~startsWith({patient_list_struct.name}, '.')).name};

% Build all combinations of tasks
task_idx = 1;
tasks = [];

for i = 1:numel(dose_levels)
    for j = 1:numel(patient_list)
        for k = 1:numel(modes)
            if modes(k) == 0
                tasks(task_idx).dose_level = dose_levels{i};
                tasks(task_idx).patient_id = patient_list{j};
                tasks(task_idx).mode = 0;
                tasks(task_idx).ext = [];
                tasks(task_idx).sev = [];
                tasks(task_idx).loc = [];
                task_idx = task_idx + 1;
            else
                for l = 1:numel(locations)
                    for m = 1:numel(extensions)
                        for n = 1:numel(severities)
                            tasks(task_idx).dose_level = dose_levels{i};
                            tasks(task_idx).patient_id = patient_list{j};
                            tasks(task_idx).mode = 1;
                            tasks(task_idx).ext = extensions(m);
                            tasks(task_idx).sev = severities{n};
                            tasks(task_idx).loc = locations{l};
                            task_idx = task_idx + 1;
                        end
                    end
                end
            end
        end
    end
end

% Parallel pool setup
if isempty(gcp('nocreate'))
    parpool;
end

parfor t = 1:length(tasks)
    task = tasks(t);
    try
        dose_level = task.dose_level;
        patient_id = task.patient_id;
        mode = task.mode;
        ext = task.ext;
        sev = task.sev;
        loc = task.loc;

        save_folder = fullfile(base_folder, 'mod_reconstruction/CTAC', patient_id);
        if ~exist(save_folder, 'dir')
            mkdir(save_folder);
        end

        if mode == 0
            patient_folder = fullfile(mod_proj_base_folder_hl, patient_id);
            image_file_name_base = [patient_id '_' dose_level];
            image_file = fullfile(patient_folder, [image_file_name_base '.a00']);
            head_file = fullfile(patient_folder, [image_file_name_base '.h00']);
            ct_image_file = fullfile(patient_folder, [image_file_name_base '.ict']);
            ct_head_file = fullfile(patient_folder, [image_file_name_base '.hct']);
        else
            patient_folder = fullfile(mod_proj_base_folder_def, patient_id);
            ict_patient_folder = fullfile(mod_proj_base_folder_hl, patient_id);
            ext_str = num2str(ext);
            image_file_name_base = ['mod_proj_' loc '21' ext_str sev '_' patient_id '_' dose_level];
            image_file = fullfile(patient_folder, [image_file_name_base '.a00']);
            head_file = fullfile(patient_folder, [image_file_name_base '.h00']);
            ct_image_file = fullfile(ict_patient_folder, [patient_id '_' dose_level '.ict']);
            ct_head_file = fullfile(ict_patient_folder, [patient_id '_' dose_level '.hct']);
        end

        % Copy and run
        copyfile(image_file, './');
        copyfile(head_file, './');
        copyfile(ct_image_file, './');
        copyfile(ct_head_file, './');

        system(['smc2castor_new ' image_file_name_base '.h00 ' image_file_name_base]);
        system(['castor-recon_ESSE_v3 -df ' image_file_name_base '.cdh -fout ' image_file_name_base ...
                ' -oit 8:8 -it 8:6 -dim 64,64,64 -vox 6.80,6.80,6.80 -atn ' ...
                image_file_name_base '.hct -conf /home/y.zezhang/castor/config -vb 1 -opti MLEM -proj classicSiddon -cdrf ' CDRP_file]);

        % Move results
        ext_list = {'_it8.img', '_it8.hdr', '.log', '.cdh', '.cdf', '.a00', ['castor_' image_file_name_base '_it2_su6.sh']};
        for e = 1:length(ext_list)
            f = [image_file_name_base ext_list{e}];
            if exist(f, 'file')
                movefile(f, fullfile(save_folder, f));
            end
        end

        % Cleanup
        delete([image_file_name_base '.*']);
        delete([patient_id '_' dose_level '.*']);

    catch ME
        fprintf('Task failed for patient %s with mode %d: %s\n', task.patient_id, task.mode, ME.message);
    end
end