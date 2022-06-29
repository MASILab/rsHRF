DATA_DIR= '../../../rsHRF_project/ADNI_23';
list_preproc =  dir([DATA_DIR '/*/*/rsfmri/Detrend_4DVolume.nii.gz']);

nb_elt = length(list_preproc)

for i=1:nb_elt

    subject = strsplit(list_preproc(i).name, 'Detrend');
    subject_dir = list_preproc(i).folder;

    % img_Height = [list_preproc(i).folder '/Deconv_Detrend_4DVolume_Olrm_Height.nii'];
    
    % if isfile(img_Height)
    %     % disp("file exist")
    %     img = [list_preproc(i).folder '/Detrend_4DVolume.nii.gz'];
        
    % else
    % disp("file exist")
    i
    % gunzip(img)

    img = [list_preproc(i).folder '/Detrend_4DVolume.nii'];
    info = niftiinfo(img);
    img_read = niftiread(info);
    % img_unnorm = [list_preproc(i).folder '/Detrend_4DVolume_unnormalized.nii' ];
    % niftiwrite(img_read, img_unnorm, info);

    % img_tmp = (img_read - mean(img_read, [1,2,3]));
    % tmp = img_tmp./std(img_read, 0, [1,2,3]);
    % niftiwrite(tmp, img, info);


    % TR value
    dirs = string(strsplit(list_preproc(i).folder, '/'));
    folder = strjoin(dirs(1:end-1),'/');
    fname = dir(strjoin([folder 'func/*.json'], '/'));
    name =  [fname.folder '/' fname.name];
    fid = fopen(string(name));
    raw = fread(fid); 
    str = char(raw'); 
    fclose(fid); 
    val = jsondecode(str);
    val.RepetitionTime

    % to save time
    if val.RepetitionTime < 2
        
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.images = {img};
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.generic{1}.multi_reg = {};
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.BPF{1}.bands = [0.01 0.1];
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.Denoising.Despiking = 1;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfm = 2;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.TR = val.RepetitionTime;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrflen = 32;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.num_basis = 3;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.mdelay = [2 12];
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.thr = 1.5;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.localK = 2;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.HRFE.hrfdeconv = 1;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.rmoutlier = 1;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.outdir = cellstr(subject_dir);
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.deconv_save = 0;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfmat_save = 1;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.hrfnii_save = 1;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.savedata.job_save = 0;
        matlabbatch{1}.spm.tools.rsHRF.vox_rsHRF.prefix = 'Deconv_Canonical_';
        
        spm_jobman('run', matlabbatch);
        
        HRF = load([subject_dir '/Deconv_Canonical_Detrend_4DVolume_hrf.mat']);

        hrfa = HRF.hrfa';
        hrfa_size = [ 61 73 61 length(hrfa(1,:))];
        hrfa = reshape(hrfa, hrfa_size);
        
        niftiwrite(hrfa, [subject_dir '/Deconv_Canonical_Detrend_4DVolume_hrf.nii']);
    end
end