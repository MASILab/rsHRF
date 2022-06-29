INPUT_DIR='../../../rsHRF_project/ADNI_23';
param = 'TroughHeight';
% files =  dir([INPUT_DIR '/*/*/func2standard/func2stand_' param '.nii.gz']);
files =  dir([INPUT_DIR '/*/*/func2stand/func2stand' param '.nii'])

y = zeros(length(files),2);

for i=2:length(files)
    i;
    folder = files(i).folder;
    try
        v1 = load_nii([folder '/func2stand_DipIntegral_v2.nii.gz']);
        v2 = load_nii([folder '/func2stand_DipIntegral_no_ants.nii.gz']);
        tmp = v1.img(:) - v2.img(:);
        mean_value = [mean(tmp), std(tmp)];
        y(i,:) = mean_value;
    catch
        i
    end
end


mat_out = [];
for j=1:length(files)
    filename = files(j).folder;
    cell_arr = split(filename, '/');
    sub = cell_arr{9};
    exp = cell_arr{10};

    mat_out = [mat_out; sub, string(exp)];
end

final_mat = [ mat_out, y];
T = array2table(final_mat);
T.Properties.VariableNames{1} = 'Subject';
T.Properties.VariableNames{2} = 'Experiment';
T.Properties.VariableNames{3} = 'Mean';
T.Properties.VariableNames{4} = 'Std';


%files QA

% l = dir('*/*/func2stand/func2stand_TroughHeight.nii.gz')
% tmptable = struct2table(l);
% test_table = tmptable(1:8:end,:);
% table = [test_table.folder test_table.name];