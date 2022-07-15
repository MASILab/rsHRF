import pandas as pd
import numpy as np
import argparse 
import statsmodels.api as sm 
import scipy.stats as stats
import random
import matplotlib.pyplot as plt
import seaborn as sns

from patsy import dmatrix
from utils import remove_outlier

def bootstrap(df, model, covariates, knot, n_boot, n_sample_age):

    ## ranodmize knot value
    df_age = df.loc[ (df['Age'] >= knot -3) & (df['Age'] <= knot+3) ]
    list_knots = np.unique(df_age['Age'])


    x = np.zeros((n_boot,))
    bs_replicates = np.zeros((n_boot,n_sample_age))
    x = np.zeros((n_boot,n_sample_age))

    ## apply bootstrapping on age and predict regression spline
    for i in range(n_boot):
        k = random.choice(list_knots)
        df_sampled = df.sample(n=n_sample_age)
        bs_sample = df_sampled['Age']
        bs_sample = sorted(bs_sample)
        x[i,:] = bs_sample
        fit = model.predict(dmatrix("bs(Age, knots=(k,), degree=3)",{"Age": bs_sample, "k":k},return_type = 'dataframe' ))
    
        bs_replicates[i,:] = fit
    return bs_replicates, x

def model(df, x, y, covariates, knot, threshold=0.005):

    cubic_x1=dmatrix("bs(Age, knots=(k,), degree=3)",{"Age": df[x], 'k':knot},return_type = 'dataframe' )
    cubic_model = sm.GLM(df[y], cubic_x1).fit()

    ### linear regression to compare -- reduced model
    covariates.insert(0,x)
    reg_x1 = df[covariates]
    reg_x1 = sm.add_constant(reg_x1)
    regression_model = sm.OLS(df[y], reg_x1).fit()

    ### likelihood ratio test --- calculate likelihood ratio Chi-Squared test statistic ## difference of log-likelihood
    LR_statistic = -2*(regression_model.llf-cubic_model.llf)

    ### calculate p-value of test statistic using 2 degrees of freedom
    p_val = stats.chi2.sf(LR_statistic, 2)
    char = '<' if p_val < threshold else '>'
    test_result = "p ({:.4f}) {} {}".format(p_val, char, threshold)

    return cubic_model, regression_model, test_result


def main(args):
    ## to do: generalize model to different knot number
    sns.set_theme(context="talk")

    pal = sns.color_palette()
    
    params = ['Height', 'DipHeight', 'TroughHeight', 'PeakIntegral', 'DipIntegral','TroughIntegral', 'Time2peak', 'Time2dip', 'Time2trough',  'FWHM']
    
    ## arguments 
    tissus_name = args.index_cols
    covariates = args.covariates
    knot = args.knot
    n_boot = args.iter_boot
    group_name = ['CN', 'AD']
    ## to compute from number of params
    nrows, ncols = [50, 20]

    fg = plt.figure(figsize=(nrows,ncols))
    for i in range(10):
        feature = params[i]
        file = args.in_dir + feature + '.csv'
        df = pd.read_csv(file)

        ## conditions on data for analysis 
        df = df.loc[ (df['Age'] >= 65) & (df['Age'] <= 90) ]
        df = df.loc[df.TR ==3.0]

        plt.subplot(2,5,i+1)
        idx_color = 0
        colname = 'WM_Harmonization_TR_and_Scanner'
        for name in group_name:

            if name == 'AD':
                df_tmp = df.loc[ (df.ResearchGroup =='AD') | (df.ResearchGroup =='LMCI')]
                df_tmp, _ = remove_outlier(df_tmp, colname)
                name = 'LMCI and AD'
            
            else:
                df_tmp = df.loc[df.ResearchGroup ==name]
                df_tmp, _ = remove_outlier(df_tmp, colname)

            print(len(df_tmp))
            df_tmp = df_tmp.sort_values('Age')
            
            n_sample_age = int(len(df_tmp)*args.n_sample)

            m_cub, _, result_test  = model(df_tmp, 'Age', colname, covariates, knot)
            bs_replicates, out_x  = bootstrap(df_tmp,m_cub, covariates, knot, n_boot, n_sample_age)
            size_bs= np.shape(bs_replicates)

            ## confidence intervals procedure
            c1 = np.zeros((size_bs[1],))
            c2 = np.zeros((size_bs[1],))
            c_mean = np.zeros((size_bs[1],))
            axis_x  = np.zeros((size_bs[1],))

            for k in range(size_bs[1]):
                c1[k] = np.percentile(bs_replicates[:,k], [5])
                c2[k] = np.percentile(bs_replicates[:,k], [95])
                c_mean[k] = np.mean(bs_replicates[:, k])
                axis_x[k] = np.mean(out_x[:, k])

            sns.scatterplot(x='Age', y=colname, data=df_tmp, color=pal[idx_color], alpha=0.4)
            
            ## regression line                
            sns.lineplot(x=axis_x, y=c_mean, label="{} : {}".format(name, result_test), color = pal[idx_color])

            ## confidence intervals values
            plt.fill_between(axis_x, c1, c2, color=pal[idx_color], alpha=0.6)

            idx_color +=1

        tit = "Changes in aging in {} - cubic spline".format(feature)
        plt.title(tit)
        plt.xlabel('Age')
        plt.legend()

        # df_out.to_csv(args.out_csv, index=False)
    fg.savefig(args.out_png)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Modelisation of changes in aging')  
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input dir containing parameters csv file to analyze', required=True)
    input.add_argument('--covariates',  type=str, nargs='+', help='columns name in in_csv to use in regression model', default=[])
    input.add_argument('--index_cols', type=str,  nargs='+', help='columns name in in_csv to study changes', default=["GM", "WM"])

    ## param limear model
    regression = parser.add_argument_group('regression model arguments')
    regression.add_argument('--knot', type=int, help='knot value of spline', default=77)
    regression.add_argument('--iter_boot', type=int, help='number of iterations for the bootstrapping procedure', default=200)
    regression.add_argument('--n_sample', type=int, help='percentage of the data to use in the bootstrapping procedure', default=0.5)

    ## output
    parser.add_argument('--out_png', type=str, help='output png containing result of linear regression', default='./result_regression.png')
    args = parser.parse_args()
    main(args)