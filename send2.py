## -*- coding:utf-8 -*-
file='data/df.csv'
import os
print(4,os.path.abspath(''))
for a,b,c in os.walk(os.path.abspath('')):
  print('------',a,b,c)
