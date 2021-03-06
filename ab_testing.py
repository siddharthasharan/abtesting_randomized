# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 09:20:00 2019

@author: sharans
"""

import pandas as pd
import math as mt
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
# reading the sample data from Udacity A/B testing course for grocery website link
grocery_data = pd.read_csv(r'C:\Users\sharans\Documents\Deep_Learning_A_Z\Convolutional_Neural_Networks\Convolutional_Neural_Networks\dataset\grocerywebsiteabtestdata.csv')

# exploratory data analysis
grocery_data.head()
grocery_data.describe()

# Units for the data
# IP address: Unit of diversion (people, unique identifier)
#Population: Visitors without an account
# Duration of the experiment: 1 week workth of data
# Size: 1/3 of the data goes to test and 2/3 to control

# A/B testing involves three steps

# Clean data : For removing unwanted data pointsonly for control variables

#Step 1: Identify unique IP address in this data
ip_address= grocery_data['IP Address'].unique().tolist()
len(ip_address)

#step 2: remove customers who already have an account identified by LoggedInFlag =1 

g_data = grocery_data.loc[grocery_data['LoggedInFlag']==0]
g_data.head()
g_data.describe()

#step 3: Get rows with unique IP addresses only

g_data = g_data.drop_duplicates('IP Address')

# step 4: update serverid 2 and 3 control and 1 as test
g_data.loc[g_data.ServerID != 1, 'ServerID'] = 'Control'
g_data.loc[g_data.ServerID == 1, 'ServerID'] = 'Test'

g_data = g_data.drop(['Control', 'Test'], axis = 1)

g_data.head()

# Analyzing the results: 

# Step 1: get totals and sums 
col_list = list(g_data)
col_list.remove('RecordID')
col_list.remove('IP Address')
col_list.remove('LoggedInFlag')
col_list.remove('ServerID')
g_data['sum'] = g_data[col_list].sum(axis =1)
g_data.head()

#step 1a: get groups for total and percentage
g_count = g_data.groupby('ServerID')['VisitPageFlag'].count().reset_index()
g_sum = g_data.groupby('ServerID')['sum'].sum().reset_index()
g_result = pd.merge(g_count, g_sum, on = 'ServerID')
g_result['conversionpct'] = g_result['sum']/ g_result['VisitPageFlag']

# Overall we see a 3% higher conversion in test vs. control group

print(g_result)

# NExt analyze the p-value to see if the results are significant and repeatable.
# p-value should be less than 0.05
from scipy.stats import ttest_ind

test = g_data[g_data['ServerID']=='Test']
control = g_data[g_data['ServerID']=='Control']

ttest_ind(test['VisitPageFlag'], control['VisitPageFlag'])
# Ttest_indResult(statistic=10.893835883797658, pvalue=1.3256687794335583e-27
# p-value is less than 0.05 hence the results are significant
