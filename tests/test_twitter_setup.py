from ..tweet_collection.twitter_connection_setup import *

class TestClassTweetCollection:

    def test_twitter_connection_setup(self):
        api = twitter_setup()
        assert api is not None


