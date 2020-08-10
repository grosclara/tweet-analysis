# Design and program a set of functions to extract relevant information from a set of tweets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def store_tweets_on_disk(tweets, filename):
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
            "ID":tweet.id, 
            "Date": tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S"), 
            "Content":tweet.full_text, 
            "Length": len(tweet.full_text),
            #"hashtags": tweet.entities['hashtags'],
            "RTs": tweet.retweet_count,
            "Likes": tweet.favorite_count
        }
        count += 1

    with open(filename, "w") as write_file:
        json.dump(tweet_dic, write_file)

def store_tweets_to_dataframe(tweets):
    """
    Transform the Tweepy object tweets in a DataFrame and return it
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing tweets relevant information
    """

    l = []

    # Convert the SearchResult object to a list and select a few attributes
    for tweet in tweets:
        l.append(\
        {
            "ID":tweet.id, 
            "Date": tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S"), 
            "Content":tweet.full_text, 
            "Length": len(tweet.full_text),
            #"hashtags": tweet.entities['hashtags'],
            "RTs": tweet.retweet_count,
            "Likes": tweet.favorite_count
        }
        )

    df = pd.DataFrame(l)

    df.Date = df.Date.astype('datetime64[ns]')
    df.Length = df.Length.astype('int32')
    df.RTs = df.RTs.astype('int32')
    df.Content = df.Content.astype('string')
    df.Likes = df.Likes.astype('int32')

    return df

def get_the_most_retweeted_tweet(tweets):
    """
    Return the most retweeted tweet
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the most retweeted tweets 
    """

    rt_max  = np.max(tweets['RTs'])
    rt  = tweets[tweets.RTs == rt_max]#.index[0] 
    # Max RTs:
    #print("The tweet with more retweets is: \n{}".format(tweets['Content'][rt]))
    #print("Number of retweets: {}".format(rt_max))
    #print("{} characters.\n".format(tweets['Length'][rt])) """
    return rt_max

def visualize_tweets_time_evolution(tweets):
    """
    Plot RTs and Likes as time functions
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the most retweeted tweets 
    """

    new = tweets.set_index("Date").filter(['RTs','Likes'], axis=1)
    # Likes vs retweets visualization:
    #new.plot()
    #plt.show()

    return new