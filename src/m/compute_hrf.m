function compute_hrf(INPUT_DIR)

listfile = dir([INPUT_DIR '/*/Detrend_4DVolume.nii.gz']);

y =[];

for i=1:length(listfile)
    i

    subject_dir = listfile(i).folder;
    outdir =  [subject_dir '/Deconv'];
        
    mkdir(outdir);

    if exist( [subject_dir '/Detrend_4DVolume.nii' ], "file") == 0
        img =  [subject_dir '/Detrend_4DVolume.nii.gz' ];
        gunzip(img)
    end
    img =  [subject_dir '/Detrend_4DVolume.nii' ];

    info = niftiinfo(img);
    img_read = load_nii(img); 
    shape_img = size(img_read.img);
    
    % znormalization
    img_tmp = (img_read.img - mean(img_read.img, [1,2,3]));
    tmp = img_tmp./std(img_read.img, 0, [1,2,3]);
    img_read.img = tmp;
    save_nii(img_read, img);


    % TR value
    pix_dims = info.PixelDimensions;
    
    % deconvolution parameters
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.images = {img}; % input image
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.generic{1}.multi_reg = {};
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.BPF{1}.bands = [0.01 0.1];
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.Despiking = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfm = 3; % type: canonical=2, gamma=3
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.TR = pix_dims(4); % input TR
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrflen = 32;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.num_basis = 3;% number of basis functions
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.mdelay = [2 12];
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.thr = 1.5;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.localK = 2;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfdeconv = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.rmoutlier = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.outdir = cellstr(outdir);% out dir 
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.deconv_save = 0;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfmat_save = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfnii_save = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.job_save = 0;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.prefix = 'Deconv_';
    
    % run job
    spm_jobman('run', matlabbatch);
    
    % reformat HRF in 4D volume
    HRF = load([outdir '/Deconv_Detrend_4DVolume_hrf.mat']);

    hrfa = HRF.hrfa';
    hrfa_size = [ shape_img(1) shape_img(2) shape_img(3) length(hrfa(1,:))];
    hrfa = reshape(hrfa, hrfa_size);
    
    niftiwrite(hrfa, [outdir '/Deconv_Detrend_4DVolume_hrf.nii']);


    % compute mean volume
    path = [ out_dir '/Deconv_Detrend_4DVolume_Olrm_Height.nii' ];
    vol = load_untouch_nii(img);
    tmp = mean(vol.img, [1, 2, 3]);

    template_img = load_untouch_nii(template);
    template_img.img = tmp;

    outfile = [ subject_dir '/mean_Detrend_4DVolume.nii'];
    save_untouch_nii(template_img,outfile)

    % compute other HRF features
    compute_params(outdir)
end