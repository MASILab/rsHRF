import os 
import argparse
import numpy as np
import pandas as pd

def main(args):

  df_age = pd.read_csv(args.csv_age_subject)
  df_TR = pd.read_csv(args.csv_TR_subject)
  df=pd.read_csv(args.csv_to_age)
  df_scan = pd.read_csv(args.csv_scanner)

  for index, row in df.iterrows():
    df_tr = df_TR.copy()
    dfage = df_age.copy()
    dfscan = df_scan.copy()

    experiment = row['Experiment']
    
    dfage = dfage.loc[ dfage['experiment'] == experiment]
    df_tr = df_tr.loc[ df_tr['experiment'] == experiment]
    dfscan = dfscan.loc[ dfscan['experiment'] == experiment]

    manu = dfscan['Manufacturer'].to_numpy()
    model = dfscan['Model'].to_numpy()
    if manu:

      df.at[index, 'Manufacturer'] = manu[0]
      df.at[index, 'Modele'] = model[0]

    TR = df_tr['TR'].to_numpy()

    age = dfage['age'].to_numpy()
    study = dfage['Study'].to_numpy()
    weight = dfage['Weight'].to_numpy()
    sex = dfage['Sex'].to_numpy()
    disease = dfage['ResearchGroup'].to_numpy()

    if TR:
      df.at[index, 'TR'] = TR[0]
    else:
      print('TR ', experiment)

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
  parser.add_argument('--csv_TR_subject', type=str)
  parser.add_argument('--csv_scanner', type=str)

  parser.add_argument('--outfile', type=str)

  args = parser.parse_args()

  main(args)

