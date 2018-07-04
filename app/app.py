import datetime
import pandas as pd
import numpy as np
import pandas_datareader.data as web

import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from snp500 import getsp500


flask_app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server=flask_app)
dash_app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# a bit of setup
sp500 = getsp500()  # list of tickers
extras = ['tsla', 'yelp', 'lulu']
all_stocks = sp500 + extras
metadata = pd.read_csv('data/company_metadata.csv')
all_params = pd.read_csv('data/tuned_params.csv')
points_to_mark = list(np.linspace(-5, 5, 21))   
marks = {int(i) if i % 1 == 0 else i: '{}'.format(i) for i in points_to_mark}


@server.route('/hello')
def hello():
    return 'Hello, World!'

def get_stock_data(ticker):
    ''' get data from web directly'''
    start = datetime.datetime(2012, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(ticker, 'morningstar', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    df = df.drop("Symbol", axis=1)
    return df.Close


def compute_band(s, factor, window):
    '''compute a bollinger band'''
    mean_ = s.rolling(window).mean()
    std_ = s.rolling(window).std()
    return mean_ + std_ * factor

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
                                 min=-5.,
                                 max=5.,
                                 step=None,
                                 marks=marks,
                                 value=[-2.5, 2.5],
                             ),
                         ],
                         style={'margin-top': '20'}
                     ),

                html.Div(id='output-graph'),
                html.Div(id='param_data', style={'margin-top': '10,',
                                                 'margin-left': '200'})
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

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in params.columns[2:]])] +

        # Body
        [html.Tr([
            html.Td(params.iloc[0][col]) for col in params.columns[2:]
        ])]
    )


@dash_app.callback(
    output=Output('output-graph', 'children'),
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

    df = get_stock_data(ticker)
    params = all_params[all_params.SOI == ticker]
    low = compute_band(df, band_range[0], int(params.window_size))
    high = compute_band(df, band_range[1], int(params.window_size))

    return dcc.Graph(
        id='ex-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df, 'type': 'line', 'name': ticker},
                {'x': df.index, 'y': high, 'type': 'line', 'name': 'upper Z {}'.format(band_range[1])},
                {'x': df.index, 'y': low, 'type': 'line', 'name': 'lower Z {}'.format(band_range[0])},
            ],
            'layout': {
                'title': '{}  {}'.format(ticker.upper(), name)
            }
        }
    )


if __name__ == '__main__':
    dash_app.run_server(debug=True)
