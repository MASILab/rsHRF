import pandas as pd
import numpy as np
import argparse 
import seaborn as sns
import matplotlib.pyplot as plt
import os

from utils import *

def main(args):
    sns.set_theme(context="poster")
    pal = sns.color_palette()
    j = 0

    n_cols = 4
    n_rows = 10
    plt.figure(figsize=(n_cols*12, n_rows*12))
    in_dir  = args.in_dir
    for file in os.listdir(in_dir):
        csvfile = os.path.join(in_dir, file)
        param, ext = os.path.splitext(file)
        if ext == '.csv':

            df = pd.read_csv(csvfile)

            df, _ = remove_outlier(df, args.cols[0])
            # df = df.rename(columns={"Modele": "Model"})

            xmin = int(np.min(df['Age'])) -1
            xmax = round(np.max(df['Age'])) +1

            ymin = min(np.min(df[args.cols[0]]), np.min(df[args.cols[1]])) - 0.25
            ymax = max(np.max(df[args.cols[0]]), np.max(df[args.cols[1]])) + 0.25

            axis = [xmin, xmax, ymin, ymax] 


            ax = plt.subplot(n_rows,n_cols,j+1)

            df = df.loc[ (df['TR'] ==0.607) | (df['TR'] ==3.0) ]
            # print(df)
            plot_hue = hue_regplot(data=df, x='Age', y=args.cols[0], hue=args.effects[0])
            plt.title("{} in {} before ComBAT - {} color ".format(param, args.cols[0], args.effects[0]))
            # plt.axis(axis)

            plt.subplot(n_rows,n_cols,j+2)
            plot_hue = hue_regplot(data=df, x='Age', y=args.cols[1], hue=args.effects[0], legend=True)
            plt.title("{} in {} after ComBAT - {} color".format(param, args.cols[0], args.effects[0]))
            plt.legend()
            # plt.axis(axis)

            ax = plt.subplot(n_rows,n_cols,j+3)
            plot_hue = hue_regplot(data=df, x='Age', y=args.cols[0], hue=args.effects[1])
            plt.title("{} in {} before ComBAT - Scanner color".format(param, args.cols[0], args.effects[1]))
            # plt.axis(axis)

            ax = plt.subplot(n_rows,n_cols,j+4)
            plot_hue = hue_regplot(data=df, x='Age', y=args.cols[1], hue=args.effects[1], legend=True)
            plt.title("{} in {} after ComBAT  - Scanner color".format(param, args.cols[0], args.effects[1]))
            plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left")
            # plt.axis(axis)

            j+=4

    suptitle = 'Results of harmonization in ' + args.cols[0] + ' across aging - left is TR color - right is scanner color'
    plt.suptitle(suptitle)
    plt.savefig(args.out_png)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display ComBAT results')
    
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input csv file containing the data harmonized', required=True)
    input.add_argument('--cols', type=str, nargs='+', help='columns name in csv file to compare',required=True)
    input.add_argument('--effects', type=str, nargs='+', help='effects name in csv file to study',required=True)

    ## output
    parser.add_argument('--out_png', type=str, help='output png file to save the img', default='./out.png')
    args = parser.parse_args()
    main(args)
