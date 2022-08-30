import os 
import argparse
import numpy as np
import pandas as pd

def main(args):

  df_age = pd.read_csv(args.csv_age_subject)
  df=pd.read_csv(args.csv_to_age)
  print(df.head(), df_age.head())
  df['Subject'] = 'Nan'


  for index, row in df.iterrows():
    dfage = df_age.copy()

    exp = row['Experiment']
    dfage = dfage.loc[ dfage.Experiment.str.contains(exp)]

    if len(dfage) > 0 :
        sub = dfage['Subject'].to_numpy()
        
        df.at[index, 'Subject'] = sub[0]
        model = dfage['Scanner'].to_numpy()
        df.at[index, 'Scanner'] = model[0]
        
        tr = dfage['TR'].to_numpy()
        df.at[index, 'TR'] = tr[0]

        age = dfage['Age'].to_numpy()
        df.at[index, 'Age'] = age[0]

        study = dfage['Study'].to_numpy()
        df.at[index, 'Study'] = study[0]
        
        sex = dfage['Sex'].to_numpy()
        df.at[index, 'Sex'] = sex[0]

        dx = dfage['ResearchGroup'].to_numpy()
        df.at[index, 'ResearchGroup'] = dx[0]

    
    else:
        print(row['Experiment'])


# df.to_csv(args.outfile, index=False)

  df.to_csv(args.outfile, index=False)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='')

  parser.add_argument('--csv_age_subject', type=str)
  parser.add_argument('--csv_to_age', type=str)
    #   parser.add_argument('--csv_site', type=str)

  parser.add_argument('--outfile', type=str)

  args = parser.parse_args()

  main(args)

