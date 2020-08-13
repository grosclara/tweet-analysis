# Design and program a set of functions to extract relevant information from a set of tweets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
from wordcloud import WordCloud
# Using plotly.express
import plotly.express as px

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
        "username": user.name,
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
    :param tweets: a dataframe of tweets
    :return (pd.DataFrame) the dataframe containing the most retweeted tweet
    """

    rt_max  = np.max(tweets['RTs'])
    rt  = tweets[tweets.RTs == rt_max].squeeze()
    # Max RTs:
    #print("The tweet with more retweets is: \n{}".format(tweets['Content'][rt]))
    #print("Number of retweets: {}".tweet_mode=extendedormat(rt_max))
    #print("{} characters.\n".format(tweets['Length'][rt])) """
    return rt

def visualize_tweets_time_evolution(tweets):
    """
    Return a new dataframe indexed by the date containing RTs and Likes
    Optionnally plot RTs and Likes as time functions
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the most retweeted tweets 
    """


    fig = px.line(tweets, x='Date', y=['RTs','Likes'], \
                    labels={ "value": "Counts" ,
                            'variable': 'Legend'},
                    title="Time evolution of the Candidat's tweets"
                )
    return fig

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

def get_most_frequently_used_words(candidate_num, tweets):
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

    wc = WordCloud(background_color="black", max_words=1000)
    # generate word cloud
    wc.generate_from_frequencies(words.word_counts)

    filepath = './images/wordcloud_{}.png'.format(candidate_num)

    # save
    fig = plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    fig.savefig(filepath)

    return filepath



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

def getFrequencyDictForText(text):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for word in text:
        val = tmpDict.get(word, 0)
        tmpDict[word] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict

