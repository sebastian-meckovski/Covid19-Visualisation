import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('owid-covid-data.csv')

dict_comprehension = [{'label': i, 'value': str(i)}for i in df['location'].unique()]

app.layout = html.Div([

    dcc.Dropdown(
        id='country_selected',
        options=[{'label': i, 'value': i}for i in df['location'].unique()],
        multi=True,
        value=['United Kingdom', 'United States'],
        style={'margin-bottom': '10px'}
    ),

    dcc.Graph(id='feature-graphic')

])


@app.callback(Output('feature-graphic', 'figure'),
              [Input('country_selected', 'value')]
              )
def update_graph(country_names):
    scatter_list = []
    for i in range(len(country_names)):
        country_df = df[df['location'] == country_names[i]]
        country_vac = country_df.dropna(subset=['total_vaccinations'])
        temp = go.Scatter(x=country_vac['date'],
                          y=country_vac['total_vaccinations'],
                          mode='lines+markers',
                          name=country_names[i])
        scatter_list.append(temp)

    return {'data': scatter_list,

            'layout': go.Layout(title='Global Vaccinations Data By Country',
                                xaxis={'title': 'Date'},
                                yaxis={'title': 'Total Vaccinations to date'}
                                )
            }


if __name__ == '__main__':
    app.run_server()
