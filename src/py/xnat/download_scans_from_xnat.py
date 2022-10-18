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
for str_subject in list_subjects:
    print(str_subject)
    subject = project.subject(str_subject)
    list_exp = subject.experiments().get()


    for str_exp in list_exp:
        exp = subject.experiment(str_exp)

        scan = exp.scan('anat')
        list_ress = scan.resources().get()

        for str_ress in list_ress:
            ress = scan.resource(str_ress)
            
            # the zip file downloaded contain the ressource id 
            location_files = str(out) + str_subject + '/' + str_exp + '/anat'
            pathfiles = '/project/ADNI_23/subjects/' + str_subject + '/experiment/' + str_exp + '/scan/anat/resources/' + str_ress + '/'

            # download files
            if os.path.exists(location_files) == False:
                os.makedirs(location_files)
            central.select(pathfiles).get(location_files)

            # unzip archive
            file_zip = location_files  + '/' + str_ress +'.zip'
            with zipfile.ZipFile(file_zip, 'r') as zip_ref:
                tmp_dir = location_files + '/tmp'
                if  os.path.exists(tmp_dir) == False:
                    os.makedirs(tmp_dir)
                zip_ref.extractall(tmp_dir)