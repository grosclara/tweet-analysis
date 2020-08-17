# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html

from tweet_collection.tweet_collect import *
from tweet_collection.twitter_connection_setup import *
from tweet_analysis.tweet_analyze import *

from dashboard.callbacks import *
from dashboard.layout import *

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([sidebar, content])

@app.callback(
    [
        #Profile
        Output('profile-picture', 'src'),
        Output('username', 'children'),
        Output('description', 'children'),
        Output('followers-count','children'),
        
        # Most retweeted tweet
        Output('tweet-content','children'),
        Output('tweet-date','children'),
        Output('rt-count','children'),
        Output('like-count', 'children'),

        # Wordcloud
        Output('wordcloud-img','src'),

        #Charts
        Output('tweets-evolution', 'figure'),
        Output('bubble-chart','figure')
    ],
    [
        Input('submit-button', 'n_clicks'),
        Input('input-hashtag', 'value'),
        Input('input-candidate-id', 'value')
    ])
def update_output(n_clicks, hashtag, num_candidate):
    """ Update the dashboard """

    if n_clicks > 0:

        # Launch a connexion to the Twitter API
        api = twitter_setup()

        df_user = update_candidate_profile(api, num_candidate)
        df_tweet = update_most_retweeted_tweet(api, num_candidate)
        wordcloud = generate_wordcloud(api, hashtag, num_candidate)
        fig_stats = update_rt_stats(api, num_candidate)
        sentimental_analysis = update_sentimental_analysis_graph(api, num_candidate)
        
        return df_user.profile_image_url, \
                df_user.username, \
                df_user.description, \
                str(df_user.followers_count)+' followers',\
                df_tweet.Content, \
                'Created at: '+str(df_tweet.Date), \
                str(df_tweet.RTs)+' RTs', \
                str(df_tweet.Likes)+' Likes', \
                wordcloud, \
                fig_stats, \
                sentimental_analysis

    else:
        # Prevent from firing callback when loading page
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)