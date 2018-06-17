import pandas_datareader.data as web
import datetime
import pandas as pd 
import numpy as np 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

all_stocks = pd.read_csv('../data/quandl.csv')
all_stocks.index = pd.DatetimeIndex(all_stocks.date)
metadata = pd.read_csv('../data/company_metadata.csv')
all_params = pd.read_csv('../data/tuned_params.csv')


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
    return mean_ + std_*factor


# build the interactive inputs 
app.layout =html.Div(children=[
                html.Div(children=''' Symbol to graph: '''),
                dcc.Input(id='stock_name', value='', type='text'),
                
               html.Div(
                        [
                            html.Label('Threshold Range', id='thresh-range-label'),
                            dcc.RangeSlider(
                                id='thresh_slider',
                                min=-50.,
                                max=50.,
                                value=[-25., 25.], 
                                # marks = np.linspace(-50, 50, 101)
                            ),
                        ],
                        style={'margin-top': '20'}
                    ),
                
                html.Div(id='output-graph'),

                html.Div(id='param_data', style={'margin-top': '10,',
                                                 'margin-left' : '200'})
            ])


# build the table with parmas / metadata 
@app.callback(
    output=Output('param_data', 'children'),
    inputs=[Input('stock_name', 'value')]
    )
def update_value(input_data):
    if input_data == '' or  input_data not in all_stocks.columns: 
        return ''

    params = all_params[all_params.SOI == input_data]
    
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in params.columns[2:]])] +

        # Body
        [html.Tr([
            html.Td(params.iloc[0][col]) for col in params.columns[2:]
        ])]
    )


# build the graph 
@app.callback(
    output=Output('output-graph', 'children'),
    inputs=[Input('thresh_slider', 'value'),
            Input('stock_name', 'value')]
    )
def update_value(band_range, input_data):
    input_data = input_data.lower()
    band_range = [float(x)/10 for x in band_range]

    # some exception handling for non-valid tickers 
    if input_data == '': 
        return None
    if input_data not in all_stocks.columns: 
        return 'no stock data for "{}" '.format(input_data) 

    name = metadata[metadata.Ticker == input_data.upper()].Name.values[0]
    
    # use stored data
    # df = all_stocks.loc[:, input_data].dropna()

    df = get_stock_data(input_data)
    params = all_params[all_params.SOI == input_data]
    low, high = [compute_band(df, x, int(params.window_size)) for x in band_range]
    
    return dcc.Graph(
        id='ex-graph', 
        figure={
            'data': [
                {'x': df.index, 'y': df, 'type': 'line', 'name': input_data},
                {'x': df.index, 'y': high, 'type': 'line', 'name': 'upper Z {}'.format(band_range[1])},
                {'x': df.index, 'y': low, 'type': 'line', 'name': 'lower Z {}'.format(band_range[0])},
            ],
            'layout': {
                'title': '{}  {}'.format(input_data.upper(), name)
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
