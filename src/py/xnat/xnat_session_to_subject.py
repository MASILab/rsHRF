import pandas as pd
import os
import argparse


def main(args):
    input_dir = args.input_dir
    df = pd.read_csv(args.xnat_csv)

    list_age = []
    list_exp = []
    list_subject = []
    list_ResearchGroup = []
    list_Sex = []
    list_Weight = []
    list_Phase = []

    for subject in sorted(os.listdir(input_dir)):
        subject_dir = os.path.join(input_dir, subject)
        for experiment in sorted(os.listdir(subject_dir)):
            exp_dir = os.path.join(subject_dir, experiment)
            try:
                scz_fold = os.path.join(exp_dir, 'Scz_OUTPUTS')
                for filename in os.listdir(scz_fold):
                    name, ext = os.path.splitext(filename)

                    if ext == '.txt':
                        list_char = filename.split('-')

                        visit = list_char[4].split('_Visit')[1]
                        name = list_char[4].split('_Visit')[0]
                        sid = name.split('S_')[1]

                        df_sub_exp = df.loc[ (df['sID'] == int(sid)) & (df['vcode'] == float(visit))]
                        list_subject.append(subject)
                        list_exp.append(experiment)
                        
                        try:
                            age = df_sub_exp['Age']
                            tmp = age.to_numpy()
                            list_age.append(tmp[0])
                            
                            Phase = df_sub_exp['Phase']
                            tmp = Phase.to_numpy()
                            list_Phase.append(tmp[0])

                            Weight = df_sub_exp['Weight']
                            tmp = Weight.to_numpy()
                            list_Weight.append(tmp[0])

                            Sex = df_sub_exp['Sex']
                            tmp = Sex.to_numpy()
                            list_Sex.append(tmp[0])

                            ResearchGroup = df_sub_exp['ResearchGroup']
                            tmp = ResearchGroup.to_numpy()
                            list_ResearchGroup.append(tmp[0])   

                        except:
                            print('Fail to find information for subject {}. Adding NaN'.format(subject))
                            list_age.append('NaN')
                            list_Phase.append('Nan')
                            list_Sex.append('Nan')
                            list_Weight.append('Nan')
                            list_ResearchGroup.append('Nan')
            except:
                pass

    df_out = pd.DataFrame(data={'subject':list_subject,
                                'experiment': list_exp,
                                'age': list_age,
                                'Study': list_Phase,
                                'Weight': list_Weight,
                                'Sex': list_Sex,
                                'ResearchGroup': list_ResearchGroup
                                })

    df_out.to_csv(args.outfile, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='translate csv file from xnat subject format (x-##_S##-Visit##) to dataset directory (VUIISXNAT_S##/VUIISXNAT_E##)')

    parser.add_argument('--input_dir', type=str, help='input directory containing data downloaded from xnat', required=True)
    parser.add_argument('--xnat_csv', type=str, help=' xnat csv file containing infos on subject', required=True)
    parser.add_argument('--outfile', type=str, help='output csv file', default='./subject_infos.csv')

    args = parser.parse_args()
    main(args)