files =  dir('../../rsHRF_project/ADNI_23/*/*/*/Deconv_Detrend_4DVolume_hrf.mat');

mean_params = zeros(length(files)+1,8);
mean_params(1,:) = ["TR", "FWHM", "Height", "DipHeight", "Time2peak", "Time2dip", "PeakIntegral", "DipIntegral"];

for i=2:length(files)+1
    i
    
    %664
    folder = files(i).folder;
    mat = load([folder '/' files(i).name]);
    
    FWHM = niftiread([folder '/Deconv_Detrend_4DVolume_Olrm_FWHM.nii']);

    TTD =  niftiread([folder '/Deconv_Detrend_4DVolume_Time2dip.nii']);
    TTP =  niftiread([folder '/Deconv_Detrend_4DVolume_Olrm_Time2peak.nii']);
    
    PeakIntegral = niftiread([folder '/Deconv_Detrend_4DVolume_PeakIntegral.nii']);
    DipIntegral = niftiread([folder '/Deconv_Detrend_4DVolume_DipIntegral.nii']);

    Height = niftiread([folder '/Deconv_Detrend_4DVolume_Olrm_Height.nii']);
    DipHeight = niftiread([folder '/Deconv_Detrend_4DVolume_DipHeight.nii']);
    
    mean_params(i,1) = mat.para.TR;
    mean_params(i,2) = mean(FWHM, [1 2 3]);
    
    mean_params(i,3) = mean(Height, [1 2 3]);
    mean_params(i,4) = mean(DipHeight, [1 2 3]);
    
    mean_params(i,5) = mean(TTP, [1 2 3]);
    mean_params(i,6) = mean(TTD, [1 2 3]);
    
    mean_params(i,7) = mean(PeakIntegral, [1 2 3]);
    mean_params(i,8) = mean(DipIntegral, [1 2 3]);
            
end


outliers = zeros(2,7);
outliers(1,:) = ["FWHM", "Height", "DipHeight", "Time2peak", "Time2dip", "PeakIntegral", "DipIntegral"];

for j=1:8
    cpt=0;

    m = mean(mean_params(2:end,j));
    sig = std(mean_params(2:end,j));

    BS = m + 3*sig;
    BI = m - 3*sig;

    list_outliers = find( (mean_FWHM(2:end,2) < BI) | (mean_FWHM(2:end,2) > BS));
    j
    length(list_outliers)
    outliers(2,j) = list_outliers;

end


save('../output/params_analysis.mat', 'mean_params' )
save('../output/outliers_params.mat', 'outliers' )

% niftiwrite(TTP, [OUTPUT_DIR 'TTP_undivided_length_06.nii']);
% niftiwrite(TTD, [OUTPUT_DIR 'TTD_undivided_length_06.nii']);

% niftiwrite(PeakIntegral, [OUTPUT_DIR 'PeakIntegral_undivided_length_06.nii']);
% niftiwrite(DipIntegral, [OUTPUT_DIR 'DipIntegral_undivided_length_06.nii']);

% niftiwrite(Height, [OUTPUT_DIR 'Height_undivided_length_06.nii']);
% niftiwrite(DipHeight, [OUTPUT_DIR 'DipHeight_undivided_length_06.nii']);

% niftiwrite(FWHM, [OUTPUT_DIR 'FMWH_undivided_length_06.nii']);

% TTP = TTP./j;
% TTD = TTD./j;

% PeakIntegral = PeakIntegral./j;
% DipIntegral =DipIntegral./j;

% Height = Height./j;
% DipHeight = DipHeight./j;

% FWHM = FWHM./j;
% j

% niftiwrite(TTP, [OUTPUT_DIR 'TTP_length_06.nii']);
% niftiwrite(TTD, [OUTPUT_DIR 'TTD_length_06.nii']);

% niftiwrite(PeakIntegral, [OUTPUT_DIR 'PeakIntegral_length_06.nii']);
% niftiwrite(DipIntegral, [OUTPUT_DIR 'DipIntegral_length_06.nii']);

% niftiwrite(Height, [OUTPUT_DIR 'Height_length_06.nii']);
% niftiwrite(DipHeight, [OUTPUT_DIR 'DipHeight_length_06.nii']);

% niftiwrite(FWHM, [OUTPUT_DIR 'FMWH_length_06.nii']);
