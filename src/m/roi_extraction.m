%% Roi analysis - 50

roi_left = load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/HarvardOxford-cort-1mm-left_padded.nii.gz');
roi_right = load_nii('/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/HarvardOxford-cort-1mm-right_padded.nii.gz');

roi = unique(roi_right.img);

INPUT_DIR='../../../rsHRF_project/ADNI_23';
param = 'Height';
list_dir= dir([INPUT_DIR '/*/*/func2stand/func2stand_' param '_no_ants.nii.gz']);

list_index=[7, 17];

y = zeros(length(list_dir),2*length(list_index));


yi=1;
for i=1:length(list_index)
    roi_id = list_index(i);
    
    idx_l = find(roi_left.img == roi(roi_id));
    mask_l = zeros(size(roi_left.img));    
    mask_l(idx_l)=1;

    idx_r = find(roi_right.img == roi(roi_id));
    mask_r = zeros(size(roi_right.img));    
    mask_r(idx_r)=1;

    for j=1:length(list_dir)
        filename = [list_dir(j).folder '/' list_dir(j).name];
        tmp_img = load_nii(filename);

        img_masked_r = tmp_img.img .* mask_r;
        mean_r = mean(img_masked_r(idx_r), [1,2,3]);
        
        img_masked_l = tmp_img.img .* mask_l;
        mean_l = mean(img_masked_l(idx_l), [1,2,3]);
        
        y(j,yi) = mean_l;
        y(j,yi+1) = mean_r;
    end
    yi = yi + 2;
end

% mat_out = [];
% for j=1:length(list_dir)
%     filename = list_dir(j).folder;
%     cell_arr = split(filename, '/');
%     sub = cell_arr{9};
%     exp = cell_arr{10};

%     mat_out = [mat_out; sub, string(exp)];
% end

% final_mat = [ mat_out, y];
% filemat= ['../../../tmp_file2age_mean_' param '.mat'];
% save(filemat, 'final_mat') %save .mat
% mat_loaded = load(filemat);
% filemat= ['../../../tmp_file2age_mean_' param '.csv'];
% writetable(struct2table(mat_loaded),filemat) % save .csv



%% debug of how good is the registration
% offset = 0;
% for i=1:15
%     figure()
%     for j=1+offset: 100+offset %length(list_dir)
%         j
%         filename = [list_dir(j).folder '/' list_dir(j).name];
%         tmp = niftiread(filename);
%         subplot(10, 10,j-offset)
%         sz =  size(tmp);
%         img = reshape(tmp(85,:,:), [sz(2),sz(3)]);
%         tit = ['num' int2str(j)];
%         imshow(img)
%         title(tit)
%     end
%     offset = offset +100;
%     x0=0;
%     y0=0;
%     height= 980;
%     width=1848;
%     set(gcf, 'position', [x0,y0,width,height])
%     filefig= [ 'brain_masked_' int2str(offset +1) '_to_' int2str(offset + 100) '.png'];
%     saveas(gcf, filefig)
% endl/Documents/rsHRF_project/output/roi_analysis/meanbrain_FWHM_cleaned.csv';
% T = readtable(file);
% T = removevars(T, {'Var1','Unnamed_0'});
% T.Subject = char(T.Subject);
% T.Sex = char(T.Sex);
% T.Study = char(T.Study);
% T(1:5,:)
% 
% mdl = fitlme(T, 'White_Matter ~ Age ') 
% mdl = fitlme(T, 'White_Matter ~ Age + Weight') 
% mdl = fitlme(T, 'White_Matter ~ Age + Sex ')
% mdl = fitlme(T, 'White_Matter ~ Age + Sex + Weight')  
% % T.Properties.VariableNames{1} = 'subject';
% % T.Properties.VariableNames{2} = 'experiment';
% % T.Properties.VariableNames{3} = 'GM';
% % T.Properties.VariableNames{4} = 'WM';
% % T.Properties.VariableNames{6} = 'age';
% 
% % lme = fitlme(T,'age ~ GM + (1|subject)')
% % lme = fitlme(T,'age ~ WM + (1|subject)')
% 
% 
% % writetable(T, filecsv)
% 
% T.diff = (T.GM - T.WM);
% lme = fitlme(T,'age ~ diff + (1|subject)')
% % lme = fitlme(T,'age ~ diff + (1|experiment)')




filename ='../../../rsHRF_project/output/WM_GM_analysis/csv_cleaned/meanbrain_Height_cleaned.csv'

T = readtable(filename);


T.Manufacturer = char(T.Manufacturer);
T.Modele = char(T.Modele);
T.Sex = char(T.Sex);
 
T(1:2,:)







%% Linear Model Analysis
% filecsv = '/home/local/VANDERBILT/dolel/Documents/rsHRF_project/output/roi_analysis/csv/average_Height_ROI_aged.csv'
% T = readtable(filecsv);
% array_T = table2array(T(:,4:53));

% file='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/output/roi_analysis/meanbrain_FWHM_cleaned.csv';
% T = readtable(file);
% T = removevars(T, {'Var1','Unnamed_0'});
% T.Subject = char(T.Subject);
% T.Sex = char(T.Sex);
% T.Study = char(T.Study);
% T(1:5,:)
% 
% mdl = fitlme(T, 'White_Matter ~ Age ') 
% mdl = fitlme(T, 'White_Matter ~ Age + Weight') 
% mdl = fitlme(T, 'White_Matter ~ Age + Sex ')
% mdl = fitlme(T, 'White_Matter ~ Age + Sex + Weight')  
% % T.Properties.VariableNames{1} = 'subject';
% % T.Properties.VariableNames{2} = 'experiment';
% % T.Properties.VariableNames{3} = 'GM';
% % T.Properties.VariableNames{4} = 'WM';
% % T.Properties.VariableNames{6} = 'age';
% 
% % lme = fitlme(T,'age ~ GM + (1|subject)')
% % lme = fitlme(T,'age ~ WM + (1|subject)')
% 
% 
% % writetable(T, filecsv)
% 
% T.diff = (T.GM - T.WM);
% lme = fitlme(T,'age ~ diff + (1|subject)')
% % lme = fitlme(T,'age ~ diff + (1|experiment)')
% lme = fitlme(T,'age ~ diff')

% [p, f] = coefTest(lme) 
% % lme = fitlme(T,'final_mat_53 ~ final_mat_4');
% % [p, f] = coefTest(lme)


% T.Properties.VariableNames{1+3} = 'ROI_2_R';
% T.Properties.VariableNames{3+3} = 'ROI_6_R';
% T.Properties.VariableNames{5+3} = 'ROI_10_R';
% T.Properties.VariableNames{7+3} = 'ROI_13_R';
% T.Properties.VariableNames{9+3} = 'ROI_19_R';
% T.Properties.VariableNames{11+3} = 'ROI_20_R';
% T.Properties.VariableNames{13+3} = 'ROI_21_R';
% T.Properties.VariableNames{15+3} = 'ROI_42_R';
% T.Properties.VariableNames{17+3} = 'ROI_44_R';
% T.Properties.VariableNames{19+3} = 'ROI_45_R';
% T.Properties.VariableNames{21+3} = 'ROI_46_R';