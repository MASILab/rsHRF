% function average_population(INPUT_DIR, OUTPUT_DIR)
% average_population_hrf - compute the average of the HRF parameters accross a population

% INPUT_DIR='../../../rsHRF_project/ADNI_23';
% OUTPUT_DIR='../../../rsHRF_project/output/average/population';

% files =  dir([INPUT_DIR '/*/*/func2stand/func2stand_Height_no_ants.nii.gz']);
% hrf_files =  dir([INPUT_DIR '/*/*/rsfmri/Deconv_Detrend_4DVolume_hrf.nii']);


length(files)

idx = 1;

% Height = load_nii([files(idx).folder '/func2stand_Height_no_ants.nii.gz']);
% DipHeight = load_nii([files(idx).folder '/func2stand_DipHeight_no_ants.nii.gz']);
% TroughHeight = load_nii([files(idx).folder '/func2stand_TroughHeight.nii.gz']);

% PeakIntegral= load_nii([files(idx).folder '/func2stand_PeakIntegral_v2.nii.gz']);
% DipIntegral = load_nii([files(idx).folder '/func2stand_DipIntegral_v2.nii.gz']);
% TroughIntegral = load_nii([files(idx).folder '/func2stand_TroughIntegral.nii.gz']);

% TTP = load_nii([files(idx).folder '/func2stand_Time2peak_no_ants.nii.gz']);
% TTD = load_nii([files(idx).folder '/func2stand_Time2dip_no_ants.nii.gz']);
% TTT = load_nii([files(idx).folder '/func2stand_Time2trough.nii.gz']);

% FWHM = load_nii([files(idx).folder '/func2stand_FWHM_no_ants.nii.gz']);

j=1;

for i=idx+1:length(files)
    i;
    folder = files(i).folder;
    try
        vol = load_nii([hrf_files(i).folder '/' hrf_files(i).name]);
        sz = size(vol.img);
        if sz(4) == 11
            j = j+ 1

            % tmp = load_nii([files(i).folder '/func2stand_Height_no_ants.nii.gz']);
            % Height.img = Height.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_DipHeight_no_ants.nii.gz']);
            % DipHeight.img = DipHeight.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_TroughHeight.nii.gz']);
            % TroughHeight.img = TroughHeight.img + tmp.img;

            % tmp = load_nii([files(i).folder '/func2stand_PeakIntegral_v2.nii.gz']);
            % PeakIntegral.img= PeakIntegral.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_DipIntegral_v2.nii.gz']);
            % DipIntegral.img = DipIntegral.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_TroughIntegral.nii.gz']);
            % TroughIntegral.img = TroughIntegral.img + tmp.img;

            % tmp = load_nii([files(i).folder '/func2stand_Time2peak_no_ants.nii.gz']);
            % TTP.img = TTP.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_Time2dip_no_ants.nii.gz']);
            % TTD.img = TTD.img + tmp.img;
            
            % tmp = load_nii([files(i).folder '/func2stand_Time2trough.nii.gz']);
            % TTT.img = TTT.img + tmp.img;

            % tmp = load_nii([files(i).folder '/func2stand_FWHM_no_ants.nii.gz']);
            % FWHM.img = FWHM.img + tmp.img;

        end
    catch
    end
end
j

% Height.img = Height.img ./j;
% DipHeight.img = DipHeight.img ./j;
% TroughHeight.img = TroughHeight.img ./j;
% PeakIntegral.img = PeakIntegral.img ./j;
% DipIntegral.img = DipIntegral.img ./j;
% TroughIntegral.img = TroughIntegral.img ./j;
% TTP.img = TTP.img ./j;
% TTD.img = TTD.img ./j;
% TTT.img = TTT.img ./j;
% FWHM.img = FWHM.img ./j;

% param = '/HRF_41/'
% save_nii(Height, [ OUTPUT_DIR param 'Height.nii'])
% save_nii(DipHeight, [ OUTPUT_DIR param 'DipHeight.nii'])
% save_nii(TroughHeight, [ OUTPUT_DIR param 'TroughHeight.nii'])

% save_nii(PeakIntegral, [ OUTPUT_DIR param 'PeakIntegral.nii'])
% save_nii(DipIntegral, [ OUTPUT_DIR param 'DipIntegral.nii'])
% save_nii(TroughIntegral, [ OUTPUT_DIR param 'TroughIntegral.nii'])

% save_nii(TTP, [ OUTPUT_DIR param 'TTP.nii'])
% save_nii(TTD, [ OUTPUT_DIR param 'TTD.nii'])
% save_nii(TTP, [ OUTPUT_DIR param 'TTP.nii'])

% save_nii(FWHM, [ OUTPUT_DIR param 'FWHM.nii'])    
% % save_nii(nii,[folder 'TroughIntegral.nii'])