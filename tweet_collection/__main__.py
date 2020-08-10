# Main program initiating and executing a collection of tweets

from .tweet_collect import *
from .twitter_connection_setup import *

# Example
file_path = "./CandidateData/"
#Trump_ID = 736267842681602048
Biden_ID = 939091
keyword_type = "keywords"


# Connexion to the API
api = twitter_setup()

# Generate a query from the text files
queries = get_candidate_queries(Biden_ID, file_path, keyword_type)

# Collect candidate actuality tweets
tweets = get_tweets_from_candidates_search_queries(queries, api)
#collect_candidate_actuality_tweets_by_streaming(queries, api)

# Collect candidate's tweet activity
#get_replies_to_candidate(Biden_ID, api)
#print(collect_candidate_tweet_activity_by_streaming(twitter_api=api, candidate_id=Biden_ID))

#store_tweets_on disk(tweets, "./TweetsData/data_{}.json".format(Biden_ID))
print(store_tweets_to_dataframe(tweets))