function compute_wm_gm_values(INPUT_DIR, OUT_DIR, PARAM, PATH_WM, PATH_GM)
% params = ["Height", "DipHeight", "TroughHeight", "PeakIntegral", "DipIntegral","TroughIntegral", "Time2peak", "Time2dip", "Time2trough",  "FWHM"];

list_dir= dir([INPUT_DIR '*/func2stand/func2stand_' PARAM '.nii.gz']);

mask_gm =load_nii(PATH_GM);
mask_wm =load_nii(PATH_WM);

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
    exp = cell_arr{5};
    mat_out = [mat_out; string(exp)];
end

final_mat = [ mat_out, y];
filename= [ OUTDIR '/' PARAM '.csv'];
T = array2table(final_mat);

names = ["Experiment", "GM", "WM"];
T.Properties.VariableNames = names;

write(T,filename) 
