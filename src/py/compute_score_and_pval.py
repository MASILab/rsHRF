import argparse
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import itertools

import scipy.stats as stats
import seaborn as sns

from utils import cohens_d, clean_dataframe


def set_axis(fig, ax, params, y_axis_name, test, name):
    nb_features = len(params)
    nb_manu = len(y_axis_name)

    fig.subplots_adjust(hspace=1)

    ax.set_xticks(np.arange(nb_features)+0.5, params, rotation=45, fontsize=20)
    ax.set_yticks(np.arange(nb_manu)+0.5, y_axis_name, rotation=0, fontsize=20)

    ax.set_title("{} score for each feature in {:}".format(test,name), fontsize=25,pad=30)
    ax.set_xlabel("HRF feature",labelpad=30, fontsize=20)
    ax.set_ylabel("scanner effect studied",labelpad=30, fontsize=20)

    return fig


def main(args):

    y_axis_name = []
    
    min_x = 0
    max_x = 0

    params = ['Height', 'DipHeight', 'TroughHeight', 'PeakIntegral', 'DipIntegral','TroughIntegral', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM']
    col = args.effect
    tissus = ['WM', 'WM_Harmonization_TR_and_Scanner']
    name =  ['WM before harmonization', 'WM after harmonization of TR and scanners']
    

    ## compute combination
    labels_age = ['[65;70]',']70;75]',']75;80]', ']80;85]', ']85;90]']
    if col == 'Manufacturer':
        labels_manu = ['GE', 'Philips', 'Siemens']
        combination = list(itertools.combinations(labels_manu, 2))
    elif col == 'Age':
        combination = list(itertools.combinations(labels_age, 2))

    nb_manu = len(combination)
    nb_features = len(params) 
    mat_d = np.zeros(shape=(nb_manu,nb_features))
    mat_d_p = np.zeros(shape=(nb_manu,nb_features))

    bool_pval = False

    fig1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(20,15))
    fig2, ax2 = plt.subplots(nrows=2, ncols=1, figsize=(20,15))

    for k in range(2):
        tissu = tissus[k]
        for i in range(nb_features):
            feature = params[i]
            file = args.in_dir + feature + '_canonical.csv'
            df = pd.read_csv(file)

            df = df.loc[(df['Age'] >=65) & (df['Age'] <=90)]
            df['Age'] = pd.cut(df.Age,bins=[65, 70, 75, 80, 85, 90],labels=labels_age)    
            

            df_2 = df.loc[ df['TR'] == 3]
            df_2.insert(5, "Mean_Brain",df_2[["GM", "WM"]].mean(axis=1), True)
            df_2, _ = clean_dataframe(df_2, 'Mean_Brain')


            df_1 = df.loc[ df['TR'] == 0.607]
            df_1.insert(5, "Mean_Brain",df_1[["GM", "WM"]].mean(axis=1), True)
            # df_1["Mean_Brain"] = 
            df_1, _ = clean_dataframe(df_1, 'Mean_Brain')
            df = pd.concat([df_2, df_1])


            for j in range(nb_manu):
                sub_col_1 = combination[j][0]
                sub_col_2 = combination[j][1]

                df_1 = df.loc[df[col]== sub_col_1]
                df_2 = df.loc[df[col]== sub_col_2]

                name_d = sub_col_1 + "/" + sub_col_2
                y_axis_name.append(name_d)

                if args.type == 'kruskal':
                    F, p = stats.kruskal( df_1[tissu],  df_2[tissu])
                    cmap = sns.color_palette("rocket", as_cmap=True)
                    
                    mat_d[j,i] = F
                    mat_d_p[j,i] = p
                    bool_pval = True

                elif args.type=='cohen':
                    c = cohens_d(df_1[tissu], df_2[tissu])
                    cmap = sns.diverging_palette(240, 10, n=9)     
                    mat_d[j,i] = c

        if args.type == 'kruskal':

            min_x = min(mat_d.min(), min_x)
            max_x = max(mat_d.max(), max_x)
        
        elif args.type=='cohen':
            c = cohens_d(df_1[tissu], df_2[tissu])
            mat_d[j,i] = c

            max_x = max( abs(mat_d.max()), max_x)
            min_x = -max_x

        y_axis_name = y_axis_name[0:nb_manu]
        
        sns.heatmap(mat_d, cmap = cmap, vmax=max_x, vmin=min_x, annot=True, annot_kws={"fontsize":15}, ax=ax1[k])
        fig1 = set_axis(fig1, ax1[k], params, y_axis_name, args.type, name[k])

        if bool_pval == True:
            sns.heatmap(mat_d_p, cmap = cmap, vmax=1, vmin=0, annot=True, annot_kws={"fontsize":15}, ax=ax2[k])
            fig2 = set_axis(fig2, ax2[k], params, y_axis_name, 'pval of {}'.format(args.type), name[k])
    
    outfile = args.out + "ComBAT_performance_{}_test_{}_effect_canonical_data.png".format(args.type, args.effect)
    fig1.savefig(outfile)


    if bool_pval == True:
        outfile2 = args.out + "ComBAT_performance_{}_pval_{}_effect_canonical_data.png".format(args.type, args.effect)
        fig2.savefig(outfile2)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute a metric for all HRF features and save is a png')
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input csv file containing the data harmonized', required=True)
    input.add_argument('--type', type=str, help='metric to compute i.e. cohen, kurskal or anova',required=True) 
    input.add_argument('--effect', type=str, help='effect to study i.e. Age, Manufacturer',required=True)

    ## output
    parser.add_argument('--out', type=str, help='output png file to save the img', default='./out.png')
    args = parser.parse_args()
    main(args)