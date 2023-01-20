## -*- coding:utf-8 -*-

import os
print(4,os.path.abspath(''))
file=os.environ["SDF"]
import pandas as pd
df=pd.read_csv(file)
print(8,type(df),len(df))
print(9,df)
