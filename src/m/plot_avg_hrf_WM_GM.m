INPUT_DIR='../../../rsHRF_project/ADNI_23';
ATLAS_DIR='../../../rsHRF_project/atlases';
param = 'hrf';

OUT_DIR = '../../../rsHRF_project/hrf_test';

%% compute HRF average population 
files =  dir([INPUT_DIR '/*/*/rsfmri/Deconv_Detrend_4DVolume_' param '.nii']);

length(files)
idx = 1112;
Param = load_nii([files(idx).folder '/' files(1).name]);
j=1;
for i=idx+1:length(files)
    i
    folder = files(i).folder;
    try
        vol = load_nii([folder '/' files(i).name]);
        sz = size(vol.img);
        if sz(4) == 41
            j = j+ 1;
            Param.img = Param.img + vol.img;
        end
    catch
        error_message = ['error in ' vol];
        disp(error_message)
    end
end
message = ['number of volumes used:' num2str(j)];
disp(message)

Param.img = Param.img ./j;
avg_hrf_file = ['../../../rsHRF_project/output/average_population/' param '0788.nii'];
save_nii(Param, avg_hrf_file)
message = ['save mean population to:' avg_hrf_file];
disp(message)

%% regrid img to match template size

template = [ATLAS_DIR '/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii'];

in_one_sub = [INPUT_DIR '/VUIISXNAT04_S16966/VUIISXNAT04_E232335/rsfmri/Deconv_Detrend_4DVolume_hrf.nii'];
out_one_sub = [OUT_DIR '/one_sub_sized.nii'];

in_avg_sub = avg_hrf_file;
out_avg_sub = [OUT_DIR '/avg_sub_sized.nii'];


system(['mrgrid ' in_one_sub ' regrid -size 193,229,193 ' out_one_sub])
system(['mrgrid ' in_avg_sub ' regrid -size 193,229,193 ' out_avg_sub])


%% write image to same voxel size

one_sub_vox = [OUT_DIR '/one_sub_voxed.nii'];
avg_sub_vox = [OUT_DIR '/avg_sub_voxed.nii'];

tmp = niftiread(out_one_sub);
niftiwrite(tmp, one_sub_vox);

tmp = niftiread(out_avg_sub);
niftiwrite(tmp, avg_sub_vox);

%% compute and plot avg in WM/GM

mask_gm =load_nii([ATLAS_DIR '/gm.nii']);
mask_wm =load_nii([ATLAS_DIR '/wm.nii']);

list_index_gm=find(mask_gm.img==1);
list_index_wm=find(mask_wm.img==1);

str = [ one_sub_vox ' ' avg_sub_vox];
files_cell = split(str);

name = ['one subject', 'mean population'];

figure()
TR = [3, 0.607];


for i=1:length(files_cell)

    file = char(files_cell(i));
    nii = load_nii(file);
    sz = size(nii.img);
    
    sizemat = sz(1)*sz(2)*sz(3);

    gm = zeros([1, sz(4)]);
    wm = zeros([1, sz(4)]);
    x = 1:sz(4);
    x = x.* TR(i);

    gm_mat = zeros([sizemat, sz(4)]);
    wm_mat = zeros([sizemat, sz(4)]);

    for j=1:sz(4)
        img = nii.img(:,:,:,j);
    
        img_masked_gm = img .* mask_gm.img;
        gm_mat(:,j) = img_masked_gm(:);
%         mean_gm = mean(img_masked_gm(list_index_gm), [1,2,3]);
%         gm(j) = mean_gm;
    
        img_masked_wm = img .* mask_wm.img;
        wm_mat(:,j) = img_masked_wm(:);
%         mean_wm = mean(img_masked_wm(list_index_wm), [1,2,3]);    
%         wm(j) = mean_wm;
 
    end

    subplot(1,2,i)
    hold on;
    plot(x, gm, 'b'); plot(x, wm, 'r');
%     title(name(i))
    legend('GM', 'WM') 
    xlabel('time (s)')
    axis([x(1), x(end), -0.5, 2.1])
end


