# THIS CODE COMES FROM https://www.pueschel.dev/python,/dash,/plotly/2019/06/28/dash-logs.html

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging
import sys

logger = logging.getLogger(__name__)


class DashLogger(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream=stream)
        self.logs = list()

    def emit(self, record):
        try:
            msg = self.format(record)
            self.logs.append(msg)
            self.logs = self.logs[-1000:]
            self.flush()
        except Exception:
            self.handleError(record)


dash_logger = DashLogger(stream=sys.stdout)
logger.addHandler(dash_logger)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='my-div'),
    html.Button('Submit', id='button'),
    dcc.Interval(
        id='log-update',
        interval=1 * 1000  # in milliseconds
    ),
    html.Div(id='log')
])


@app.callback(
    Output('log', 'children'),
    [Input('log-update', 'n_intervals')])
def update_logs(interval):
    return [html.Div(log) for log in dash_logger.logs]


@app.callback(Output('my-div', 'children'), [Input('button', 'n_clicks')])
def add_log(click):
    logger.warning("Important Message")


if __name__ == '__main__':
    app.run_server(debug=True)