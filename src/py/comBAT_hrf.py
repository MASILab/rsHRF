import pandas as pd
import numpy as np
import argparse 

from neuroCombat import neuroCombat
from utils import *

def applyComBAT(df, list_tissus,  list_params_studied, list_effects ,exp_name):

    ## prepare data in the good format
    dfdata = df[ list_tissus ]
    dfdata = dfdata.transpose()

    filename = '../../../rsHRF_project/test.csv'
    dfdata.to_csv(filename, index=False)
    dfdata = pd.read_csv(filename)

    data = np.genfromtxt(filename, delimiter=',', skip_header=1)
    data = data[0: len(list_tissus),:] #take only the tissus specified

    ## prepare batch dataframe considering TR and Model
    keys = np.unique(df['Model'].to_numpy())
    model = df.copy()
    i = 0
    covars = pd.DataFrame()
    for k in keys:
        for tr in np.unique(df['TR'].to_numpy()):
            model.loc[ (model['Model'] == k) & (model['TR']==tr), 'Model'] = i
            i +=1
        
    covars['Model_and_TR'] = model['Model']

    categorical_cols = []
    ## other covariates
    for param in list_params_studied:
        # categorical & char variables -> change in binary
        if param =='Sex':
            gender = df.copy()
            gender.loc[gender["Sex"] == "F", "Sex"] = 1
            gender.loc[gender["Sex"] == "M", "Sex"] = 2
            
            covars['Sex'] = gender["Sex"].to_numpy() 
            categorical_cols = ['Sex']

        else:
            covars[param] = df[param].to_numpy() 

    # # # Harmonization step:
    data_combat = neuroCombat(dat=data,
        covars=covars,
        batch_col='Model_and_TR',
        categorical_cols=categorical_cols)["data"]

    df_out = df.copy()

    for i in range(len(list_tissus)):
        df_out[ list_tissus[i] + '_' + exp_name] = data_combat[i,:]
    
    return df_out



def main(args):

    print("---- start ComBAT Harmonization ----")

    df = pd.read_csv(args.in_csv)
    df = df.rename(columns={"Modele": "Model"})

    print(df)

    ## select scanner list
    if 'Model' in args.effects:   
        df_models_count = pd.DataFrame(df['Model'].value_counts())
        scans_to_keep = df_models_count.loc[ df_models_count['Model'] >= args.model_thd].index.to_numpy()

    ## select scanner list
    if 'TR' in args.effects:
        df_TR_count = pd.DataFrame(df['TR'].value_counts())
        TR_to_keep = df_TR_count.loc[ df_TR_count['TR'] >= args.TR_thd].index.to_numpy()

    print(TR_to_keep, scans_to_keep)

    ## clean dataframe from TR and scanners used less than 19 and 26 times
    df_clean = pd.DataFrame()
    if 'TR' in args.effects:
        for tr_i in TR_to_keep:

            df_1 = df.loc[ df['TR'] == tr_i]
            df_1["Mean_Brain"] = df_1[["GM", "WM"]].mean(axis=1)
            df_1, _ = clean_dataframe(df_1, 'Mean_Brain')
            df_clean = pd.concat([df_clean, df_1])

    if 'Model' in args.effects:        
        df_clean = df_clean.loc[ df_clean['Model'].isin(scans_to_keep)]


    column_name = 'Harmonization_' + "_and_".join(args.effects)
    df_out = applyComBAT(df_clean, args.params_to_harmonize, args.add_covariates, args.effects, column_name)
    df_out.to_csv(args.out_csv, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply ComBAT to remove TR and scanners effects')
    
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_csv', type=str, help='input csv file containing the data to harmonize', required=True)
    input.add_argument('--TR_thd', type=int, help='threshold value to select TR for ComBAT', default=19)
    input.add_argument('--model_thd', type=int, help='threshold value to select Model for ComBAT', default=26)

    ## param comBAT
    combat = parser.add_argument_group('ComBAT arguments')
    combat.add_argument('--params_to_harmonize', type=str,  nargs='+', help='columns name in in_csv to harmonize', default=["WM", "GM"])
    combat.add_argument('--add_covariates', type=str, nargs='+', help='columns name in in_csv to use as covariates in ComBAT', default=[])
    combat.add_argument('--effects', type=str,nargs='+', help='effect to study, i.e. scanner effects. name should be in in_csv', default=['TR, Model'])


    ## output
    parser.add_argument('--out_csv', type=str, help='output csv file containing the harmonized and original data', default='./list_subjects.csv')
    args = parser.parse_args()
    main(args)
