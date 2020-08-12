# Design and program a set of functions to extract relevant information from a set of tweets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob import Blobber
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from textblob import Word

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

def store_user_to_dataframe(user):
    """
    Transform the Tweepy object user in a Serie and return it
    :param user: a Tweepy User object
    :return (pd.Series) the Serie containing the relevant information
    """

    l = {
        "ID":user.id,
        "name": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "url": user.url,
        "followers_count": user.followers_count,
        "profile_image_url": user.profile_image_url
    }

    df = pd.Series(l)

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
    #print("Number of retweets: {}".tweet_mode=extendedormat(rt_max))
    #print("{} characters.\n".format(tweets['Length'][rt])) """
    return rt_max

def visualize_tweets_time_evolution(tweets):
    """
    Return a new dataframe indexed by the date containing RTs and Likes
    Optionnally plot RTs and Likes as time functions
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the most retweeted tweets 
    """

    new = tweets.set_index("Date").filter(['RTs','Likes'], axis=1)
    # Likes vs retweets visualization:
    #new.plot()
    #plt.show()

    return new

def sentimental_analysis_of_tweet_replies(replies):
    """
    Return a new dataframe indexed by the date containing Likes, Polarity and Subjectivity indicators
    :param replies: a list of tweets (Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the tweets and their sentimental analysis
    """

    df = replies.filter(["Likes"])
    df['Polarity'] = replies['Content'].map(lambda x: TextBlob(x).sentiment.polarity)
    df['Subjectivity'] = replies['Content'].map(lambda x: TextBlob(x).sentiment.subjectivity)

    return df

def get_most_frequently_used_words(tweets):
    """
    Return a new dataframe containing word and their frequency after having removed stop words
    :param tweets: a list (SearchResult object) of tweets (Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the relevant words and their frequency
    """

    words = ''
    textual_content = tweets.Content.to_list()
    for tweet in textual_content:
        for word in tweet.split(' '):
            words += ' '+word

    words = TextBlob(clean_tweets(words))

    word = np.array(list(words.word_counts.keys()))
    frequency = np.array(list(words.word_counts.values()))

    df = pd.DataFrame({'Word':word, 'Frequency':frequency}).sort_values("Frequency", ascending=False)
    return df

def clean_tweets(tweet_words):
    """
    Clean a string of words by removing punctuation, stopwords and unrelevant words
    :param words: a string of words to clean
    :return (str) a text with relevant words only
    """

    # Split into words
    tokens = word_tokenize(tweet_words)
    # Convert to lower case
    tokens = [w.lower() for w in tokens]
    # Remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # Remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # Filter out stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    text = ''
    for w in words:
        if w not in ['rt', 'http','https']:
            text += ' '+Word(w).lemmatize()

    return text

