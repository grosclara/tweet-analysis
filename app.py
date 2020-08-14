# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import base64
import datetime
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)

# Create app layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                    className='two columns',
                ),
                html.Div(
                    [
                        html.H2(
                            'Twitter Predictor',

                        ),
                        html.H4(
                            'Statistics on Twitter personalities',
                        )
                    ],

                    className='eight columns'
                ),
                html.A(
                    html.Button(
                        "Learn More",
                        id="learnMore"

                    ),
                    href="https://gitlab.com/grosclara/twitterpredictor",
                    className="two columns"
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(children='You must upload one file containing hashtags separated by commas and named *hashtags\_candidate\_{ID}.txt* where the ID is the candidate\'s TwitterID'),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    #Link to candidate profile pic
                                    src="https://seeklogo.com/vector-logo/274043/twitter",
                                    id="profile_picture"
                                ),
                                dcc.Markdown(
                                    # Screen Name
                                    children='Screen name',
                                    id="screen_name"
                                ),
                                dcc.Markdown(
                                    # Name starting with @
                                    children='Name',
                                    id="name"
                                ),
                                dcc.Markdown(
                                    # Description
                                    children='Status',
                                    id="description"
                                ),
                                dcc.Markdown(
                                    # Number of followers
                                    children='Followers Count',
                                    id="followers_count"
                                ),
                                html.A(
                                    children="URL profile",
                                    href="https://gitlab.com/grosclara/twitterpredictor",
                                    #className="two columns",
                                    id="link_to_profile"
                                )
                            ],
                            className='pretty_container four columns',
                            id='candidate_info'
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    # Number of followers
                                    children='The tweet with more retweets is:',
                                ),
                                dcc.Markdown(
                                    # Content
                                    children='Content',
                                    id="most_retweeted_tweet_content"
                                ),
                                dcc.Markdown(
                                    # Date
                                    children='Date',
                                    id="most_retweeted_tweet_date"
                                ),
                                dcc.Markdown(
                                    # Number of followers
                                    children='RT',
                                    id="retweet_count"
                                                ),
                                dcc.Markdown(
                                    # Number of followers
                                    children='Likes',
                                    id="favorite_count"
                                )
                            ],
                            className='pretty_container four columns',
                        ),
                        html.Div(
                            [
                                html.Img(
                                    #Link to wordcloud
                                    src="https://seeklogo.com/vector-logo/274043/twitter",
                                    id="wordcloud"
                                )
                            ],
                            className='pretty_container four columns', 
                        )
                    ],
                    className='row'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='statistics_graph')
                            ],
                            className='pretty_container four columns',
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='sentimental_analysis_graph')
                            ],
                            className='pretty_container eight columns',
                        ),
                    ],
                    className="row"
                ),
            ],
            className="row"
        ),
        html.Div(
            [
                html.H2(
                    'Clara Gros, Student at CentraleSupélec',
                ),
                html.H4(
                    'Source: Twitter API',
                )
            ],
            className='eight columns'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)

@app.callback(
    [
        Output('profile_picture', 'src'),
        Output('screen_name', 'children'),
        Output('name', 'children'),
        Output('description', 'children'),
        Output('followers_count','children'),
        Output('link_to_profile','href'),
        Output('most_retweeted_tweet_content','children'),
        Output('most_retweeted_tweet_date','children'),
        Output('retweet_count','children'),
        Output('favorite_count', 'children'),
        Output('wordcloud','src'),
        Output('statistics_graph', 'figure'),
        Output('sentimental_analysis_graph','figure')
    ],
    [
        Input('upload-data', 'filename'),
        Input('upload-data', 'contents')
    ])
def update_output(uploaded_filenames, uploaded_file_contents):
    """
    Save uploaded files and update the dashboard
    """

    if uploaded_file_contents is not None:

        # Check file names format and save information
        data = verify_file_upload(uploaded_file_contents, uploaded_filenames)
        # Save files in the CandidateData directory
        save_file(uploaded_filenames, uploaded_file_contents)

        # Launch a connexion to the Twitter API
        api = twitter_setup()

        # Retrieve user profile information
        df_user = update_candidate_profile(api, data)
        
        df_tweet = update_most_retweeted_tweet(api, data)
        
        wordcloud = generate_wordcloud(api, data)

        fig_stats = update_rt_stats(api, data)

        sentimental_analysis = update_sentimental_analysis_graph(api, data)
        
        return df_user.profile_image_url, \
                '@'+df_user.screen_name, \
                df_user.username, \
                df_user.description, \
                str(df_user.followers_count)+' followers',\
                df_user.url, \
                df_tweet.Content, \
                'Created at: '+str(df_tweet.Date), \
                str(df_tweet.RTs)+'RTs', \
                str(df_tweet.Likes)+'Likes', \
                wordcloud, \
                fig_stats, \
                sentimental_analysis
    else:
        raise dash.exceptions.PreventUpdate

def verify_file_upload(contents, filenames):
    """
    Assert filenames are well formatted and return a dictionary containing the candidate number as well as each file labeled according to its keyword type
    :param : contents
    :param : filenames
    :return : (dic) {'candidate_num': 4864, 'keywords':filename1, 'hashtags': filename2}
    """

    # Assert the filename matches the regex
    default_file_name = r'hashtags_candidate_\d*\.txt'
    assert re.match(default_file_name, filenames)
    
    num_candidate = int(re.findall(r"[0-9]+", filenames)[0])

    files = {}
    files['num_candidate'] = num_candidate
    files['filepath'] = 'CandidateData/'+filenames

    return files

def update_candidate_profile(api, data):
    user = get_candidate_info(api, data["num_candidate"])
    df_user = store_user_to_dataframe(user)
    return df_user

def update_most_retweeted_tweet(api, data):
    tweets = get_candidate_tweets(data['num_candidate'], api)
    tweets_df = store_tweets_to_dataframe(tweets)
    max_rt_tweet = get_the_most_retweeted_tweet(tweets_df) 
    return max_rt_tweet

def generate_wordcloud(api, data):

    queries = get_candidate_queries(data["num_candidate"], data["filepath"])
    tweets_query = get_tweets_from_candidates_search_queries(queries, api)
    tweets_query_df = store_tweets_to_dataframe(tweets_query)
    wordcloud_path = get_most_frequently_used_words(data["num_candidate"], tweets_query_df)

    # Encode the image
    encoded_wordcloud = base64.b64encode(open(wordcloud_path, 'rb').read()).decode('ascii')
    return 'data:image/png;base64,{}'.format(encoded_wordcloud)

def update_rt_stats(api, data):
    tweets_candidate = get_candidate_tweets(data["num_candidate"], api)
    tweets_candidate_df = store_tweets_to_dataframe(tweets_candidate)
    fig = visualize_tweets_time_evolution(tweets_candidate_df)
    return fig

def update_sentimental_analysis_graph(api, data):
    replies = get_replies_to_candidate(data["num_candidate"], api)
    replies_df = store_tweets_to_dataframe(replies)
    fig = sentimental_analysis_of_tweet_replies(replies_df)
    return fig

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]

    try:
        with open('CandidateData/'+name, "wb") as fp:
            fp.write(base64.decodebytes(data))
    except OSError as err: 
        raise(err)

if __name__ == '__main__':
    app.run_server(debug=True)