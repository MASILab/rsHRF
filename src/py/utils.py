from statistics import mean, stdev
from math import sqrt
import numpy as np
import pandas as pd 
import seaborn as sns
import statsmodels.api as sm 
import scipy.stats as stats
import random
import matplotlib.pyplot as plt

from patsy import dmatrix

def remove_outlier(df, index):
    Q1 = df[index].quantile(0.25)
    Q3 = df[index].quantile(0.75)

    IQR = Q3 - Q1

    filter = (df[index] >= Q1 - 1.5*IQR) &  (df[index] <= Q3 + 1.5*IQR)
    outlier =  (df[index] <= Q1 - 1.5*IQR) |  (df[index] >= Q3 + 1.5*IQR)

    return df.loc[filter], df.loc[outlier]

def clean_dataframe(df, index):

  df = df[(df != 0).all(1)]
  df = df.dropna()
  df_inliers, df_outlier = remove_outlier(df, index)


  return df_inliers, df_outlier

def cohens_d(c0, c1):
  std_diff = sqrt((stdev(c0) ** 2 + stdev(c1) ** 2) / 2)
  return (mean(c0) - mean(c1)) / std_diff



def hue_regplot(data, x, y, hue, palette=None, legend=False, **kwargs):
    
    regplots = []
    levels = data[hue].unique()
    pal = sns.color_palette("husl", n_colors=len(levels))
    
    i = 0
    if legend:
        for key in levels:
            regplots.append(sns.regplot(x=x, y=y, data=data[data[hue] == key], color=pal[i], label= key, scatter_kws={'s':300}))
            i +=1
            # plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left")

    else:
        for key in levels:
            regplots.append(sns.regplot(x=x, y=y, data=data[data[hue] == key], color=pal[i],scatter_kws={'s':300}))
            i +=1

    return regplots



### put in utils file
def bootstrap(df, model, n_boot, n_sample_age, knot, formula):

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

        df_sampled.sort_values(by=['Age'])

        # print(df_sampled['Age'].min())
        x[i,:] = bs_sample
        fit = model.predict(dmatrix(formula,{"Age": bs_sample},return_type = 'dataframe' ))

        bs_replicates[i,:] = fit
    
    return bs_replicates, x

def cubic_model(df, x, y, covariates, knot, formula, threshold=0.005):

    cubic_x1=dmatrix(formula,{"Age": df[x], 'k':knot},return_type = 'dataframe' )
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
    test_result = "p ={:.4f}".format(p_val)

    return cubic_model, regression_model, test_result

def compute_CI(bs_replicates, knot, out_x):
    size_bs= np.shape(bs_replicates)
    cmin = np.zeros((size_bs[1],))
    cmax = np.zeros((size_bs[1],))
    cmean = np.zeros((size_bs[1],))
    axis  = np.zeros((size_bs[1],))

    for k in range(size_bs[1]):
        cmin[k] = np.percentile(bs_replicates[:,k], [5])
        cmax[k] = np.percentile(bs_replicates[:,k], [95])
        cmean[k] = np.mean(bs_replicates[:, k])
        axis[k] = np.mean(out_x[:, k])

    return cmin, cmax, cmean, axis

def linear_model(df, x, col, feature, font, color):

    name = col.split('_')[0]

    r, p = np.round(stats.pearsonr(df[x], df[col]), decimals=5)
    legend = "{}: r={:.3f}, p={:.1e} ".format(name, r, p)
    ax=sns.regplot(x=x, y=col, data=df, color=color, scatter_kws={'alpha':0.7}, label=legend)

    plt.legend(prop={'size': 20})
    plt.title(feature, fontdict={'fontsize':font})
    plt.xlabel(x, fontdict={'fontsize':font})
    plt.ylabel('')
