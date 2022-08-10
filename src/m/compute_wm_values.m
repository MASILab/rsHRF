INPUT_DIR='/nfs2/rsHRF/BLSA/';

param = 'Height';
blsa= dir([INPUT_DIR '*/func2stand/func2stand_' param '.nii.gz']);


% param = 'Height';
INPUT_DIR='/nfs2/rsHRF/ADNI/';
adni= dir([INPUT_DIR '*/*/func2stand/func2stand_' param '.nii.gz']);

list_dir = [blsa; adni];

% params = ["Height", "DipHeight", "TroughHeight", "PeakIntegral", "DipIntegral","TroughIntegral", "Time2peak", "Time2dip", "Time2trough",  "FWHM"];

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
for j=1:length(blsa)
    filename = blsa(j).folder;
    cell_arr = split(filename, '/');
    exp = cell_arr{5};
    mat_out = [mat_out; string(exp)];
end

for j=1:length(adni)
    filename = adni(j).folder;
    cell_arr = split(filename, '/');
    exp = cell_arr{6};
    mat_out = [mat_out; string(exp)];
end

final_mat = [ mat_out, y];
filename= ['../../../rsHRF_project/output/WM_GM_analysis/csv_val_extracted/all_dataset/' param '.csv'];
T = array2table(final_mat);

names = ["Experiment", "GM", "WM"];
T.Properties.VariableNames = names;

write(T,filename) 

% 
% list_index= find(labels.img == 50);
% tmp = zeros(size(labels.img));
% tmp(list_index)=1;
% imshow(tmp(:,:,87))