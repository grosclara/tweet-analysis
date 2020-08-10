import tweepy
import json
from datetime import datetime
import pandas as pd

def get_candidate_queries(num_candidate, file_path, keyword_type):
    """
    Generate and return a list of string queries for the search Twitter API from the file file_path_num_candidate.txt
    :param num_candidate: the number of the candidate
    :param file_path: the path to the keyword and hashtag 
    files
    :param type: type of the keyword, either "keywords" or "hashtags"
    :return: (list) a list of string queries that can be done to the search API independently
    """

    # Validation of parameters
    assert keyword_type == 'hashtags' or keyword_type == 'keywords', "Invalid keyword_type parameter: either 'hashtags' or 'keywords'"
    assert type(num_candidate) == int, "num_candidate should be a int"
    assert num_candidate > 0, "num_candidate should be positive"

    try :
        # Open txt file
        with open("{0}{1}_candidate_{2}.txt".format(file_path, keyword_type, num_candidate),'r',encoding = 'utf-8') as f:
            # Retrieve words
            keywords = f.read().split(',')
            # Remove empty keywords
            keywords = [w.strip() for w in keywords if w.strip()]
            # Remove duplicate and sort list
            keywords = sorted(set(keywords), key=str.lower)
            return keywords
    
    except IOError as err:
        raise err

def get_candidate_tweets(candidate_id, twitter_api):
    """
    Given a candidate Twitter id, return all the recent tweets of the given candidate.
    :param num_candidate: the candidate number
    :param twitter_api: the connection instance
    :return: (SearchResult) a list of the candidate's most recent tweets
    """

    try :
        # Retrieve the candidate's tweet
        statuses = twitter_api.user_timeline(id = candidate_id, count = 100)

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
        tweets = twitter_api.search(query_string,language=lang,rpp=100)

    except tweepy.TweepError as err:
        raise err

    return tweets
    

def get_replies_to_candidate(candidate_id, twitter_api):
    """
    Given a candidate Twitter id, return for each recent tweet of the given candidate, 
    the re-tweets to this tweet. The information on the original tweet will be kept in the type of return.
    :param num_candidate: the candidate number
    :param twitter_api: the connection instance
    :return: (tuple) a tuple containing the candidate's tweet and a list of the corresponding retweets
    """

    retweets = []

    try :
        # Retrieve the candidate's tweet
        status = twitter_api.user_timeline(id = candidate_id, count = 1)[0]

        # If status is not null, retrieves the correponding retweets
        if status:
            retweets = twitter_api.retweets(id = status.id, count = 100)

    except tweepy.TweepError as err:
        raise err

    return (status, retweets)

