import pandas as pd
import numpy as np
import argparse 
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy import stats

from utils import *

def main(args):
    sns.set_theme(context="poster")
    pal = sns.color_palette()
    j = 1

    font = 30

    plt.figure(figsize=(40,100))
    in_dir  = args.in_dir

    wmcol = 'WM'
    gmcol = 'GM'
    
    if args.col != '':
        wmcol = wmcol + '_' + args.col
        gmcol = gmcol + '_' + args.col


    for file in os.listdir(in_dir):
        csvfile = os.path.join(in_dir, file)

        param, ext = os.path.splitext(file)
        if ext == '.csv':

            df = pd.read_csv(csvfile)
            # df = df.rename(columns={"Modele": "Model"})
            # df = df.loc[ df.TR == 3 ]
            
            df["Mean_Brain"] = df[[gmcol, wmcol]].mean(axis=1)
            df, _ = clean_dataframe(df, 'Mean_Brain')

            plt.subplot(5,2, j)
            j+=1

            r_gm, p_gm = np.round(stats.pearsonr(df['Age'], df[gmcol]), decimals=5)
            r_wm, p_wm = np.round(stats.pearsonr(df['Age'], df[wmcol]), decimals=5)

            legend_gm = "Gray Matter: corr = {:.3f}, p = {:.1e} ".format(r_gm, p_gm)
            legend_wm = "White Matter: corr = {:.3f}, p = {:.1e} ".format(r_wm, p_wm)


            ax=sns.regplot(x='Age', y=gmcol, data=df,  scatter_kws={'alpha':0.7}, label=legend_gm)
            # plt.setp(ax.get_legend().get_title(), fontsize=font) # for legend title
            
            ax=sns.regplot(x='Age', y=wmcol, data=df,  scatter_kws={'alpha':0.7}, label=legend_wm)
            # plt.setp(ax.get_legend().get_title(), fontsize=font) # for legend title

            plt.legend(prop={'size': 6})
            plt.xlabel('Age', fontdict={'fontsize':font})
            plt.ylabel(param, fontdict={'fontsize':font})
            # plt.title('changes in {} with aging'.format(param))


    suptitle = 'HRF changes in WM/GM across aging'
    plt.suptitle(suptitle)
    plt.savefig(args.out_png)

    ## save fig

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply ComBAT to remove TR and scanners effects')

    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input csv file', required=True)
    input.add_argument('--col', type=str, help='column name to display', default='')

    ## output
    parser.add_argument('--out_png', type=str, help='output png file to save the img', default='./out.png')
    args = parser.parse_args()
    main(args)
