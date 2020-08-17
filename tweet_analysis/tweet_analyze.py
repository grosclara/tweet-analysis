# Design and program a set of functions to extract relevant information from a set of tweets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from textblob import TextBlob
from textblob import Blobber
import nltk
import re
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
import plotly.graph_objects as go

def store_tweets_to_dataframe(tweets):
    """
    Transform the Tweepy object tweets in a DataFrame and return it
    :param tweets: a list of tweets (SearchResult of Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing tweets relevant information
    """

    """         
        df.Date = df.Date.astype('datetime64[ns]')
        df.Length = df.Length.astype('int32')
        df.RTs = df.RTs.astype('int32')
        df.Content = df.Content.astype('string')
        df.Likes = df.Likes.astype('int32') 
    """


    column_names = ["ID", "Date", "Content", "Length", "RTs", "Likes"]
    df = pd.DataFrame(columns = column_names)

    # Fill the dataframe
    for tweet in tweets:
        df = df.append({\
                "ID":tweet.id, 
                "Date": tweet.created_at.strftime("%m/%d/%Y, %H:%M:%S"), 
                "Content":tweet.full_text, 
                "Length": len(tweet.full_text),
                "RTs": tweet.retweet_count,
                "Likes": tweet.favorite_count
            }, ignore_index=True)

    return df

def store_user_to_dataframe(user):
    """
    Transform the Tweepy object user in a Serie and return it
    :param user: a Tweepy User object
    :return (pd.Series) the Serie containing the relevant information
    """

    profile_pic_url = re.sub(r'_normal', '', user.profile_image_url)

    l = {
        "ID":user.id,
        "username": user.name,
        "screen_name": user.screen_name,
        "description": user.description,
        "url": user.url,
        "followers_count": user.followers_count,
        "profile_image_url": profile_pic_url
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
                    title="Time evolution of the candidate's tweets"
                )
    return fig

def sentimental_analysis_of_tweet_replies(replies):
    """
    Return a new dataframe indexed by the date containing Likes, Polarity and Subjectivity indicators
    :param replies: a list of tweets (Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the tweets and their sentimental analysis
    """

    # Load data
    replies['Polarity'] = replies['Content'].map(lambda x: TextBlob(x).sentiment.polarity)
    replies['Subjectivity'] = replies['Content'].map(lambda x: TextBlob(x).sentiment.subjectivity)

    hover_text = []
    bubble_size = []

    for index, row in replies.iterrows():
        hover_text.append(('Date: {date}<br>'+
                        'Content: {content}<br>'+
                        'Length: {len}<br>'+
                        'RTs: {rts}<br>'+
                        'Likes: {likes}<br>'+
                        'Polarity: {polarity}<br>'+
                        'Subjectivity: {subj}<br>').format(date=row['Date'],
                                                content=row['Content'],
                                                len=row['Length'],
                                                rts=row['RTs'],
                                                likes=row['Likes'],
                                                polarity=row['Polarity'],
                                                subj = row['Subjectivity']))
      
        bubble_size.append(row['RTs']) if int(row['RTs']) != 0 else bubble_size.append(0.5)

    replies['Text'] = hover_text
    replies['Size'] = bubble_size
    sizeref = 2.*max(replies['Size'])/(100**2)

    # Create figure
    fig = go.Figure()
        
    fig = go.Figure(data=[go.Scatter(
        x=replies['Polarity'], y=replies['Subjectivity'],
        text=replies['Text'],
        name='Retweet counts',
        marker_size=replies['Size'],
        # Tune marker appearance and layout
        mode='markers',
        marker=dict(
            color=replies["Likes"],
            sizemode='area', 
            sizeref=sizeref, 
            line_width=2,
            showscale=True
            ))
    ])

    fig.update_layout(
        title='Polarity vs Subjectivity of the candidate\'s tweets',
        xaxis=dict(
            title='Polarity',
            gridcolor='white',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Subjectivity',
            gridcolor='white',
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    
    return fig

def get_most_frequently_used_words(candidate_num, tweets):
    """
    Return a new dataframe containing word and their frequency after having removed stop words
    :param tweets: a list (SearchResult object) of tweets (Tweepy Status objects)
    :return (pd.DataFrame) the DataFrame containing the relevant words and their frequency
    """

    words = ''
    textual_content = tweets.Content.to_list()

    try :
        for tweet in textual_content:
            for word in tweet.split(' '):
                words += ' '+word

        words = TextBlob(clean_tweets(words))

        wc = WordCloud(background_color="black", max_words=1000)
        # generate word cloud
        wc.generate_from_frequencies(words.word_counts)

        return wc.to_image()

    except ValueError:
        return None

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

