## -*- coding:utf-8 -*-
file='data/df.csv'
import os
print(os.path.abspath(''))
for a,b,c in os.path.walk(''):
  print(a,b,c)
