# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from io import BytesIO
import base64
import io
import plotly.graph_objs as go
import re
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from tweet_collection.tweet_collect import *
from tweet_collection.twitter_connection_setup import *
from tweet_analysis.tweet_analyze import *
import dash_bootstrap_components as dbc
from layout import *

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([sidebar, content])

if __name__ == '__main__':
    app.run_server(debug=True)