import tweepy

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
    except tweepy.TweepError:
        raise
    except tweepy.RateLimitError:
        raise

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
    except tweepy.TweepError :
        raise
    except tweepy.RateLimitError:
        raise

    return statuses

def get_tweets_from_hashtag(hashtag, twitter_api):
    """
    Given a query list (of the search type) and a twitter_api connection instance, 
    retrieve and return the tweets responding to the various queries.
    :param queries: the list of keywords
    :param twitter_api: the connection instance
    :return: (list) a list of the tweets returned from the API
    """

    try :
        tweets = twitter_api.search(hashtag, result_type='popular', rpp=100, tweet_mode='extended')
    except tweepy.TweepError:
        raise
    except tweepy.RateLimitError:
        raise

    return tweets
    

def get_replies_to_candidate(candidate_id, twitter_api):
    """
    Given a candidate Twitter id, return most popular replies to the given candidate's tweets 
    :param candidate_id: the candidate number
    :param twitter_api: the connection instance
    :return: (list) a list containing every popular replies (Status objects)
    """

    profile = get_candidate_info(twitter_api, candidate_id)
    user_name = "@"+profile.screen_name

    popular_replies = []

    replies = tweepy.Cursor(twitter_api.search, q='to:{} filter:replies'.format(user_name), result_type='popular', tweet_mode='extended').items()
    while True:
        try:
            reply = replies.next()
            if not hasattr(reply, 'in_reply_to_user_id_str'):
                continue
            else:
                if reply.in_reply_to_user_id == candidate_id :
                    popular_replies.append(reply)
        
        except tweepy.RateLimitError as e:
            continue

        except tweepy.TweepError as e:
            break

        except StopIteration:
            break
    
    return popular_replies