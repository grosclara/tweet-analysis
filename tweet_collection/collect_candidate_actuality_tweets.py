import tweepy
from .StreamListener import *

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
        print(err.response.text)
        raise err

    return tweets

def collect_candidate_actuality_tweets_by_streaming(queries, twitter_api):

    listener = StdOutListener()
    stream = tweepy.Stream(auth = twitter_api.auth, listener=listener)
    stream.filter(track=queries)