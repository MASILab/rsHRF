import pandas as pd
import numpy as np
import argparse 
import seaborn as sns
import matplotlib.pyplot as plt
import os

from utils import *

def set_axis(ax, xlabel, ylabel, font=30):
    plt.tight_layout()
    ax.set_ylabel(ylabel, fontsize=font)
    ax.set_xlabel(xlabel, fontsize=font)
    plt.xticks(fontsize=font-20)
    plt.yticks(fontsize=font-20)
    
def main(args):
    sns.set_theme(context="poster")
    pal = sns.color_palette()
    in_dir  = args.in_dir
    
    j = 0
    font=55

    params = ['Height', 'DipHeight', 'TroughHeight', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM', 'PeakIntegral', 'DipIntegral', 'TroughIntegral']

    n_cols = 4
    n_rows = len(params)

    plt.figure(figsize=(n_cols*25, n_rows*30))
    for i in range(len(params)):
        param = params[i]
        csvfile = in_dir +param+ '.csv'

        df = pd.read_csv(csvfile)

        df_tr = pd.DataFrame()
        for tr in args.TR_values:
            df_tmp = df.loc[(df['TR']==tr)]
            df_tmp, _ = remove_outlier(df_tmp, args.cols[0])            
            df_tr = pd.concat([df_tr, df_tmp])

        df = df_tr.copy()

        xmin = int(np.min(df['Age'])) -1
        xmax = round(np.max(df['Age'])) +1

        ymin = min(np.min(df[args.cols[0]]), np.min(df[args.cols[1]])) - 0.25
        ymax = max(np.max(df[args.cols[0]]), np.max(df[args.cols[1]])) + 0.25

        axis = [xmin, xmax, ymin, ymax] 

        plt.subplots_adjust(wspace=0.3) 


        ## TR - non harmonized
        ax= plt.subplot(n_rows,n_cols,j+1)
        hue_regplot(data=df, x='Age', y=args.cols[0], hue=args.effects[0], legend=True)
        plt.title("{} before ComBAT \n {} color ".format(param, args.effects[0]), fontdict={'fontsize':font+3})
        plt.legend(prop={'size': font-8}, loc="lower left")
        set_axis(ax, 'Age', args.cols[0], font)

        ## TR - harmonized
        ax =plt.subplot(n_rows,n_cols,j+2)
        hue_regplot(data=df, x='Age', y=args.cols[1], hue=args.effects[0], legend=True)
        plt.title("{} after ComBAT \n {} color".format(param, args.effects[0]), fontdict={'fontsize':font+3})
        plt.legend(prop={'size': font-8}, loc="upper right")
        set_axis(ax, 'Age', args.cols[1], font)

        ## Scanner - non harmonized
        ax =plt.subplot(n_rows,n_cols,j+3)
        hue_regplot(data=df, x='Age', y=args.cols[0], hue=args.effects[1])
        plt.title("{} before ComBAT \n Scanner color".format(param, args.effects[1]), fontdict={'fontsize':font+3})
        set_axis(ax, 'Age', args.cols[0], font)

        ## Scanner - harmonized
        ax =plt.subplot(n_rows,n_cols,j+4)
        hue_regplot(data=df, x='Age', y=args.cols[1], hue=args.effects[1], legend=True)
        plt.title("{} after ComBAT \n Scanner color".format(param, args.effects[1]), fontdict={'fontsize':font+3})
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left",prop={'size': font-5})
        set_axis(ax, 'Age', args.cols[1], font)
    
        j+=4

    plt.savefig(args.out_png)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display ComBAT results')
    
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input csv file containing the data harmonized', required=True)
    input.add_argument('--cols', type=str, nargs='+', help='columns name in csv file to compare, i.e. WM WM_harmonized or Mean_brain Mean_brain harmonized',required=True)
    input.add_argument('--effects', type=str, nargs='+', help='effects name in csv file to study, i.e. TR Scanner',required=True)
    input.add_argument('--TR_values', type=float, nargs='+', help='list of TR values to use',default=[0.607, 2, 3])

    ## output
    parser.add_argument('--out_png', type=str, help='output png file to save the img', default='./out.png')
    args = parser.parse_args()
    main(args)
