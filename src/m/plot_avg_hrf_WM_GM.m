% INPUT_DIR='../../../rsHRF_project/ADNI_23';
INPUT_DIR='/nfs2/rsHRF/BLSA';

ATLAS_DIR='../../../rsHRF_project/atlases/MNI';
param = 'hrf';

OUT_DIR = '../../../rsHRF_project/';

%% compute HRF average population 
files =  dir([INPUT_DIR '/*/Deconv/Deconv_Detrend_4DVolume_hrf.nii']);

length(files)
idx = 1;
Param = load_nii([files(idx).folder '/' files(1).name]);
j=1;
for i=idx+1:length(files)
    i
    folder = files(i).folder;
    try
        vol = load_nii([folder '/' files(i).name]);
        sz = size(vol.img);
        if sz(4) == 17
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

% Param.img = Param.img ./j;
% avg_hrf_file = ['../../../rsHRF_project/output/average_population/' param '_canonical.nii'];
% save_nii(Param, avg_hrf_file)
% message = ['save mean population to:' avg_hrf_file];
% disp(message)

% %% regrid img to match template size

template = [ATLAS_DIR '/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii'];

% in_one_sub = [INPUT_DIR '/VUIISXNAT04_S16966/VUIISXNAT04_E232335/rsfmri/Deconv_canonical_Detrend_4DVolume_hrf.nii'];
% out_one_sub = [OUT_DIR '/one_sub_sized.nii'];

in_avg_sub = avg_hrf_file;
out_avg_sub = [OUT_DIR '/avg_sub_sized_blsa.nii'];


% system(['mrgrid ' in_one_sub ' regrid -size 193,229,193 ' out_one_sub])
system(['mrgrid ' in_avg_sub ' regrid -size 193,229,193 ' out_avg_sub])


%% write image to same voxel size

% one_sub_vox = [OUT_DIR '/one_sub_voxed.nii'];
avg_sub_vox = [OUT_DIR '/avg_sub_voxed_blsa.nii'];

% tmp = niftiread(out_one_sub);
% niftiwrite(tmp, one_sub_vox);

tmp = niftiread(out_avg_sub);
niftiwrite(tmp, avg_sub_vox);

%% compute and plot avg in WM/GM
MASK_DIR='../../../rsHRF_project/atlases';
mask_gm =load_nii([MASK_DIR '/gm.nii']);
mask_wm =load_nii([MASK_DIR '/wm.nii']);

list_index_gm=find(mask_gm.img==1);
list_index_wm=find(mask_wm.img==1);


% name = ['one subject', 'mean population'];

TR = [2, 2];

% img_11_gm = '../../../rsHRF_project/avg_sub_voxed.nii';
img_53_gm = '../../../rsHRF_project/avg_sub_voxed_blsa.nii';
str = [ img_53_gm ];
files_cell = split(str);

gm = zeros([1, 18]);
wm = zeros([1, 18]); 
x =  zeros([1, 18]);

for i=1:length(files_cell)

    file = char(files_cell(i));
    nii = load_nii(file);
    sz = size(nii.img);
    
    sizemat = sz(1)*sz(2)*sz(3);


    x_tmp = 1:sz(4);
    x(i,2:sz(4)+1) = x_tmp.* TR(i);

    gm_mat = zeros([sizemat, sz(4)]);
    wm_mat = zeros([sizemat, sz(4)]);

    for j=1:sz(4)
        img = nii.img(:,:,:,j);
    
        img_masked_gm = img .* mask_gm.img;
        gm_mat(:,j) = img_masked_gm(:);
        mean_gm = mean(img_masked_gm(list_index_gm), [1,2,3]);
        gm(i,j) = mean_gm;
    
        img_masked_wm = img .* mask_wm.img;
        wm_mat(:,j) = img_masked_wm(:);
        mean_wm = mean(img_masked_wm(list_index_wm), [1,2,3]);    
        wm(i,j) = mean_wm;
 
    end
    % plot(x, gm, color(j)); plot(x, wm, color(j+1));
    %     j = j+2
end
f = figure();

hold on;
plot(x(1,:), wm(1,:),'Color', [0.8500 0.3250 0.0980], 'LineWidth', 1)
plot(x(1,:), gm(1,:), 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1) 
% plot(x(2,:), wm(2,:), 'Color', [0 0.4470 0.7410], 'LineWidth', 2)
% plot(x(2,:), wm(2,:), 'Color', [0.3010 0.7450 0.9330], 'LineWidth', 2);

[~, hobj, ~, ~] = legend('WM', 'GM', fontsize=10);
hl = findobj(hobj,'type','line');
set(hl,'LineWidth',2);

xlabel('time (s)', fontsize=15)
ylabel('Signal Amplitude', fontsize=15)
axis([x(1), x(end), -1, 2])
exportgraphics(f,'blsa.png','Resolution',600)