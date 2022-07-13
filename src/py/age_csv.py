import os 
import argparse
import numpy as np
import pandas as pd

def main(args):

  df_age = pd.read_csv(args.csv_age_subject)
  df=pd.read_csv(args.csv_to_age)
  df_site = pd.read_csv(args.csv_site)

  for index, row in df.iterrows():
    dfage = df_age.copy()
    dfsite = df_site.copy()

    experiment = row['Experiment']
    
    dfage = dfage.loc[ dfage['experiment'] == experiment]
    dfsite = dfsite.loc[ dfsite['Experiment'] == experiment]

    manu = dfsite['Manufacturer'].to_numpy()
    model = dfsite['Scanner'].to_numpy()
    freq = dfsite['Frequence'].to_numpy()
    site = dfsite['Site'].to_numpy()
    tr = dfsite['TR'].to_numpy()
    
    df.at[index, 'Manufacturer'] = manu[0]
    df.at[index, 'Scanner'] = model[0]
    df.at[index, 'Frequence'] = freq[0]
    df.at[index, 'Site'] = site[0]
    df.at[index, 'TR'] = tr[0]

    age = dfage['age'].to_numpy()
    study = dfage['Study'].to_numpy()
    weight = dfage['Weight'].to_numpy()
    sex = dfage['Sex'].to_numpy()
    disease = dfage['ResearchGroup'].to_numpy()

    if age: 
      df.at[index, 'Age'] = age[0]
      df.at[index, 'Study'] = study[0]
      df.at[index, 'Sex'] = sex[0]
      df.at[index, 'Weight'] = weight[0]
      df.at[index, 'ResearchGroup'] = disease[0]
      
    else:
      print('Study ', experiment)

  df.to_csv(args.outfile, index=False)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='')

  parser.add_argument('--csv_age_subject', type=str)
  parser.add_argument('--csv_to_age', type=str)
  parser.add_argument('--csv_site', type=str)

  parser.add_argument('--outfile', type=str)

  args = parser.parse_args()

  main(args)

