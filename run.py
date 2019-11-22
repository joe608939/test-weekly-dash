


# -*- coding: utf-8 -*-


import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from collections import Counter
from collections import OrderedDict
from operator import itemgetter  

data = pd.read_csv('https://storage.googleapis.com/search-tool-259006.appspot.com/WeeklyAllTextCleaned-utf8.csv')
author_data = pd.read_csv('https://raw.githubusercontent.com/joe608939/test/master/(Draft)%20HKLit%20Author%20list%202019_v.6_20190920.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


full_name_list = []
for i in range(0, author_data.shape[0]):
    name = list(author_data.iloc[i]['Be Known as ':])
    name = [str(x) for x in name if str(x) != 'nan' and str(x) != 'same as column 1']
    full_name_list.append(name)


nameList = list(author_data['Be Known as '])
year_list = list(set((list(data['Search_date']))))

year_list = [str(x) for x in year_list if str(x) != 'nan']
yearList = []
for i in range(0,len(year_list)):
    yearList.append(year_list[i][(year_list[i].rfind('/')) + 1 :])
yearList = list(set(yearList))
yearList.sort(reverse = False) 


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': v, 'value': v} for v in yearList
        ],
        value='1952'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='dd-output-container',

            )
        ], className="Columnn"),
    ],className="row")
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(input_value):
    temp_df = data[data['Search_date'].str.contains(input_value, na = False)]
    name_list_from_temp_df = list(temp_df['Creator'])
    temp_dict = {}
    for i in range(0, len(full_name_list)):
        count = 0
        for element in name_list_from_temp_df:
            if element in full_name_list[i]:
                count = count + 1
        if count > 0:
            temp_dict[full_name_list[i][0]] = count
    A = dict(Counter(temp_dict).most_common(5))
    temp_data = []
    x = []
    y = []
    for key in A:
        x.append(key)
        y.append(A[key])
    # Use textposition='auto' for direct text
    trace_close = go.Bar(
                x=x, y=y,
                text=y,
                textposition='auto',
            )
    temp_data.append(trace_close)
    return {
        "data":temp_data
    }


if __name__ == '__main__':
    app.run_server(debug=False)






