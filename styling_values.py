BrownGrey = '#ac9592'
LightBrown = '#dbba3'
SandBrown = '#e3d0c3'
Grey = '#eeeceb'
DarkSkyeBlue = '#c6d7da'
DarkSkyeBlueDarker = '#bdd5ff'
LightBlue = '#cfe0ff'
DarkBlueBars = '#2b66fc'
DarkBlueHover = '#87b3ff'
DarkBlue = '#5493ff'

linkedInURL = 'https://www.linkedin.com/in/sebastian-meckovski'
facebookURL = 'https://www.facebook.com/sebastian.meckovski/'
homeURL = 'https://sebastian-meckovski.github.io/seb_website_portfilio/'
sourceCodeURL = 'https://github.com/sebastian-meckovski/Covid19-visualisation'
sourceDataURL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

style = {
    'border': DarkBlueHover + ' solid 2px',
    'border-radius': '10px',
    'background-color': DarkSkyeBlueDarker,
    'padding': '3px'
}

dropdown_style = {
    'color': 'black',
    'background-color': DarkSkyeBlueDarker,
    'border-radius': '10px',
}

legend_style = {'orientation': 'v', 'xanchor': 'auto',
                'yanchor': 'auto', 'x': 0.055, 'y': .99,
                'bgcolor': DarkSkyeBlueDarker, 'bordercolor': DarkBlueHover,
                'borderwidth': 2}

plotPaperBgColor = {'plot_bgcolor': DarkSkyeBlueDarker, 'paper_bgcolor': DarkSkyeBlueDarker}

bar_color = DarkBlueBars

title_style_middle = {'y': 1, 'x': .5}

bar_chart_style = dict(showgrid=False, showticklabels=False, title=None)

static_config = {'displayModeBar': False,
                 'staticPlot': True}
