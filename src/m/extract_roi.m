function extract_rois(INPUT_DIR, OUT_DIR, PARAM, TEMPLATE)


list_dir = dir([INPUT_DIR '*/ants_func2stand/func2stand_' PARAM '.nii'])

labels = load_nii(TEMPLATE);

rois_id = unique(labels.img);
y = zeros(757,length(rois_id)-1);
y = zeros(5,length(rois_id)-1);

    
for j=1:length(list_dir)
    nii =load_nii([list_dir(j).folder '/func2stand_' param '.nii']);

    for roi=1:length(rois_id) -1
        list_idx = find(labels.img == roi);
            
        mask = zeros(size(labels.img));
        mask(list_idx) =1;
        
        img_masked_wm = mask .* nii.img;
        mean_wm = mean(img_masked_wm(list_idx), [1,2,3]);
    
        y(j,roi) = mean_wm;

    end
end

mat_out = [];
for j=1:length(list_dir)
    filename = list_dir(j).folder;
    cell_arr = split(filename, '/');
    exp = cell_arr{5};
    mat_out = [mat_out; string(exp)];
end

final_mat = [ mat_out, y];
filename= [ OUT_DIR '/' param '.csv'];
T = array2table(final_mat);

names = ["Experiment", string(rois_id(2:end))'];
T.Properties.VariableNames = names;
T = removevars(T, "45");
T = removevars(T, "46");

write(T,filename) 