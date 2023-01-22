import pandas as pd
import numpy as np
import sys
import math
import logging

def topsis(inputfile,weight,impact,outputfile):
  '''if len(sys.argv) != 3:
    logging.error("Error: Wrong number of inputs provided.")
    return'''
  if ',' not in weight:
        logging.error("Error: Weights should be separated by ','")
        return
  weights=weight.split(',')
  try:
    weights=list(map(int,weights))
  except ValueError:
    logging.error("Error: Weights have non-integer value")
    return

  if ',' not in impact:
    logging.error("Error: Impacts should be separated by ','")
    return
  impacts=impact.split(',')
  for x in impacts:
    if x!='+' and x!='-':
      logging.error("Error: Impact must contain only '+' or '-'")
      return

  try:
    data1=pd.read_csv(inputfile)
  except FileNotFoundError:
    logging.error("Error: File not found.")

  if len(data1.iloc[0,:])<3:
    logging.error("Error: Columns in file less than 3.")

  data=data1.iloc[:,1:].values
  data=pd.DataFrame(data)
  data.dropna(inplace=True)
  row=len(data)
  col=len(data.iloc[0,:])

  '''for i in range(row):
    for j in range(col):
      try:
        data[i][j]=pd.to_numeric(data[i][j])
      except ValueError:
        logging.error("Error: Non-numeric value between 2nd to last column")'''

  if(col!=len(weights) or col!=len(impacts)):
    logging.error("Error: Length of inputs do not match.")
    return

  #root of sum of squares
  df=data.iloc[:,:]
  SquareRoots=[]
  for c in range(col):
    sum=0
    for r in range(row):
      d=data.iloc[r,c]
      x=d*d
      sum=sum+x
    root=math.sqrt(sum)
    SquareRoots.append(root)
  
  #normalizing data  
  j = 0
  while(j<col):
        for i in range(row):
            df[j][i] = df[j][i]/SquareRoots[j] 
        j = j+1
  
  #weighted normalized matrix
  for j in range(col):
    for i in range(row):
        df[j][i]=df[j][i]*weights[j]
  
  #idea best/ideal worst values
  ideal_best = (df.max().values)
  ideal_worst = (df.min().values)
  for i in range(col):
    if impacts[i] == '-':
      ideal_best[i], ideal_worst[i] = ideal_worst[i], ideal_best[i]

  #score - Eucledian distance
  score=[]
  for i in range(row):
    p,n=0,0
    for j in range(col):
      p += (ideal_best[j] - df.iloc[i, j])**2
      n += (ideal_worst[j] - df.iloc[i, j])**2
    p, n=p*0.5,n*0.5
    score.append(n/(p + n))

  data1['Topsis_score']=score
  data1['Rank'] = (data1['Topsis_score'].rank(method='max', ascending=False))

#   print(data1)
  data1.to_csv(outputfile)
  


