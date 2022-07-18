%  function compute_params_hrf(INPUT_DIR)
% compute_params_HRF - compute the last parameters of the HRF: Time to Dip, Dip Height, Dip Integral and Peak Integral.

% csv containing data path
filename = '../sh/test2.csv';

fid = fopen(filename);
out=textscan(fid,' %s ');
fclose(fid);

T = cell2table(out{1,1});
direct = table2array(cell2table(T.Var1(3:3:end,:)));


nb_elt = height(direct);


for ii = 1:nb_elt
    ii
    folder = [direct{i,1} '/rsfmri' ];
    
    HRF = load([folder 'hrf.mat']);
    nii = load_nii([folder 'Olrm_FWHM.nii']);
    FWHM = nii.img;

    sz = size(FWHM);
    hrf = zeros([size(FWHM) size(HRF.hrfa,1)]);
    
    Time2dip_1d = zeros([size(HRF.hrfa,2) 1]);
    DipHeight_1d = zeros([size(HRF.hrfa,2) 1]);
    DipIntegral_1d = zeros([size(HRF.hrfa,2) 1]);

    PeakIntegral_1d = zeros([size(HRF.hrfa,2) 1]);

    Time2trough_1d  = zeros([size(HRF.hrfa,2) 1]);
    TroughHeight_1d  = zeros([size(HRF.hrfa,2) 1]);
    TroughIntegral_1d  = zeros([size(HRF.hrfa,2) 1]);
    
    time_axis= HRF.para.dt*[1:size(HRF.bf,1)];
    % for each hrf, get time to dip and dip magnitude
    % Area over negative dip. Area under positive peak.
    % size(HRF.hrfa,1)
    for i=1:size(HRF.hrfa,2)
        
        tmp_hrf = HRF.hrfa(:,i);
        tmp_d = HRF.hrfa(:,i);
        tmp_t = HRF.hrfa(:,i);
        tmp_int = HRF.hrfa(:,i);
        
        % long TR = short HRF != values of Dip, Peak, Trough
        if size(tmp_d) <=25
            tmp_d = tmp_d(1:3);
            tmp_t = tmp_t(3:end);
            tmp_int(1:5)=1;     
            
        % short TR = long HRF
        else 
            tmp_d=tmp_d(1:10);
            tmp_t=tmp_t(12:end);
            tmp_int(1:13)=1;

        end

        min_indx = find(tmp_d==min(tmp_d),1);
        min_indx_t = find(tmp_t==min(tmp_t),1);

        Time2dip_1d(i) = time_axis(min_indx);
        DipHeight_1d(i) = tmp_d(min_indx);

        Time2trough_1d(i) = time_axis(min_indx_t);
        TroughHeight_1d(i) = tmp_t(min_indx_t);


        % find first negative after index=10,take trapezoid rule repeatedly from that 0 to beginning, save trap numbers, sum positives and sum negatives
        
        l = find(tmp_int < 0, 1); % from this index to 1 make trap rules
        
        trap=[];
        for kk=2:l-1
            trapezoid = ((time_axis(kk)-time_axis(kk-1))/2) * (tmp_hrf(kk)+tmp_hrf(kk-1));
            trap = [trap trapezoid];
        end
        DipIntegral_1d(i)=sum(trap(trap<0));
        PeakIntegral_1d(i)=sum(trap(trap>0));
        
        trap=[];
        for kk=l:size(tmp_int)
            trapezoid = ((time_axis(kk)-time_axis(kk-1))/2) * (tmp_hrf(kk)+tmp_hrf(kk-1));
            trap = [trap trapezoid];
        end
        TroughIntegral_1d(i)=sum(trap(trap<0));
    end
    
    Time2dip = zeros([size(FWHM)]);
    DipHeight = zeros([size(FWHM)]);
    DipIntegral = zeros([size(FWHM)]);
    PeakIntegral = zeros([size(FWHM)]);


    Time2trough= zeros([size(FWHM)]);
    TroughHeight = zeros([size(FWHM)]);
    TroughIntegral = zeros([size(FWHM)]);    


    Time2dip(HRF.smask_ind) = Time2dip_1d;
    DipHeight(HRF.smask_ind) = DipHeight_1d;
    DipIntegral(HRF.smask_ind) = DipIntegral_1d;
    PeakIntegral(HRF.smask_ind) = PeakIntegral_1d;

    Time2trough(HRF.smask_ind) = Time2trough_1d;
    TroughHeight(HRF.smask_ind) = TroughHeight_1d;
    TroughIntegral(HRF.smask_ind) = TroughIntegral_1d;
    
    nii.hdr = nii.original.hdr;
    nii.img = Time2dip;
    save_nii(nii,[folder 'Time2dip.nii'])
    nii.img = DipHeight;
    save_nii(nii,[folder 'DipHeight.nii'])
    nii.img = DipIntegral;
    save_nii(nii,[folder 'DipIntegral.nii'])
    nii.img = PeakIntegral;
    save_nii(nii,[folder 'PeakIntegral.nii'])
    nii.img = Time2trough;
    save_nii(nii,[folder 'Time2trough.nii'])
    nii.img = TroughHeight;
    save_nii(nii,[folder 'TroughHeight.nii'])
    nii.img = TroughIntegral;
    save_nii(nii,[folder 'TroughIntegral.nii'])

end