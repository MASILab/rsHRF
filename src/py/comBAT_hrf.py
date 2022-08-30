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

    ## prepare batch dataframe considering TR and Scanner
    keys = np.unique(df['Scanner'].to_numpy())
    model = df.copy()
    i = 0
    covars = pd.DataFrame()
    for k in keys:
        for tr in np.unique(df['TR'].to_numpy()):
            # model.loc[ (model['Scanner'] == k), 'Scanner'] = i
            model.loc[ (model['Scanner'] == k) & (model['TR']==tr), 'Scanner'] = i         
            i +=1
        
    covars['Scanner'] = model['Scanner']

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
        batch_col='Scanner',
        categorical_cols=categorical_cols)["data"]

    df_out = df.copy()

    for i in range(len(list_tissus)):
        df_out[ list_tissus[i] + '_' + exp_name] = data_combat[i,:]
    
    return df_out



def main(args):

    print("---- start ComBAT Harmonization ----")

    df = pd.read_csv(args.in_csv)
    df = df.dropna(subset=['Age'])

    if args.rois :
        indexes = df.columns.to_numpy()
        i=args.rois[1]
        list_rois = indexes[i:i+args.rois[0]]
    
    if args.gm_wm:
        list_rois = args.gm_wm


    print(list_rois)
    ## select scanner list
    if 'Scanner' in args.effects:   
        df_models_count = pd.DataFrame(df['Scanner'].value_counts())
        scans_to_keep = df_models_count.loc[ df_models_count['Scanner'] >= args.model_thd].index.to_numpy()
        print(scans_to_keep)

    ## select scanner list
    if 'TR' in args.effects:
        df_TR_count = pd.DataFrame(df['TR'].value_counts())
        TR_to_keep = df_TR_count.loc[ df_TR_count['TR'] >= args.TR_thd].index.to_numpy()
        print(TR_to_keep)

    ## clean dataframe from TR and scanners used less than 19 and 26 times
    df_clean = pd.DataFrame()
    if 'TR' in args.effects:
        df = df.loc[ df['TR'].isin(TR_to_keep)]
        for tr_i in TR_to_keep:

            df_1 = df.loc[ df['TR'] == tr_i]
            df_1.insert(5, "Mean_Brain",df_1[list_rois].mean(axis=1), True)

            df_1, _ = clean_dataframe(df_1, 'Mean_Brain')
            df_1 = df_1.drop(columns=['Mean_Brain'])
            df_clean = pd.concat([df_clean, df_1])

    # df_.drop(columns=['Mean_Brain'])

    if 'Scanner' in args.effects:        
        df_clean = df_clean.loc[ df_clean['Scanner'].isin(scans_to_keep)]

    column_name = 'harmonized'
    df_out = applyComBAT(df_clean, list_rois, args.add_covariates, args.effects, column_name)

    list_rois_harmonized = [s + '_harmonized' for s in list_rois]

    df_out['Mean_brain'] = df_out[ list_rois ].mean(axis=1)
    df_out['Mean_brain_harmonized'] = df_out[ list_rois_harmonized ].mean(axis=1)

    df_out.to_csv(args.out_csv, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply ComBAT to remove TR and scanners effects')
    
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_csv', type=str, help='input csv file containing the data to harmonize', required=True)
    input.add_argument('--TR_thd', type=int, help='threshold value to select TR for ComBAT', default=100)
    input.add_argument('--model_thd', type=int, help='threshold value to select Scanner for ComBAT', default=46)

    ## analysis type
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gm_wm', type=str,  nargs='+', help='columns name in in_csv to harmonize')
    group.add_argument('--rois', type=int,  nargs='+', help='rois to harmonize, specify number of roi and first column index')

    ## param comBAT
    combat = parser.add_argument_group('ComBAT arguments')
    combat.add_argument('--add_covariates', type=str, nargs='+', help='columns name in in_csv to use as covariates in ComBAT', default=[])
    combat.add_argument('--effects', type=str,nargs='+', help='effect to study, i.e. scanner effects. name should be in in_csv', default=["TR", "Scanner"])


    ## output
    parser.add_argument('--out_csv', type=str, help='output csv file containing the harmonized and original data', default='./list_subjects.csv')
    args = parser.parse_args()
    main(args)
