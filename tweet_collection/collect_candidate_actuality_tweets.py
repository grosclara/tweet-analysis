import tweepy

def get_tweets_from_candidates_search_queries(queries, twitter_api):
    """
    Given a query query list (of the search type) and a twitter_api connection instance, 
    retrieve and return the tweets responding to the various queries.
    :param queries: the list of keywords
    :param twitter_api: the connection instance
    :return: (list) a list of the tweets returned from the API