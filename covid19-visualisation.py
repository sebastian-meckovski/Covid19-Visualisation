import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import datetime as dt
import time as t
from concurrent.futures import ThreadPoolExecutor
import urllib.request as urllib2
from styling_values import *


app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )
server = app.server


def openurl():
    """this function will send a request to 'url' and do nothing after that"""
    url = 'https://covid19-visualisation-seb.herokuapp.com/'
    # url = 'https://www.google.com/'
    urllib2.urlopen(url)
    pass


def get_new_data():
    """Updates the global variable 'df' with new data"""
    global df, date_min_vac, date_max_vac, date_min_cases, date_max_cases
    # df = pd.read_csv('owid-covid-data.csv')
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    df['new_cases'] = df['new_cases'].abs()
    df['new_deaths'] = df['new_deaths'].abs()
    date_min_vac = df[(df['date'] >= '') & (df['people_vaccinated_per_hundred'])]['date'].min()
    date_max_vac = df[(df['date'] >= '') & (df['people_vaccinated_per_hundred'])]['date'].max()
    date_min_cases = df[(df['date'] >= '') & (df['total_cases'])]['date'].min()
    date_max_cases = df[(df['date'] >= '') & (df['total_cases'])]['date'].max()

    print('data loaded')


def get_new_data_every(period=1200):
    """Update the data every 'period' seconds"""
    while True:
        get_new_data()
        openurl()
        t.sleep(period)


def date_to_unix(date_arg):
    """convert date string into datetime object"""
    date_arg = dt.datetime.strptime(date_arg, "%Y-%m-%d").timetuple()
    date_arg = t.mktime(date_arg)
    return date_arg


def unix_to_date(unix):
    """This function will convert datetime object to unix timestamp"""
    return str(dt.datetime.fromtimestamp(unix).date())


def create_steps(date_min_arg, date_max_arg):
    """This function will return a dictionary containing X dates split across even intervals"""
    length_in_sec = date_max_arg - date_min_arg
    intervals = 5
    step = length_in_sec/intervals

    day_steps = {int(date_min_arg + step * interval): {'label': unix_to_date(date_min_arg + step * interval),
                                                       'style': {'font-size': '10px'}}
                 for interval in range(0, intervals + 1)}
    return day_steps


get_new_data()

app.layout = html.Div([

    html.Div([

       html.Nav('Covid-19 global data Dashboard')

    ], id='navbar'),

    html.Div([
                dcc.Dropdown(
                    id='country_selected',
                    options=[{'label': i, 'value': i} for i in df['location'].unique()],
                    multi=True,
                    value=['United Kingdom', 'United States'],
                    style=dropdown_style
                ),
    ], id='dropdown1'),

    html.Div([

        dcc.Graph(id='feature-graphic1',
                  config={'displayModeBar': False,
                          'staticPlot': True},
                  style=style
                  )], id='graph1'),

    html.Div([
        dcc.Graph(id='feature-graphic-2nd-dose',
                  config={'displayModeBar': False,
                          'staticPlot': True},
                  style=style
                  )], id='graph2'),

    html.Div([
        dcc.RangeSlider(id='slider',
                        step=1
                        )
    ], id='slider1'),

    html.Div([

        dcc.Dropdown(
            id='country_selected2',
            options=[{'label': i, 'value': i} for i in df['location'].unique()],
            value='United Kingdom',
            style=dropdown_style)
    ], id='dropdown2'),
    
    html.Div([

        dcc.Graph(id='feature-graphic2',
                  config={'displayModeBar': False,
                          'staticPlot': True}),
        dcc.RangeSlider(
            id='slider2')
    ], id='graph3', style=style),

    html.Div([

        dcc.Graph(id='feature-graphic4',
                  config={'displayModeBar': False},
                  style={'height': 395, **style},
                  )

    ], id='graph4'),

    html.Div([
        dcc.Graph(id='feature-graphic5',
                  style={'height': 395, **style},
                  config={'displayModeBar': False, 'staticPlot': True})
    ], id="graph5"),

    html.Div([
        dcc.Graph(id='feature-graphic6',
                  style={'height': 395, **style},
                  config={'displayModeBar': False, 'staticPlot': True}),
    ], id="graph6"),

    html.Div([
        html.H2("page under construction")
    ], id='footer'),


    html.Div([
        dcc.Input(id='empty-field',
                  style={'display': 'none'})
    ]),




], className='container')

layout_settings = go.Layout(yaxis={'anchor': 'free', 'position': 0.05,
                                   'ticksuffix': '%'},
                            legend={'orientation': 'v',  'yanchor': 'top', 'x': 0.055, 'y': 0.96,
                                    'bgcolor': "#d8e7e5", 'bordercolor': "#859795", 'borderwidth': 2,
                                    },
                            margin=dict(l=5, r=5, t=20, b=30),
                            plot_bgcolor='#bfd8d5',
                            paper_bgcolor='#bfd8d5')


@app.callback(
        Output('feature-graphic1', 'figure'),
        Output('feature-graphic-2nd-dose', 'figure'),
        Input('country_selected', 'value'),
        Input('slider', 'value'))
def update_graph1(country_names, date_range):
    scatter_list_1st_vacc = []
    scatter_list_2st_vacc = []
    for i in range(len(country_names)):
        country_df = df[(df['location'] == country_names[i]) & (df['date'] >= unix_to_date(date_range[0])) &
                        (df['date'] <= unix_to_date(date_range[1]))]
        country_df = country_df.dropna(subset=['people_vaccinated_per_hundred'])
        fig1 = go.Scatter(x=country_df['date'],
                          y=country_df['people_vaccinated_per_hundred'],
                          mode='lines+markers',
                          name=country_names[i],
                          )

        fig2 = go.Scatter(x=country_df['date'],
                          y=country_df['people_fully_vaccinated_per_hundred'],
                          mode='lines+markers',
                          name=country_names[i],
                          )

        scatter_list_1st_vacc.append(fig1)
        scatter_list_2st_vacc.append(fig2)

    return {'data': scatter_list_1st_vacc, 'layout': layout_settings},\
           {'data': scatter_list_2st_vacc, 'layout': layout_settings}


@app.callback(Output('feature-graphic2', 'figure'),
              [Input('country_selected2', 'value'),
               Input('slider2', 'value')])
def update_graph2(country_name, date_range):
    country_df_bar = df[(df['location'] == country_name) & (df['date'] >= unix_to_date(date_range[0])) &
                        (df['date'] <= unix_to_date(date_range[1]))]
    country_df_sca = df[(df['location'] == country_name) & (df['date'] >= unix_to_date(date_range[0])) &
                        (df['date'] <= unix_to_date(date_range[1]))]

    country_df_sca['new_cases'] = country_df_sca['new_cases'].rolling(window=7).mean()
    country_df_sca['new_cases'] = country_df_sca['new_cases'].iloc[::2]  # warning needs handling

    country_df_sca = country_df_sca.dropna(subset=['new_cases'])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=country_df_sca['date'], y=country_df_sca['new_cases'],
                   line=dict(color='red', width=4, dash='dot'), showlegend=False, mode="lines")
    )

    fig.add_trace(
        go.Bar(x=country_df_bar['date'], y=country_df_bar['new_cases'], showlegend=False)
    )

    fig.update_layout(title={'text': 'Total cases per day', 'y': .9, 'x': .05},
                      xaxis=None, yaxis=None,
                      margin=dict(l=5, r=5, t=20, b=20),
                      plot_bgcolor='#bfd8d5',
                      paper_bgcolor='#bfd8d5',
                      )
    fig.update_traces(marker_color=bar_color)
    fig.update_yaxes(gridcolor='#9db0ae', zerolinecolor='#9db0ae')

    return fig


@app.callback(Output('feature-graphic4', 'figure'),
              [Input('country_selected2', 'value')])
def update_piechart(country_name):
    current_country = df[df['location'] == country_name]

    max_1vac = current_country['people_vaccinated_per_hundred'].max()
    max_2vac = current_country['people_fully_vaccinated_per_hundred'].max()

    chart_values = [100 - max_1vac, max_1vac - max_2vac, max_2vac]
    labels = ['Not vaccinated', 'First Dose', 'Fully Vaccinated']

    fig = go.Figure(go.Pie(labels=labels,
                           hole=.43,
                           values=chart_values,
                           textinfo='label+percent',
                           showlegend=False,
                           hoverinfo='skip'
                           ))

    fig.update_layout(plot_bgcolor='#bfd8d5',
                      paper_bgcolor='#bfd8d5',
                      margin=dict(t=15, b=15, l=15, r=15))
    return fig


@app.callback(Output('slider', 'min'),
              Output('slider', 'max'),
              Output('slider', 'marks'),
              Output('slider', 'value'),
              [Input('empty-field', 'value')])
def update_slider(empty_value):
    min_arg = date_to_unix(date_min_vac),
    max_arg = date_to_unix(date_max_vac),
    marks = create_steps(date_to_unix(date_min_vac), date_to_unix(date_max_vac)),
    value = [date_to_unix(date_min_vac), date_to_unix(date_max_vac)],
    empty_value = None
    print('values updated from update slider function')
    return min_arg[0], max_arg[0], marks[0], value[0]


@app.callback(Output('slider2', 'min'),
              Output('slider2', 'max'),
              Output('slider2', 'marks'),
              Output('slider2', 'value'),
              [Input('empty-field', 'value')])
def update_slider2(empty_value):
    min_arg = date_to_unix(date_min_cases),
    max_arg = date_to_unix(date_max_cases),
    marks = create_steps(date_to_unix(date_min_cases), date_to_unix(date_max_cases)),
    value = [date_to_unix(date_max_cases)-31536000, date_to_unix(date_max_cases)],
    empty_value = None
    print('values updated from update slider function')
    return min_arg[0], max_arg[0], marks[0], value[0]


@app.callback(Output('feature-graphic5', 'figure'),
              [Input('country_selected2', 'value')])
def update_graph5(country_name):
    print(country_name)
    country_df = df[df['location'] == country_name]
    fig = px.bar(country_df.tail(30), x='date', y='new_cases')
    fig.update_traces(marker_color=bar_color)

    fig.update_layout(xaxis=bar_chart_style, yaxis=bar_chart_style, margin=dict(l=0, r=0, t=0, b=0),
                      plot_bgcolor='#bfd8d5'
                      )

    fig.add_trace(go.Indicator(
        mode='number+delta',
        value=country_df.tail(30).iloc[29]['new_cases'],
        delta={'reference': country_df.tail(30).iloc[1]['new_cases'], 'relative': True,
               'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
        number={'font': {'color': '#1f302e'}}
    ))

    return fig


@app.callback(Output('feature-graphic6', 'figure'),
              [Input('country_selected2', 'value')])
def update_graph6(country_name):
    print(country_name)
    country_df = df[df['location'] == country_name]
    fig = px.bar(country_df.tail(30), x='date', y='new_deaths')
    fig.update_traces(marker_color=bar_color)

    fig.update_layout(xaxis=bar_chart_style, yaxis=bar_chart_style, margin=dict(l=0, r=0, t=0, b=0),
                      plot_bgcolor='#bfd8d5'
                      )

    fig.add_trace(go.Indicator(
        mode='number+delta',
        value=country_df.tail(30).iloc[29]['new_deaths'],
        delta={'reference': country_df.tail(30).iloc[1]['new_deaths'], 'relative': True,
               'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
        number={'font': {'color': '#1f302e'}}
    ))

    return fig


executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_data_every)

if __name__ == '__main__':
    app.run_server()
