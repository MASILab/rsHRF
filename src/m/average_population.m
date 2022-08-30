% function average_population(INPUT_DIR, OUTPUT_DIR)
% average_population_hrf - compute the average of the HRF parameters accross a population
% files =  dir([INPUT_DIR '/*/ants_func2stand/func2stand_Olrm_Height.nii'])


length(files)

idx = 1;

Height = load_nii([files(idx).folder '/func2stand_Olrm_Height.nii']);
DipHeight = load_nii([files(idx).folder '/func2stand_DipHeight.nii']);
TroughHeight = load_nii([files(idx).folder '/func2stand_TroughHeight.nii']);

PeakIntegral= load_nii([files(idx).folder '/func2stand_PeakIntegral.nii']);
DipIntegral = load_nii([files(idx).folder '/func2stand_DipIntegral.nii']);
TroughIntegral = load_nii([files(idx).folder '/func2stand_TroughIntegral.nii']);

TTP = load_nii([files(idx).folder '/func2stand_Olrm_Time2peak.nii']);
TTD = load_nii([files(idx).folder '/func2stand_Time2dip.nii']);
TTT = load_nii([files(idx).folder '/func2stand_Time2trough.nii']);

FWHM = load_nii([files(idx).folder '/func2stand_Olrm_FWHM.nii']);

j=1;

for i=idx+1:length(files)
    i;
    folder = files(i).folder;
    try
        % vol = load_nii([hrf_files(i).folder '/' hrf_files(i).name]);
        % sz = size(vol.img);
        % if sz(4) == 17
        j = j+ 1
    
        tmp = load_nii([files(i).folder '/func2stand_Olrm_Height.nii']);
        Height.img = Height.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_DipHeight.nii']);
        DipHeight.img = DipHeight.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_TroughHeight.nii']);
        TroughHeight.img = TroughHeight.img + tmp.img;

        tmp = load_nii([files(i).folder '/func2stand_PeakIntegral.nii']);
        PeakIntegral.img= PeakIntegral.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_DipIntegral.nii']);
        DipIntegral.img = DipIntegral.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_TroughIntegral.nii']);
        TroughIntegral.img = TroughIntegral.img + tmp.img;

        tmp = load_nii([files(i).folder '/func2stand_Olrm_Time2peak.nii']);
        TTP.img = TTP.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_Time2dip.nii']);
        TTD.img = TTD.img + tmp.img;
        
        tmp = load_nii([files(i).folder '/func2stand_Time2trough.nii']);
        TTT.img = TTT.img + tmp.img;

        tmp = load_nii([files(i).folder '/func2stand_Olrm_FWHM.nii']);
        FWHM.img = FWHM.img + tmp.img;
        % end
    catch
    end
end
j

Height.img = Height.img ./j;
DipHeight.img = DipHeight.img ./j;
TroughHeight.img = TroughHeight.img ./j;
PeakIntegral.img = PeakIntegral.img ./j;
DipIntegral.img = DipIntegral.img ./j;
TroughIntegral.img = TroughIntegral.img ./j;
TTP.img = TTP.img ./j;
TTD.img = TTD.img ./j;
TTT.img = TTT.img ./j;
FWHM.img = FWHM.img ./j;

param = ''
save_nii(Height, [ OUTPUT_DIR param 'Height.nii'])
save_nii(DipHeight, [ OUTPUT_DIR param 'DipHeight.nii'])
save_nii(TroughHeight, [ OUTPUT_DIR param 'TroughHeight.nii'])

save_nii(PeakIntegral, [ OUTPUT_DIR param 'PeakIntegral.nii'])
save_nii(DipIntegral, [ OUTPUT_DIR param 'DipIntegral.nii'])
save_nii(TroughIntegral, [ OUTPUT_DIR param 'TroughIntegral.nii'])

save_nii(TTP, [ OUTPUT_DIR param 'TTP.nii'])
save_nii(TTD, [ OUTPUT_DIR param 'TTD.nii'])
save_nii(TTT, [ OUTPUT_DIR param 'TTT.nii'])

save_nii(FWHM, [ OUTPUT_DIR param 'FWHM.nii'])    
