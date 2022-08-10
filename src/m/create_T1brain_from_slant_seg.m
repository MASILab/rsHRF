list_dir = dir('/nfs2/rsHRF/BLSA')
original_path = '/nfs2/harmonization/BLSA';
new_path = '/nfs2/rsHRF/BLSA';

cpt=0;
for i=1:length(list_dir)

    
    path_seg = [ original_path '/' list_dir(i).name '*/ASSESSORS/'];
    
    list_sub_dir = dir(path_seg);
    for j=1:length(list_sub_dir)
        if contains(list_sub_dir(j).name, 'slant')
            path_file = [ list_sub_dir(j).folder '/' list_sub_dir(j).name '/SEG/T1_seg.nii.gz'];
            seg = load_untouch_nii(path_file);
            
            
            
            path_T1 = [ new_path '/' list_dir(i).name '/anat/T1.nii.gz'];
            outfile = [ new_path '/' list_dir(i).name '/anat/T1_brain.nii.gz'];
            if exist(outfile, 'file') == 0
                try
                    t1 = load_untouch_nii(path_T1);
                    t1.img = double(t1.img);
            
                    BW = imbinarize(seg.img,0.4);
                    t1.img = BW .* t1.img;
                    save_untouch_nii(t1,outfile)
                    cpt = i+1;
                catch
                    i
                end
                     
            end
        end
    end
end
cpt