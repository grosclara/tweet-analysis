import tweepy
from .StreamListener import *

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
        print(err.response.text)
        raise err

    return (status, retweets)

def collect_candidate_tweet_activity_by_streaming(candidate_id, twitter_api):

    listener = StdOutListener()
    stream=tweepy.Stream(auth = twitter_api.auth, listener=listener)
    stream.filter(follow=[str(candidate_id)])
