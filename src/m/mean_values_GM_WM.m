INPUT_DIR='../../../rsHRF_project/ADNI_23';
param = 'Time2peak';
% list_dir= dir([INPUT_DIR '/*/*/func2stand/func2stand_' param '.nii.gz']);
list_dir= dir([INPUT_DIR '/*/*/rsfmri/Deconv_Detrend_4DVolume_' param '.nii']);

%% Roi analysis on GM/WM

% mask_gm =load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/mni-icbm152-nlin-asym-gm-mask.nii');
% mask_wm =load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/mni-icbm152-nlin-asym-wm-mask.nii');

mask_gm =load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/gm.nii');
mask_wm =load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/wm.nii');

list_index_gm=find(mask_gm.img==1);
list_index_wm=find(mask_wm.img==1);

y = zeros(length(list_dir),2);


for j=1:length(list_dir)

    filename = [list_dir(j).folder '/' list_dir(j).name];

    tmp_img = load_nii(filename);

    img_masked_gm = tmp_img.img .* mask_gm.img;
    mean_gm = mean(img_masked_gm(list_index_gm), [1,2,3]);

    img_masked_wm = tmp_img.img .* mask_wm.img;
    mean_wm = mean(img_masked_wm(list_index_wm), [1,2,3]);

    mean_value = [mean_gm, mean_wm];
    y(j,:) = mean_value;
end







mat_out = [];
for j=1:length(list_dir)
    filename = list_dir(j).folder;
    cell_arr = split(filename, '/');
    sub = cell_arr{9};
    exp = cell_arr{10};

    mat_out = [mat_out; sub, string(exp)];
end

final_mat = [ mat_out, y];
filename= ['../../../rsHRF_project/output/WM_GM_analysis/csv_val_extracted/meanbrain_' param 'no_registration.csv'];
T = array2table(final_mat);
T.Properties.VariableNames{1} = 'Subject';
T.Properties.VariableNames{2} = 'Experiment';
T.Properties.VariableNames{3} = 'GM';
T.Properties.VariableNames{4} = 'WM';

write(T,filename) 