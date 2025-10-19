function matchingFiles = ze_get_the_specific_mat_file(folderPath, targetString)


files = dir(fullfile(folderPath, '*.mat'));
matchingFiles = {};

for i = 1:length(files)
    if contains(files(i).name, targetString)
        matchingFiles{end+1} = files(i).name; %#ok<AGROW>
    end
end


end
