import tweepy
import json
from datetime import datetime
import pandas as pd

def get_candidate_queries(num_candidate, file_path):
    """
    Generate and return a list of string queries for the search Twitter API from the file file_path_num_candidate.txt
    :param num_candidate: the number of the candidate
    :param file_path: the path to the keyword and hashtag 
    files
    :return: (list) a list of string queries that can be done to the search API independently
    """

    # Validation of parameters
    assert type(num_candidate) == int, "num_candidate should be a int"
    assert num_candidate > 0, "num_candidate should be positive"

    try :
        # Open txt file
        with open(file_path,'r',encoding = 'utf-8') as f:
            # Retrieve words
            keywords = f.read().split(',')
            # Remove empty keywords
            keywords = [w.strip() for w in keywords if w.strip()]
            # Remove duplicate and sort list
            keywords = sorted(set(keywords), key=str.lower)
            return keywords
    
    except IOError as err:
        raise err

def get_candidate_info(twitter_api, candidate_id):
    """
    Given a candidate Twitter id, return all its profile information.
    :param num_candidate: the candidate number
    :param twitter_api: the connection instance
    :return: (User) a tweepy User object containig the relevant information
    """

    try :
        # Retrieve the candidate's tweet
        profile_details = twitter_api.get_user(user_id=str(candidate_id))
    except tweepy.TweepError as err:
        raise err

    return profile_details



def get_candidate_tweets(candidate_id, twitter_api):
    """
    Given a candidate Twitter id, return all the recent tweets of the given candidate.
    :param num_candidate: the candidate number
    :param twitter_api: the connection instance
    :return: (SearchResult) a list of the candidate's most recent tweets
    """

    try :
        # Retrieve the candidate's tweet
        statuses = twitter_api.user_timeline(id = candidate_id, count = 100, tweet_mode='extended')

    except tweepy.TweepError as err:
        raise err

    return statuses

def get_tweets_from_candidates_search_queries(queries, twitter_api, lang="en"):
    """
    Given a query list (of the search type) and a twitter_api connection instance, 
    retrieve and return the tweets responding to the various queries.
    :param queries: the list of keywords
    :param twitter_api: the connection instance
    :return: (list) a list of the tweets returned from the API
    """

    query_string = ' OR '
    query_string = query_string.join(queries)

    try :
        tweets = twitter_api.search(query_string,language=lang,rpp=100, tweet_mode='extended')

    except tweepy.TweepError as err:
        raise err

    return tweets
    

def get_replies_to_candidate(candidate_id, twitter_api):
    """
    Given a candidate Twitter id, return every replies to the most recent tweet of the given candidate, 
    :param candidate_id: the candidate number
    :param twitter_api: the connection instance
    :return: (tuple) 1. (list) (Status) original tweet - 2. (list) a list containing every replies (Status objects)
    """

    replies = []

    try :
        for candidate_tweet in tweepy.Cursor(twitter_api.user_timeline,user_id=candidate_id, tweet_mode="extended").items(1):

            username = candidate_tweet.user.screen_name

            for tweet in tweepy.Cursor(twitter_api.search,q='to:{}'.format(username), 
                                        since_id=candidate_tweet.id, tweet_mode='extended').items(100):

                if (tweet.in_reply_to_status_id == candidate_tweet.id):
                    replies.append(tweet)

    except tweepy.TweepError as err:
        raise err

    return ([candidate_tweet], replies)

