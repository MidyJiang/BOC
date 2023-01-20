## -*- coding:utf-8 -*-
file='data/df.csv'
import os
for a,b,c in os.path.walk('data'):
  print(a,b,c)
