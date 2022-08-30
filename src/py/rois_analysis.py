import argparse
from curses.panel import bottom_panel
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import itertools

import scipy.stats as stats
import seaborn as sns
from patsy import dmatrix
import statsmodels.api as sm 

from utils import *



def set_axis(fig, ax, params, text, font=20):

    plt.text(24,1, "Legend: \n", fontsize=font)
    plt.text(24,10, text, fontsize=font-5)


    nb_features = len(params)

    ax.set_yticks(np.arange(nb_features)+1, params, rotation=45, fontsize=font)

    ax.set_ylabel("feature",labelpad=20, fontsize=font)
    ax.set_xlabel("WM tract index",labelpad=20, fontsize=font)

    return fig


def LR_indicator(df, idx_rois_L, idx_rois_R, df_rois):
    list_cols_L = []
    list_cols_R = []

    indicator_name = 'hemisphere'

    for idx in idx_rois_L:
        list_cols_L.append(str(idx)+'_harmonized')

    for idx in idx_rois_R:
        list_cols_R.append(str(idx)+'_harmonized')

    names_roi_L = df_rois.loc[df_rois['label'].isin(idx_rois_L)]
    names_roi_R = df_rois.loc[df_rois['label'].isin(idx_rois_R)]

    newcols_names = names_roi_R.name.to_list()
    newcols_names.insert(0,'Sex')
    newcols_names.insert(0,'Age')
    newcols_names.insert(0,'Experiment')

    df_L = df.drop(columns=list_cols_R)
    df_L.columns = newcols_names
    df_L[indicator_name] = 0

    df_R = df.drop(columns=list_cols_L)
    df_R.columns = newcols_names
    df_R[indicator_name] = 1

    return pd.concat([df_L, df_R]), indicator_name


def tract_indicator(df, list_cols):
    
    df_all = pd.DataFrame()
    indicator_name = 'tract'
    y_name = 'value'

    for col_name in list_cols:
        idx_rois = int(col_name.split('_')[0])
        values = df[col_name].to_numpy()
        label = idx_rois * np.ones_like(values)

        df_roi = pd.DataFrame({'Experiment':df.Experiment.to_numpy(), 'Sex':df.Sex.to_numpy(), 'Age':df.Age.to_numpy(), 
                                y_name:values, indicator_name:label})

        df_all = pd.concat([df_all, df_roi])
    
    return df_all, indicator_name, y_name

def main(args):

    params = ['Height', 'DipHeight', 'TroughHeight', 'PeakIntegral', 'DipIntegral','TroughIntegral', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM']
    
    type_analysis = args.type ## symmetry or tract analysis 
    filedir = args.in_dir    
    font = 15

    p_val_arr = np.zeros((len(params),1))

    ## process dataframe 
    rois_csv = args.roi_csv
    df_rois = pd.read_csv(rois_csv)
    df_rois = df_rois.loc[ df_rois['name'] != 'Inferior fronto-occipital fasciculus']
    df_rois = df_rois.loc[ df_rois['name'] != 'Unclassified']

    
    if type_analysis == 'symmetry':
        df_rois = df_rois.loc[df_rois['location']!='M']

    idx_rois = df_rois['label'].to_numpy()

    cols_to_keep = ['Experiment', 'Age', 'Sex']
    for idx in idx_rois:
        str_label = str(idx)+ '_harmonized'
        cols_to_keep.append(str_label)


    rois = df_rois.drop_duplicates(subset=['name'])
    names_rois = rois['name'].to_numpy()

    legend = ""
    for j in range(len(names_rois)):
        legend += "{} : {} \n".format(j, names_rois[j])

    ### compute df_rois, list_rois or list_rois L/R
    if type_analysis == 'symmetry':
        idx_L = df_rois.loc[df_rois['location'] == 'L']['label'].to_numpy()
        idx_R = df_rois.loc[df_rois['location'] == 'R']['label'].to_numpy()

        cohen_d_arr = np.zeros((len(params), len(idx_L)))
        p_val_arr = np.zeros((len(params), len(idx_L)))

    for i in range(10):
        feature = params[i]
        file = filedir + feature + '.csv'
        df = pd.read_csv(file)
        
        df, _ = remove_outlier(df, 'Mean_brain_harmonized')
        
        df = df.loc[ (df['Age'] >= 65) & (df['Age'] <= 90) ]
        df = df.loc[df.ResearchGroup =='CN']
        df.loc[df["Sex"] == "F", "Sex"] = 0
        df.loc[df["Sex"] == "M", "Sex"] = 1

        df = df[cols_to_keep]

        ## dataframe formatting 
        if type_analysis == 'symmetry':
            df, indicator_name = LR_indicator(df, idx_L, idx_R, df_rois=df_rois)
        else:
            df, indicator_name, y_name = tract_indicator(df, cols_to_keep[3:])


        formula = "bs(Age, knots = (77,), degree=3) + indicator + sex"
        data_dict = {"Age": df['Age'], "indicator": df[indicator_name], 'sex':df['Sex']}

        if type_analysis == 'symmetry':
            for j in range(len(names_rois)):

                df_tmp = df[ [names_rois[j], 'hemisphere'] ]
                df1 = df_tmp.loc[df_tmp.hemisphere == 0]
                df2 = df_tmp.loc[df_tmp.hemisphere == 1]

                d = cohens_d(df1[names_rois[j]], df2[names_rois[j]])
                cohen_d_arr[i,j] = d

                x1 = dmatrix(formula, data_dict, return_type = 'dataframe')
                m1 = sm.GLM(df[names_rois[j]], x1).fit()
                p_val_arr[i,j] = m1.pvalues[-1]

        else:
            
            x1 = dmatrix(formula, data_dict, return_type = 'dataframe')
            m1 = sm.GLM(df[y_name], x1).fit()

            p_val_arr[i,0] = m1.pvalues[-1]

    df = pd.DataFrame({'feature':params, 'p-values':p_val_arr[:,0]})
    
    print(df)



    if type_analysis == 'symmetry':

        fig = plt.figure(figsize=(60,40))
        ax = sns.heatmap(p_val_arr, cmap = 'Greens_r', square=True, annot=True, annot_kws={"fontsize":font-8}, cbar_kws={"shrink":0.7})
        ax = sns.heatmap(p_val_arr, mask=p_val_arr < 0.005, cmap='Oranges', vmin=-0.50, square=True, annot=False, cbar=False)
        set_axis(fig, ax, params,legend, font=font)


        fig = plt.figure(figsize=(60,40))
        xmin = np.min(cohen_d_arr)
        xmax = np.max(cohen_d_arr)
        t = max( abs(xmin), abs(xmax))


        cmap = sns.diverging_palette(240, 10, n=9)     
        ax = sns.heatmap(cohen_d_arr, cmap = cmap, vmin = -t, vmax= t, square=True, annot=True, annot_kws={"fontsize":font-5}, cbar_kws={"shrink":0.7})
        set_axis(fig, ax, params,legend, font=font)

        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute a metric for all HRF features and save is a png')
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input csv file containing the data harmonized', required=True)
    input.add_argument('--type', type=str, help='type of analysis i.e. symmetry L/R or by WM tracts',required=True) 
    input.add_argument('--roi_csv', type=str, help='effect to study i.e. Age, Manufacturer',required=True)

    ## output
    parser.add_argument('--out', type=str, help='output dir to save the img', default='./')
    args = parser.parse_args()
    main(args)