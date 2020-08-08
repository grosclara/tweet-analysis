from ..tweet_collection.twitter_connection_setup import *

def test_twitter_connection_setup():
    api = twitter_setup()
    assert api is not None