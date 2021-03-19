import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.request as urllib2


app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
server = app.server


def openurl():
    # url = 'https://covid19-visualisation-seb.herokuapp.com/'
    # # url = 'https://www.google.com/'
    # print('opening URL')
    # urllib2.urlopen(url)
    # print('URL loaded')
    pass


def get_new_data():
    """Updates the global variable 'df' with new data"""
    global df
    # df = pd.read_csv('owid-covid-data.csv')
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    print('data loaded')


def get_new_data_every(period=1200):
    """Update the data every 'period' seconds"""
    while True:
        get_new_data()
        openurl()
        time.sleep(period)


get_new_data()
app.layout = html.Div([

    html.Div([

       html.Nav('This is nav')

    ], id='content0'),


    html.Div([

        dcc.Dropdown(
            id='country_selected',
            options=[{'label': i, 'value': i} for i in df['location'].unique()],
            multi=True,
            value=['United Kingdom', 'United States'],
            style={
                'color': 'black',
                'background-color': '#dfdfdf'
            }
        ),

        dcc.Graph(id='feature-graphic',
                  config={'displayModeBar': False}
                  ),

        ], id='content1'),

    html.Div([

        dcc.Dropdown(
            id='country_selected2',
            options=[{'label': i, 'value': i} for i in df['location'].unique()],
            value='United Kingdom',
            style={
                'color': 'black',
                'background-color': '#dfdfdf'
            }
        ),

        dcc.Graph(id='feature-graphic2',
                  config={'displayModeBar': False})

    ], id='content2'),

    html.Div([

        dcc.Graph(id='feature-graphic3',
                  config={'displayModeBar': False})

    ], id='content3'),

    html.Div([
        html.H2("Div under connstruction")
    ], id='content4')


], className='container')


@app.callback(Output('feature-graphic', 'figure'),
              [Input('country_selected', 'value')]
              )
def update_graph1(country_names):
    scatter_list = []
    for i in range(len(country_names)):
        country_df = df[df['location'] == country_names[i]]
        country_vac = country_df.dropna(subset=['total_vaccinations'])
        fig = go.Scatter(x=country_vac['date'],
                         y=country_vac['total_vaccinations_per_hundred'],
                         mode='lines+markers',
                         name=country_names[i],
                         )
        scatter_list.append(fig)

    return {'data': scatter_list,

            'layout': go.Layout(title='Global Vaccinations Data By Country',
                                yaxis={'title': 'Total Vaccinations Per Hundred', 'anchor': 'free', 'position': 0.05},
                                legend={'orientation': 'h',  'yanchor': 'bottom', 'x': 0, 'y': 1},
                                margin=dict(l=5, r=5, t=20, b=30),
                                plot_bgcolor='#bfd8d5',
                                paper_bgcolor='#bfd8d5'
                                )
            }


@app.callback(Output('feature-graphic2', 'figure'),
              [Input('country_selected2', 'value')]
              )
def update_graph2(country_name):
    country_df = df[df['location'] == country_name]
    fig = px.bar(country_df, x='date', y='new_cases')
    fig.update_layout(title={'text': 'Total cases per day', 'y': .85, 'x': .1},
                      xaxis=None, yaxis={'title': 'Daily Cases', 'anchor': 'free', 'position': 0.05},
                      margin=dict(l=5, r=5, t=20, b=20),
                      plot_bgcolor='#bfd8d5',
                      paper_bgcolor='#bfd8d5')

    return fig


@app.callback(Output('feature-graphic3', 'figure'),
              [Input('country_selected2', 'value')]
              )
def update_piechart(country_name):
    selected_country_vac = df[df['location'] == country_name]['total_vaccinations_per_hundred'].max()
    chart_values = [selected_country_vac, 100 - selected_country_vac]
    labels = ['Vaccinated population', 'Non vaccinated population']

    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=chart_values,
                                 title='Vaccinated population percentage')])
    fig.update_layout(plot_bgcolor='#bfd8d5',
                      paper_bgcolor='#bfd8d5',
                      margin=dict(t=30, b=30, l=30, r=30))
    return fig


executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_data_every)

if __name__ == '__main__':
    app.run_server()
