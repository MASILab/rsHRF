import pandas as pd
import argparse 
import json 
import os


def main(args):

    input_dir = args.input_dir
    output_file = args.out_csv
    
    list_manufacturer = []
    list_model = []
    list_subjects = []
    list_exp = []
    list_TR = []

    list_f = []
    list_sites = []

    for subject in os.listdir(input_dir):
        subject_dir = os.path.join(input_dir, subject)
        for experiment in os.listdir(subject_dir):
            exp_dir = os.path.join(subject_dir, experiment)
    
            func_dir = os.path.join(exp_dir, 'func')
    
            if os.path.isdir(func_dir):
                try:
                    for file in os.listdir(func_dir):
                        name, ext = os.path.splitext(file)
                    
                        if ext == ".json":
                            filename = os.path.join(func_dir, file)
                            with open(filename) as f :
                                data = json.load(f)
                                                                
                            list_TR.append(data["RepetitionTime"])
                            
                            try:
                                list_sites.append(data["InstitutionName"]) 
                            except:
                                list_sites.append('NaN') 

                            try:
                                list_f.append(data["ImagingFrequency"])
                            except:
                                list_f.append('NaN') 

                            try:
                                list_manufacturer.append(data["Manufacturer"]) 
                            except:
                                list_manufacturer.append('NaN') 


                            try:
                                list_model.append(data["ManufacturersModelName"])
                            except:
                                list_model.append(data["NaN"])

                            list_exp.append(experiment)
                            list_subjects.append(subject)
                except:
                    print('Fail to read json file for subject {}'.format(subject))

    df = pd.DataFrame(data={'Subject':list_subjects,
                            'TR':list_TR,
                            'Experiment':list_exp,
                            'Scanner': list_model,
                            'Manufacturer': list_manufacturer,
                            'Frequence': list_f,
                            'Site': list_sites
                            })

    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create csv file containing the TR/Model/Manufacturer values for subject of a dataset')

    parser.add_argument('--input_dir', type=str, help='input directory containing subject', required=True)
    parser.add_argument('--out_csv', type=str, help='output csv file containing the listing', default='./list_params_protocols.csv')

    args = parser.parse_args()

    main(args)
