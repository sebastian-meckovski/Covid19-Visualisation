import copy
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
    html.Nav([
        html.Div("Covid-19 global data Dashboard", className="dashboard-title"),
        html.A(
            id="toggle-button",
            children=[
                html.Span(className="bar"),
                html.Span(className="bar"),
                html.Span(className="bar"),
                ],
            href="#",
            className="toggle-button"),
        html.Div(
            id="navbar-links",
            children=html.Ul(
                children=[
                    html.Li(html.A("Home", href="#")),
                    html.Li(html.A('Source Code', href="#", )),
                    html.Li(html.A("CSV Data", href="#"))]),
            className="navbar-links active"
        )],
        className="navbar"),

    html.Div([


        html.Div([
                    dcc.Dropdown(
                        id='country_selected',
                        options=[{'label': i, 'value': i} for i in df['location'].unique()],
                        multi=True,
                        value=['United Kingdom', 'United States'],
                        style=dropdown_style
                    ),
        ], id='dropdown2'),

        html.Div([

            dcc.Graph(id='feature-graphic1',
                      config=static_config,
                      style=style
                      )], id='graph1'),

        html.Div([
            dcc.Graph(id='feature-graphic-2nd-dose',
                      config=static_config,
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
        ], id='dropdown1'),

        html.Div([

            dcc.Graph(id='feature-graphic2',
                      config=static_config),

            dcc.Graph(id='feature-graphic7',
                      config=static_config),

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
                      config=static_config)
        ], id="graph5"),

        html.Div([
            dcc.Graph(id='feature-graphic6',
                      style={'height': 395, **style},
                      config=static_config),
        ], id="graph6"),

        html.Div([
            dcc.Input(id='empty-field',
                      style={'display': 'none'})
        ]),

        ], className='container-grid'),

    html.Footer([
        html.Div("created by Sebastian Meckovski", id='footer-text'),

        html.Div([
            html.P(['Find Me On:'], id='find-me-on'),
            html.A([html.Img(src=app.get_asset_url('linkedInLogo.png'), style={'height': '2rem'})], href='#'),
            html.A([html.Img(src=app.get_asset_url('facebookLogo.png'), style={'height': '2rem'})], href='#')
        ], id='footer-links'),

    ], id='footer'),

], className='container')

layout_settings = go.Layout(yaxis={'anchor': 'free', 'position': 0.05,
                                   'ticksuffix': '%'},
                            legend=legend_style,
                            title={'yanchor': 'auto', 'text': 'People with at least 1st dose', 'y': .99, 'x': .062},
                            margin=dict(l=5, r=5, t=20, b=30),
                            plot_bgcolor='#bfd8d5',
                            paper_bgcolor='#bfd8d5')

layout_settings2 = copy.deepcopy(layout_settings)
layout_settings2['title']['text'] = 'Fully vaccinated'


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
           {'data': scatter_list_2st_vacc, 'layout': layout_settings2}


@app.callback(Output('feature-graphic2', 'figure'),
              Output('feature-graphic7', 'figure'),
              [Input('country_selected2', 'value'),
               Input('slider2', 'value')])
def update_graph2(country_name, date_range):
    country_df_bar = df[(df['location'] == country_name) & (df['date'] >= unix_to_date(date_range[0])) &
                        (df['date'] <= unix_to_date(date_range[1]))]
    country_df_sca = df[(df['location'] == country_name) & (df['date'] >= unix_to_date(date_range[0])) &
                        (df['date'] <= unix_to_date(date_range[1]))]

    country_df_sca['new_cases'] = country_df_sca['new_cases'].rolling(window=7).mean()
    country_df_sca['new_cases'] = country_df_sca['new_cases'].iloc[::2]  # warning needs handling

    country_df_sca['new_deaths'] = country_df_sca['new_deaths'].rolling(window=7).mean()
    country_df_sca['new_deaths'] = country_df_sca['new_deaths'].iloc[::2]  # warning needs handling

    country_df_sca = country_df_sca.dropna(subset=['new_cases'])

    fig = go.Figure(layout=go.Layout(height=350)) # need to check if there is a better way of putting it

    fig.add_trace(
        go.Scatter(x=country_df_sca['date'], y=country_df_sca['new_cases'],
                   line=dict(color='#d1621d', width=4, dash='dot'), showlegend=True, mode="lines",
                   name='7-day average')
    )

    fig.add_trace(
        go.Bar(x=country_df_bar['date'], y=country_df_bar['new_cases'], showlegend=True,
               name='Daily Cases')
    )

    fig.update_layout(title={'text': 'Total cases per day', 'y': .99, 'x': .99},
                      # xaxis=None, yaxis=None,
                      margin=dict(l=5, r=5, t=20, b=20),
                      plot_bgcolor='#bfd8d5',
                      paper_bgcolor='#bfd8d5',
                      legend={**legend_style, 'y': .98, 'x': 1.01}
                      )

    fig.update_traces(marker_color=bar_color)
    fig.update_yaxes(gridcolor='#9db0ae', zerolinecolor='#9db0ae')

    fig2 = copy.deepcopy(fig)
    fig2['data'][0]['y'] = country_df_sca['new_deaths']
    fig2['data'][0]['line']['color'] = 'red'
    fig2['data'][1]['y'] = country_df_bar['new_deaths']
    fig2['layout']['title']['text'] = 'Total deaths per day'

    return fig, fig2


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

    fig.update_layout(title={'text': 'Vaccinated Population Breakdown ', **title_style_middle},
                      plot_bgcolor='#bfd8d5',
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

    fig.update_layout(xaxis=bar_chart_style,
                      yaxis=bar_chart_style,
                      margin=dict(l=0, r=0, t=0, b=0),
                      plot_bgcolor='#bfd8d5',
                      title={'text': 'New cases last 30 days', **title_style_middle}
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

    fig.update_layout(title={'text': 'New deaths last 30 days', **title_style_middle},
                      xaxis=bar_chart_style,
                      yaxis=bar_chart_style,
                      margin=dict(l=0, r=0, t=0, b=0),
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


@app.callback(
    Output("navbar-links", "className"),
    Input("toggle-button", "n_clicks"),
    State("navbar-links", "className"),
    prevent_initial_call=True,
)
def callback(n_clicks, current_classes):
    base_class = "navbar-links"
    if "active" in current_classes:
        return base_class
    return base_class + " active"


executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_data_every)

if __name__ == '__main__':
    app.run_server()
