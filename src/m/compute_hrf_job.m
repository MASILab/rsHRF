filename = '../sh/test2.csv';

fid = fopen(filename);
out=textscan(fid,' %s ');
fclose(fid);

T = cell2table(out{1,1});
rsfmri = table2array(cell2table(T.Var1(5:3:end,:)));
direct = table2array(cell2table(T.Var1(3:3:end,:)));


nb_elt = height(direct)

for i=794:nb_elt

    subject_dir = direct{i,1};
    i

    img =  [subject_dir '/' rsfmri{i,1}];
    info = niftiinfo(img);
    img_read = niftiread(info);
    
    % znormalization
    img_unnorm = [subject_dir '/rsfmri/Detrend_4DVolume_unnormalized.nii' ];
    niftiwrite(img_read, img_unnorm, info);

    img_tmp = (img_read - mean(img_read, [1,2,3]));
    tmp = img_tmp./std(img_read, 0, [1,2,3]);
    niftiwrite(tmp, img, info);


    % TR value
    fname = dir([subject_dir '/func/*.json']);
    name =  [fname.folder '/' fname.name];
    fid = fopen(string(name));
    raw = fread(fid); 
    str = char(raw'); 
    fclose(fid); 
    val = jsondecode(str);
    val.RepetitionTime

    % deconvolution parameters
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.images = {img}; % input image
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.generic{1}.multi_reg = {};
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.BPF{1}.bands = [0.01 0.1];
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.Despiking = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfm = 2; % type: canonical=2, gamma=3
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.TR = val.RepetitionTime; % input TR
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrflen = 32;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.num_basis = 3;% number of basis functions
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.mdelay = [2 12];
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.thr = 1.5;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.localK = 2;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfdeconv = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.rmoutlier = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.outdir = cellstr(subject_dir);% out dir 
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.deconv_save = 0;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfmat_save = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfnii_save = 1;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.job_save = 0;
    matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.prefix = 'Deconv';
    
    % run job
%     spm_jobman('run', matlabbatch);
    
    % reformat HRF in 4D volume
    HRF = load([subject_dir '/rsfmri/Deconv_Canonical_Detrend_4DVolume_hrf.mat']);

    hrfa = HRF.hrfa';
    hrfa_size = [ 61 73 61 length(hrfa(1,:))];
    hrfa = reshape(hrfa, hrfa_size);
    
    niftiwrite(hrfa, [subject_dir '/rsfmri/Deconv_Canonical_Detrend_4DVolume_hrf.nii']);

end