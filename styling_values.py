BrownGrey = '#ac9592'
LightBrown = '#dbba3'
SandBrown = '#e3d0c3'
Grey = '#eeeceb'
DarkSkyeBlue = '#c6d7da'
DarkSkyeBlueDarker = '#bdd5ff'
LightBlue = '#cfe0ff'
DarkBlueBars = '#2b66fc'
DarkBlueHover = '#87b3ff'

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
