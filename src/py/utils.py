from statistics import mean, stdev
from math import sqrt
import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

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
