from pyxnat import Interface
import os, shutil
import zipfile

# connection to xnat
central = Interface(server='https://xnat.vanderbilt.edu/xnat/')

# select project
project = central.select.project('ADNI_23')

out = '/home/local/VANDERBILT/dolel/Documents/rsHRF_project/ADNI_23/'

list_subjects = project.subjects().get()
for str_subject in list_subjects:
    subject = project.subject(str_subject)
    list_exp = subject.experiments().get()

    for str_exp in list_exp:
        exp = subject.experiment(str_exp)
        list_assess = exp.assessors().get()
        print(str_subject, str_exp)
        for str_assess in list_assess:
            assess = exp.assessor(str_assess)
            list_ress = assess.resources().get()
            # print(list_ress)
            for str_ress in list_ress:
                resource=assess.resource(str_ress)

                if resource.label() == 'scz_OUTPUTS':

                    location_files = str(out) + str_subject + '/' + str_exp 
                    pathfiles = '/project/ADNI_23/subjects/' + str_subject + '/experiment/' + str_exp + '/assessor/' + str_assess + '/resources/' + str_ress + '/'
                    print(location_files, pathfiles)
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

                    source = tmp_dir + '/preprocess/Masks'
                    shutil.move(source, location_files)
                    try:
                        shutil.rmtree(tmp_dir, ignore_errors=True)
                    except:
                        pass
