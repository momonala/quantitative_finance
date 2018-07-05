import datetime
import pandas as pd
import numpy as np

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from snp500 import getsp500
import trades


flask_app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server=flask_app)
dash_app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


def get_zscores():
    z_scores = pd.DataFrame(columns=['z_score'])
    for soi in stocks_of_interest:
        df = trades.get_stock_data(soi)
        x = df.iloc[-1]
        u = np.mean(df.iloc[-100:])
        std = np.std(df.iloc[-100:])
        z = (x - u) / std
        z_scores.loc[soi] = z
    return z_scores

# setup dataframes
sp500 = getsp500()
stocks_of_interest = ['fb', 'aapl', 'amzn', 'goog', 'tsla', 'nvda',
                      'msft', 'amrs', 'lulu', 'swks', 'voo', 'nflx', 'amd']
all_stocks = sp500 + stocks_of_interest
metadata = pd.read_csv('data/company_metadata.csv')
all_params = pd.read_csv('data/tuned_params.csv')
z_scores = get_zscores()

# markings for threshold sliders
points_to_mark = list(np.linspace(-5, 5, 21))
marks = {int(i) if i % 1 == 0 else i: '{}'.format(i) for i in points_to_mark}
base_layout = {
    # 'titlefont': dict(color='#aaaaaa', size='14'),
    # 'plot_bgcolor': "#191A1A",
    # 'paper_bgcolor': "#020202"
}


# build the interactive inputs and skeleton of the app
dash_app.layout = html.Div(children=[
    html.Div(children=''' Symbol to graph: '''),
    dcc.Input(id='stock_name', value='', type='text'),
    html.Div(
        [
            html.Label('Threshold Range',
                       id='thresh-range-label'),
            dcc.RangeSlider(
                id='thresh_slider',
                min=-5., max=5.,
                step=None,
                marks=marks,
                value=[-2.5, 2.5],
            ),
        ],
        style={'margin-top': '20'}
    ),
    html.Div([
        html.Div(
            id='stock_graph',
            className='nine columns',
            style={'margin-top': '40'}),
        html.Div(
            id='stock_graph2',
            className='three columns',
            style={'margin-top': '40'}),
    ]),
    html.Div(id='param_data', style={'margin-top': '10', 'margin-left': '200'}),
])


@dash_app.callback(
    output=Output('param_data', 'children'),
    inputs=[Input('stock_name', 'value')]
)
def update_table(ticker):
    """ Build the Table of data about the stock buy
    Args:
        ticker (str): stock name to analyze
    """
    if ticker == '' or ticker not in all_stocks:
        return ''

    params = all_params[all_params.SOI == ticker]

    return [
        html.H4('Precomputed Values'),
        html.Table(
            # Header
            [html.Tr([html.Th(col) for col in params.columns[2:]])] +

            # Body
            [html.Tr([html.Td(params.iloc[0][col]) for col in params.columns[2:]])]
        )
    ]


@dash_app.callback(
    output=Output('stock_graph', 'children'),
    inputs=[Input('thresh_slider', 'value'),
            Input('stock_name', 'value')]
    )
def update_graph(band_range, ticker):
    """ Build the graph. Compute bollinger bars and plot.
    Args:
        band_range (tuple): bounds for bollinger bars
        ticker (str): stock to plot
    """
    ticker = ticker.lower()
    band_range = [float(x) for x in band_range]

    # some exception handling for non-valid tickers
    if ticker == '':
        return None
    if ticker not in all_stocks:
        return 'no stock data for "{}" '.format(ticker)

    name = metadata[metadata.Ticker == ticker.upper()].Name.values[0]

    df = trades.get_stock_data(ticker)
    params = all_params[all_params.SOI == ticker]
    low = trades.compute_band(df, band_range[0], int(params.window_size))
    high = trades.compute_band(df, band_range[1], int(params.window_size))

    layout = base_layout.copy()
    layout.update({'title': '{}  {}'.format(ticker.upper(), name)})

    return dcc.Graph(
        id='ex-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df, 'type': 'line', 'name': ticker},
                {'x': df.index, 'y': high, 'type': 'line', 'name': 'upper Z {}'.format(band_range[1])},
                {'x': df.index, 'y': low, 'type': 'line', 'name': 'lower Z {}'.format(band_range[0])},
            ],
            'layout': layout
        }
    )


@dash_app.callback(
    output=Output('stock_graph2', 'children'),
    inputs=[Input('stock_name', 'value')]
)
def z_score_graph(value):
    """ Build the graph for z_scores. """

    return dcc.Graph(
        id='stock_graph2',
        figure={
            'data': [
                {
                    'x': np.random.random(z_scores.shape[0]) - 0.5,
                    'y': z_scores.z_score.values,
                    'text': z_scores.index,
                    'mode': 'markers+text',
                    'textposition': 'bottom',
                    'showgrid': False,
                    'marker': {'size': 12},
                }

            ],
            'layout': {
                'title': 'Current Z-Scores',
                'yaxis': {
                    'title': 'Z-Scores'
                },
                'x_axis': {
                    'showgrid': False,
                    'zeroline': False,
                    'showline': False,
                    'showticklabels': False,
                    'ticks': False
                }
            }
        }
    )


if __name__ == '__main__':
    dash_app.run_server(debug=True)
