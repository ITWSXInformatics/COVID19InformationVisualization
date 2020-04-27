from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
import state_code
from state_code import SAMPLE
import collections
import plotly.graph_objects as go
import plotly.express as px


files = os.listdir('./us_dataset/')
files.sort()
output_df = []
entire = pd.DataFrame(columns=['code','state','total_confirmed', 'death', 'recovered','testing_rate', 'hosp_rate', 'mortality_rate', 'date'])
number = 1
for i in files:
    #print(i)
    total = {}
    raw_df = pd.read_csv('./us_dataset/'+i).fillna(0)

    country = 'Country_Region'
    state = 'Province_State'
    check = raw_df[country] == 'US'
    df = raw_df[check]

    for _, row in df.iterrows():
        us_state = row[state]
        if us_state not in state_code.CODE:
            #print(us_state)
            continue
        #print(row[state],i)
        if us_state in total:
            #print(total[temp])
            total[us_state][0] += row['Confirmed']
            total[us_state][1] += row['Deaths']
            total[us_state][2] += row['Recovered']
            total[us_state][3] += row['Testing_Rate']
            total[us_state][3] += row['Hospitalization_Rate']
            total[us_state][3] += row['Mortality_Rate']
        else:
            total[us_state] = [row['Confirmed'],row['Deaths'], row['Recovered'], row['Testing_Rate'], row['Hospitalization_Rate'], row['Mortality_Rate']]
            
    usa_df = pd.DataFrame(columns=['code','state','total_confirmed', 'death', 'recovered','testing_rate', 'hosp_rate', 'mortality_rate', 'date'])


    for j in total:
        a_row = [state_code.CODE[j], j]+total[j] + [i[:10]]
        leng = len(entire)
        #usa_df.loc[leng] = a_row
        entire.loc[leng] = a_row
        #row_df = pd.DataFrame([a_row])
        # usa_df = usa_df.append(a_row, ignore_index=True)
    number += 1
    #print(usa_df)
    output_df.append(usa_df.fillna(0))



entire["total_confirmed"] = pd.to_numeric(entire.total_confirmed, errors='coerce')
entire["death"]= pd.to_numeric(entire.death, errors='coerce')
#print(entire.dtypes)
fig = px.choropleth(entire,  locations='code', scope='usa', color='hosp_rate',
color_continuous_scale = px.colors.sequential.Reds, locationmode="USA-states", hover_name='hosp_rate', animation_frame='date')
fig.show()
