import tweepy
import json
from datetime import datetime

def store_tweets(tweets, filename):
    """
    Serialize in a json file the tweets collected given in parameter
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :param filename: the name of the file where to serialize data
    """

    # Convert the SearchResult object to a list and select a few attributes
    tweet_dic = {}
    count = 0

    for tweet in tweets:
        tweet_dic[count] = \
        {
            "id":tweet.id, 
            "date": tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S"), 
            "text":tweet.text, 
            "hashtags": tweet.entities['hashtags'],
            "retweet_count": tweet.retweet_count
        }
        count += 1

    with open(filename, "w") as write_file:
        json.dump(tweet_dic, write_file)


