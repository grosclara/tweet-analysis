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

def update_candidate_profile(api, num_candidate):
    user = get_candidate_info(api, num_candidate)
    df_user = store_user_to_dataframe(user)
    return df_user

def update_most_retweeted_tweet(api, num_candidate):
    tweets = get_candidate_tweets(num_candidate, api)
    tweets_df = store_tweets_to_dataframe(tweets)
    max_rt_tweet = get_the_most_retweeted_tweet(tweets_df) 
    return max_rt_tweet

def generate_wordcloud(api, hashtag, num_candidate):
    tweets_query = get_tweets_from_hashtag(hashtag, api)
    tweets_query_df = store_tweets_to_dataframe(tweets_query)
    wordcloud = get_most_frequently_used_words(num_candidate, tweets_query_df)

    img = BytesIO()
    wordcloud.save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

def update_rt_stats(api, num_candidate):
    tweets_candidate = get_candidate_tweets(num_candidate, api)
    tweets_candidate_df = store_tweets_to_dataframe(tweets_candidate)
    fig = visualize_tweets_time_evolution(tweets_candidate_df)
    return fig

def update_sentimental_analysis_graph(api, num_candidate):
    replies = get_replies_to_candidate(num_candidate, api)
    replies_df = store_tweets_to_dataframe(replies)
    fig = sentimental_analysis_of_tweet_replies(replies_df)
    return fig