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
from .style import *

input_groups = dbc.FormGroup(
    [
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("#", addon_type="prepend"),
                dbc.Input(id="input-hashtag", type="text", placeholder="Hashtag")
            ],
        ),
        html.Br(),
        html.A(
            dbc.Button(
                children='Get Twitter ID',
                color='primary',
                block=True
            ),
            href='http://gettwitterid.com/',
        ),
        html.Br(),
        dbc.InputGroup(
            [
                dbc.Input(id="input-candidate-id", type="number", placeholder="Twitter ID")
            ],
        ),
        html.Br(),
        dbc.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            color='primary',
            block=True
        ),
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        input_groups
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardImg(src="/static/images/placeholder286x180.png", top=True, id='profile-picture'),
            dbc.CardBody([
                html.H5("Username", className="card-title", id='username'),
                html.P("Personal description",
                        className="card-text",
                        id='description', 
                ),
                html.Footer(
                        html.Small("Followers count", id='followers-count', className="text-muted")
                    ),
            ]),
        ]),
        md=4
    ),
    dbc.Col(
            dcc.Graph(id='tweets-evolution'), 
            md=8
    ),
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='bubble-chart'), md=12
        ),
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5("Most retweeted tweet", className="card-title"),
                    html.P("Retweet content",
                            className="card-text",
                            id='tweet-content', 
                    ),
                    html.Footer(
                        html.Small("Created at:", id='tweet-date', className="text-muted")
                    ),
                    html.Footer(
                        html.Small("Rewteets count", id='rt-count', className="text-muted")
                    ),
                    html.Footer(
                        html.Small("Likes count", id='like-count', className="text-muted")
                    ),
                ]),
            ]),
            md=7
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardBody(html.P("Wordcloud image showing the recurring words in tweets related to the hashtag provided in parameter", className="card-text")),
                dbc.CardImg(src="/static/images/placeholder286x180.png", bottom=True, id="wordcloud-img"),
            ]),
            md=5
        )
        
    ]
)

header = html.Div(
    [
        dbc.Row(
            [
            dbc.Col(
                html.H2('Twitter Personality Analytics', style=TEXT_STYLE),
                width=9,
            ),
            dbc.Col(
                html.A(
                    dbc.Button(
                        children='Learn More',
                        color='primary',
                    ),
                    href="https://gitlab.com/grosclara/twitterpredictor",  
                ),
                width=3
            )
            ]
        ),
        html.Hr()
    ]
)

main_content = html.Div([
    html.Br(),
    content_first_row,
    html.Br(),
    content_second_row,
    html.Br(),
    content_third_row,
    html.Br(),
])

footer = html.Div(
    [
        html.Hr(),
        dbc.Row(
            [
            dbc.Col(
                html.H3('Clara Gros, Student at CentraleSupélec', style=TEXT_STYLE),
                width=9,
            ),
            dbc.Col(
                html.H3('Nov 2018', style=TEXT_STYLE),
                width=3,
            ),
            ]
        ),   
    ]
) 

content = html.Div([header, main_content, footer], style = CONTENT_STYLE)