# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 18:19:06 2022

@author: kharr
"""

# -*- coding: utf-8 -*-
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import warnings
import statistics as st 
import sys



warnings.filterwarnings("ignore")

df = pd.read_csv('formatted_allstops(expanded)(2).csv')

#STEP 2: DATA PREPARATION - DROP IRRELEVANT DATA AND CONVERT TO CORRECT FORMAT
df = df[['durationofstop', 'raceperceivedpriortostop',                 
         'perceivedraceorethnicity', 'resultofstop',
        'gender', 'perceivedage',  
        'typeofstop', 'tract_medianincome',
        'tract_totalpop', 'tract_whitepop', 'tract_nonwhitecomp',
        'tract_poccomp', 'tract_nonwhitepop', 'tract_pocpop',
        'tract_aapop', 'tract_na_aipop', 'tract_aisianpop',
        'tract_hawaiian', 'tract_mixed2', 'tract_totalnumstops',
        'tract_annualstops', 'tract_distancefromcal']]




#STEP 3: CODING VALUES
df.perceivedraceorethnicity[df.perceivedraceorethnicity == 'White'] = 2
df.perceivedraceorethnicity[df.perceivedraceorethnicity == 'Black/African American'] = 3
df.perceivedraceorethnicity[df.perceivedraceorethnicity ==  'Black'] = 3
df.perceivedraceorethnicity[df.perceivedraceorethnicity=="Hispanic/Latino"] = 4 
df.perceivedraceorethnicity[df.perceivedraceorethnicity=="Hispanic"] = 4
df.perceivedraceorethnicity[df.perceivedraceorethnicity == 'Asian'] = 5
df[~df['perceivedraceorethnicity'].isin([2,3,4,5])] = 1
# print(f'the value counts for ethnicity are {df.perceivedraceorethnicity.value_counts()}\n')
# sys.exit('Look it worked!')



df['black'] = np.where(df['perceivedraceorethnicity'] == 3, 1,0)
np.where(df['black'] == 3, 0,0)
df['white'] = np.where(df['perceivedraceorethnicity'] == 2, 1,0)
np.where(df['white'] == 3, 0,0)
df['asian'] = np.where(df['perceivedraceorethnicity'] == 5, 1,0)
np.where(df['asian'] == 3, 0,0)
df['hispanic'] = np.where(df['perceivedraceorethnicity'] == 4, 1,0)
np.where(df['hispanic'] == 3, 0,0)



        
df['bipoc'] = np.where(df['perceivedraceorethnicity'] != 2, 1,0)
np.where(df['bipoc'] == 3, 0,0)
df['report_risk_groups'] = np.where(df['perceivedraceorethnicity'].isin([1,3,4]), 1,0)
df.report_risk_groups[df.report_risk_groups == 3] = 0
df.drop(columns=['perceivedraceorethnicity'], inplace=True)
# print(f'the value counts for risk groups: \n {df.report_risk_groups.value_counts()}\n')
# sys.exit()




df.gender[df.gender == 'Male'] = 1
df.gender[df.gender == 'Female'] = 2
df[~df['gender'].isin([1,2])] = 3
# print(f'the value counts for gender are {df.gender.value_counts()}\n')
# sys.exit('Look it worked!')



df['arrest'] = np.where(df['resultofstop'].str.contains('arrest'), 1,0)
df = df.drop(columns=['resultofstop'])
# print(f'the value counts for arrests are: \n {df.arrest.value_counts()}\n')



df.typeofstop[df.typeofstop == 'Vehicle'] = 1
df.typeofstop[df.typeofstop == 'Pedestrian'] = 2 
df.typeofstop[df.typeofstop == 'Bicycle'] = 3
df['trafficstop'] = np.where(df['typeofstop']==1, 1,0)
df = df.drop(columns=['typeofstop'])




df['raceperceivedpriortostop'] = np.where(df['raceperceivedpriortostop']==True, 1,0)
# print(f'the value counts for race perceived prior are {df.raceperceivedpriortostop.value_counts()}\n')
# sys.exit('Look it worked!')

averagestopduration = round(st.mean(df.durationofstop),2) 
# longer_stopduration = round(st.mean(df.durationofstop),2) + round(st.stdev(df.durationofstop),2)

df['longstop'] = np.where(df['durationofstop'] > averagestopduration, 1,0)
# df['longergstop'] = np.where(df['durationofstop'] > longer_stopduration, 1,0)
df = df[df['durationofstop'] < 270]
# print(df.longstop.value_counts())
# sys.exit('Look it worked!')



# sys.exit('first part works!')
    
    

    
    
    
    
    
    
    
# #STEP 4/5: SELECT THE MODEL 
# from sklearn.linear_model import LogisticRegression, LinearRegression
# from scipy.special import expit  

# y = df['arrest'].values
# X = df.drop(columns=['arrest'])

# clf = LogisticRegression(C=1e5)
# clf.fit(X, y)

# # and plot the result
# plt.figure(1, figsize=(4, 3))
# plt.clf()
# plt.scatter(X.ravel(), y, color="black", zorder=20)
# X_test = np.linspace(-5, 10, 300)
    
    
    
    
# sys.exit('Did it work?') 
    
    
    
    
    
    
    
    
#STEP 4: PREPARE DEPENDENT VARIABLES & CREATE MODEL
cols = ['black','perceivedage','gender',
         'trafficstop','raceperceivedpriortostop',
         'tract_distancefromcal','tract_medianincome','tract_nonwhitecomp','tract_annualstops']


y = df['arrest']
X = df[cols].astype(int)


df = df[(df['black'] != 3)]
print(f'the val count black is {df.black.value_counts()}')

import statsmodels.api as sm
res = sm.Logit(y,X).fit()
# result=logit_model.fit()
# params = res.get_params(deep=True)
print(res.summary())
print('\n\n',np.exp(res.params))



