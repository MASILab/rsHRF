from pyxnat import Interface
import os, shutil
import zipfile

# connection to xnat
central = Interface(server='https://xnat.vanderbilt.edu/xnat/')

# select project
project = central.select.project('ADNI_23')

out = '/home/local/VANDERBILT/mazumdt/Documents/rsHRF_project/ADNI_23/'

#  loop on subject, experiment,and assessor
list_subjects = project.subjects().get()

list_files = []
for str_subject in list_subjects:
    subject = project.subject(str_subject)
    list_exp = subject.experiments().get()

    for str_exp in list_exp:
        exp = subject.experiment(str_exp)
        list_assess = exp.assessors().get()

        for str_assess in list_assess:
            assess = exp.assessor(str_assess)
            list_ress = assess.resources().get()

            for str_ress in list_ress:
                ress = assess.resource(str_assess)
            
                # the zip file downloaded contain the ressource id 
                location_files = str(out) + str_subject + '/' + str_exp + '/rsfmri'
                pathfiles = '/project/ADNI_23/subjects/' + str_subject + '/experiment/' + str_exp + '/assessor/' + str_assess + '/resources/' + str_ress + '/'

                # download files
                if os.path.exists(location_files) == False:
                    print(str_subject)
                    os.makedirs(location_files)
                    # niifile = location_files + 'Detrend_4DVolume.nii'
                    # list_files.append(niifile)
                    central.select(pathfiles).get(location_files)

                    # unzip archive
                    file_zip = location_files  + '/' + str_ress +'.zip'
                    with zipfile.ZipFile(file_zip, 'r') as zip_ref:
                        tmp_dir = location_files + '/tmp'
                        if  os.path.exists(tmp_dir) == False:
                            os.makedirs(tmp_dir)
                        zip_ref.extractall(tmp_dir)

                    # to keep only the wanted file
                    
                    location_detrend = tmp_dir + '/result1_corrmatrix/FunImgARCFWD/1/Detrend_4DVolume.nii.gz'
                    if os.path.exists(location_detrend):
                        wanted_location_detrend = location_files + '/Detrend_4DVolume.nii.gz'
                        os.rename(location_detrend, wanted_location_detrend)
        
# with open('../../rsHRF_project/list_rsfmri_volumes_missing.txt', 'w') as f:
#     for item in list_TR:
#         f.write("%s\n" % item)