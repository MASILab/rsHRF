import pandas as pd
import numpy as np
import argparse 
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils import *

def set_axis_and_labels(x, y, roi_val, hemisphere):
    minx = min(x)
    maxx = max(x)

    miny = min(y)
    maxy = max(y)

    range_val = abs(abs(maxy) - abs(miny))
    axis = np.array([minx-1, maxx+1, miny -0.25*range_val, maxy + 0.1*range_val ])


    chars = roi_val.split('of')
    tmp_name = roi_val
    if len(chars) > 1:
        tmp_name = chars[0] + 'of \n ' + chars[1]
    
    if hemisphere == 'M':
        tit = tmp_name
    else:
        tit = tmp_name + ' - ' + hemisphere
    
    return axis, tit

def main(args):
    sns.set_theme(context="poster")
    pal = sns.color_palette()

    dic_color = {'L':0, 'R': 1, 'M': 2}
    
    params = ['Height', 'DipHeight', 'TroughHeight', 'PeakIntegral', 'DipIntegral','TroughIntegral', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM']
    
    ## arguments 
    filedir = args.in_dir
    outdir = args.out_dir 
    df_rois = pd.read_csv(args.roi_csv)
    df_rois = df_rois.loc[ df_rois['name'] != 'Inferior fronto-occipital fasciculus']
    df_rois = df_rois.loc[ df_rois['name'] != 'Unclassified']


    names_rois = df_rois['name'].drop_duplicates().to_numpy()

    knot = args.knot
    n_boot = args.iter_boot

    font = 20
    n_col = 6
    n_row = 3

    for feature in params[0:]:
        file = filedir + feature + '.csv'

        df = pd.read_csv(file)
        df = df.loc[ df.ResearchGroup =='CN']
        df = df.loc[ (df['Age'] >= 65) & (df['Age'] <= 90) ]
        df, _ = remove_outlier(df, 'Mean_brain_harmonized')

        ## find better than this 
        for offset in [0, 9, 18]:
            plt.figure(figsize=(n_col*6,n_row*6))
            j=1
            for i in range(offset, min(9+offset,len(names_rois))):
                roi_info = df_rois.loc[ df_rois.name == names_rois[i]]
                
                for idx, row in roi_info.iterrows():
                    location = row['location']
                    idx_color = dic_color[location]

                    col_name = str(roi_info.label.to_numpy()[0]) + '_harmonized'
                    df, _ = remove_outlier(df, col_name)
                    
                    if args.model == 'linear':
                        plt.subplot(3,6,j)
                        linear_model(df, 'Age', col_name, feature, font, color= pal[idx_color])
                        j+= 1
                        axis, title = set_axis_and_labels(df['Age'], df[col_name], names_rois[i], location)

                        plt.axis(axis)
                        plt.ylabel('')
                        plt.title(title)

                    else:

                        n_sample_age = int(len(df)*0.5)

                        formula="bs(Age, knots=(77,), degree=3)"
                        m_cub, _, result_test  = cubic_model(df, 'Age', col_name, [ ], 77, formula)
                        bs_replicates, out_x  = bootstrap(df,m_cub, 100, n_sample_age, 77,formula)  #bootstrap(df, model, n_boot, n_sample_age, knot, formula)
                        
                        c_min, c_max, c_mean, x_axis = compute_CI(bs_replicates, knot, out_x)

                        ## draw points, line and CIs
                        plt.subplot(3,6,j)
                        sns.scatterplot(x='Age', y=col_name, data=df, color=pal[idx_color], alpha=0.4)
                        sns.lineplot(x=x_axis, y=c_mean, color= pal[idx_color], label="{}".format(result_test))
                        plt.fill_between(x_axis, c_min, c_max, color= pal[idx_color],alpha=0.6)

                        axis, title = set_axis_and_labels(df['Age'], df[col_name], names_rois[i], location)

                        plt.axis(axis)
                        plt.ylabel('')
                        plt.title(title)

                        j+= 1

            plt.tight_layout()
            plt.subplots_adjust(hspace=0.4, wspace=0.3)

            name_file = '{}_reg_{}_feature_rois_{}_to_{}.png'.format(args.model, feature, 2*offset, i*2+1)
            plt.savefig(os.path.join(args.out_dir, name_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modelisation of changes in aging')  
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input dir containing parameters csv file to analyze', required=True)
    input.add_argument('--covariates',  type=str, nargs='+', help='columns name in in_csv to use in regression model', default=[])
    input.add_argument('--model', type=str, help='model to use, linear or cubic', default='linear')
    
    input.add_argument('--roi_csv', type=str, help='path to roi csv file', required=True)

    ## param limear model
    regression = parser.add_argument_group('regression model arguments')
    regression.add_argument('--knot', type=int, help='knot value of spline', default=77)
    regression.add_argument('--iter_boot', type=int, help='number of iterations for the bootstrapping procedure', default=100)
    regression.add_argument('--n_sample', type=int, help='percentage of the data to use in the bootstrapping procedure', default=0.5)

    ## output
    parser.add_argument('--out_dir', type=str, help='output directory to save images', default='.')
    args = parser.parse_args()
    main(args)