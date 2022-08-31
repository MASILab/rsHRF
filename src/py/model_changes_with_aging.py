import pandas as pd
import argparse 
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *

def main(args):

    sns.set_theme(context="poster")
    pal = sns.color_palette()
    
    params = ['Height', 'DipHeight', 'TroughHeight', 'PeakIntegral', 'DipIntegral','TroughIntegral', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM']
    
    ## arguments 
    covariates = args.covariates
    knot = args.knot
    n_boot = args.iter_boot
    font = 20
    model = args.model

    nrows, ncols = [5, 2]
    fg = plt.figure(figsize=(10*nrows,10*ncols))

    for i in range(len(params)):
        feature = params[i]
        file = args.in_dir + feature + '.csv'
        df = pd.read_csv(file)


        ## conditions on data for analysis 
        # df = df.loc[(df['Age'] >= 45) & (df['Age'] <= 99) ]
        df = df.loc[df.ResearchGroup =='CN']
        df = df.loc[df.TR.isin(args.TR)] ## changes in arguments


        df["Mean_Brain"] = df[[args.cols[0], args.cols[1]]].mean(axis=1)
        df, _ = remove_outlier(df, 'Mean_Brain')

        plt.subplot(2,5,i+1)
        idx_color = 0

        if model == 'linear':
            linear_model(df, 'Age', args.cols[0], feature, font, pal[0])
            linear_model(df, 'Age', args.cols[1], feature, font, pal[1])

        else:
            for col in args.cols:

                df, _ = remove_outlier(df, col)
                miny = df[ args.cols].min().min()
                maxy = df[ args.cols].max().max()

                minx, maxx = df['Age'].min(), df['Age'].max()
                
                df = df.sort_values('Age')
                
                n_sample_age = int(len(df)*args.n_sample)
                formula="bs(Age, knots=(77,), degree=3)"

                m_cub, _, result_test  = cubic_model(df, 'Age', col, args.covariates, knot, formula)
                bs_replicates, out_x  = bootstrap(df,m_cub, n_boot, n_sample_age, knot,formula)  #bootstrap(df, model, n_boot, n_sample_age, knot, formula)
                
                cmin, cmax, cmean, axis_x = compute_CI(bs_replicates, knot, out_x)

                sns.scatterplot(x='Age', y=col, data=df, color=pal[idx_color], alpha=0.4, s=250)

                range_val = abs(abs(maxy) - abs(miny))
                plt.axis([minx-1, maxx+1, miny -0.25*range_val, maxy + 0.1*range_val ])
                
                # regression line
                col_name =col.split('_')[0]

                sns.lineplot(x=axis_x, y=cmean, label="{} : {}".format(col_name, result_test), color = pal[idx_color],linewidth=5)

                # confidence intervals values
                plt.fill_between(axis_x, cmin, cmax, color=pal[idx_color], alpha=0.6)

                idx_color +=1

        plt.legend(loc='lower right', prop={'size': 30})

        plt.title(feature,fontdict={'size': font+10})
        plt.xlabel('Age', fontdict={'size': font})

        plt.tight_layout()

    fg.savefig(args.out_png)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modelisation of changes in aging wit two model linear or cubic')  
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input dir containing parameters csv file to analyze', required=True)
    input.add_argument('--covariates',  type=str, nargs='+', help='columns name in in_csv to use in regression model', default=[])
    input.add_argument('--cols', type=str,  nargs='+', help='columns name in in_csv to study changes', default=["GM", "WM"])
    input.add_argument('--model', type=str, help='model to use, linear or cubic', default='linear')
    input.add_argument('--TR', type=float, nargs='+', help='Repetition time to use', default=[0.607])

    ## param limear model
    regression = parser.add_argument_group('regression model arguments')
    regression.add_argument('--knot', type=int, help='knot value of spline', default=77)
    regression.add_argument('--iter_boot', type=int, help='number of iterations for the bootstrapping procedure', default=100)
    regression.add_argument('--n_sample', type=int, help='percentage of the data to use in the bootstrapping procedure', default=0.5)

    ## output
    parser.add_argument('--out_png', type=str, help='output png containing result of linear regression', default='./result_regression.png')
    args = parser.parse_args()
    main(args)