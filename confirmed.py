from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import os
import state_code
from state_code import SAMPLE
import collections
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

files = os.listdir('./dataset/')
files.sort()

biggest_con = 0

def set_color_group(item):
    #print(lst)
    pop = int(item)
    [1000, 5000, 10000, 50000]
    if pop <= 0:
        return 0
    elif pop < 1000:
        return 1
    elif 1000 <= pop < 5000:
        return 2
    elif 5000 <= pop < 10000:
        return 3
    elif 10000 <= pop < 50000:
        return 4
    else:
        return 5
    

entire =  pd.DataFrame(columns=['code','state','total_confirmed','color_code', 'date'])
#output_df = []
for i in files:
    #print(i)
    total = {}
    raw_df = pd.read_csv('./dataset/'+i).fillna(0)
    country = [col for col in raw_df.columns if 'Country' in col][0]
    state = [col for col in raw_df.columns if 'Province' in col][0]
    check = raw_df[country] == 'US'
    df = raw_df[check]

    for _, row in df.iterrows():
        us_state = row[state].split(',')[0]
        if us_state not in state_code.CODE:
            if len(row[state].split(',')) < 2 or len((row[state].split(',')[1]).split(' ')[1]) < 2:
                continue
            s_code = (row[state].split(',')[1]).split(' ')[1]
            if s_code in state_code.CODE_R:
                us_state = state_code.CODE_R[s_code]
            else:
                print(row[state])
                continue
        #print(row[state],i)
        if us_state in total:
            #print(total[temp])
            total[us_state][0] += row['Confirmed']
            total[us_state][1] += row['Deaths']
            total[us_state][2] += row['Recovered']
        else:
            total[us_state] = [row['Confirmed'], row['Deaths'], row['Recovered']]
            #total[row[state]][3] += row['Active']
    #print(total)
    #usa_df = pd.DataFrame(columns=['code','total_confirmed','total_death','total_recovered','date'])
    #usa_df = pd.DataFrame(columns=['code','state','total_confirmed','color_code', 'date'])

    # total two-d array total[0] = [number_confirmed, number_death, number_ recovered]
    #wtf
    for j in total:
        item = total[j][0]
        biggest_con = max(biggest_con, total[j][0])
        a_row = [state_code.CODE[j], j]+[str(int(item))]+[set_color_group(item)]+ [i[:10][:5]]
        leng = len(entire)
        entire.loc[leng] = a_row
        #usa_df.loc[leng] = a_row
        #row_df = pd.DataFrame([a_row])
        # usa_df = usa_df.append(a_row, ignore_index=True)
    #print(usa_df)
    #output_df.append(usa_df.fillna(0))

#print(entire.dtypes)
entire['total_confirmed'] = pd.to_numeric(entire.total_confirmed, errors='coerce')
entire['color_code'] = pd.to_numeric(entire.color_code, errors='coerce')
fig = px.choropleth(entire,  locations='code', scope='usa', color='color_code',range_color=[0,6], title= 'COVID-19 USA Data Visualization',
            color_continuous_scale = px.colors.sequential.Reds, locationmode="USA-states", hover_name='total_confirmed', animation_frame='date')
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 250
fig.layout.coloraxis['colorbar'] = dict(
        title = {'text':'Poplulation'},
        tickvals=[1, 2, 3, 4, 5, 6],
        ticktext=["1000", "5000", "10000", "50000", "100000"]+[str(biggest_con)])
fig.show()