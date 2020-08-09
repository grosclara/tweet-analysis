from ..tweet_collection.twitter_connection_setup import *
from ..tweet_collection.get_queries import *

import pytest

class TestClassTwitterConnectionSetup:

    def test_twitter_connection_setup(self):
        api = twitter_setup()
        assert api is not None

class TestClassSearchQueries:

    file_path = "./tests/testCandidateData/"
    num_candidate = 1
    keyword_type = "keywords"

    def test_invalid_file_path(self):
        invalid_file_path = "wrong_file_path/"
        with pytest.raises(FileNotFoundError):
            get_candidate_queries(self.num_candidate, invalid_file_path, self.keyword_type)

    def test_invalid_num_candidate(self):
        invalid_num_candidate = "str"
        with pytest.raises(AssertionError):
            get_candidate_queries(invalid_num_candidate, self.file_path, self.keyword_type)

    def test_non_existent_candidate(self):
        non_existent_num_candidate = 2
        with pytest.raises(FileNotFoundError):
            get_candidate_queries(non_existent_num_candidate, self.file_path, self.keyword_type)

    def test_negative_num_candidate(self):
        negative_num_candidate = -1
        with pytest.raises(AssertionError):
            get_candidate_queries(negative_num_candidate, self.file_path, self.keyword_type)

    def test_invalid_keyword_type(self):
        invalid_keyword_type = "banana"
        with pytest.raises(AssertionError):
            get_candidate_queries(self.num_candidate, self.file_path, invalid_keyword_type)

    def test_valid_queries(self):
        assert get_candidate_queries(self.num_candidate, self.file_path, self.keyword_type) == ['Donald AND Trump','Trump']

class TestClassCollectTweets:

    api = twitter_setup()
    candidate_id = 939091 #Joe Biden Twitter ID

    def test_get_tweets_from_candidates_search_queries:
        pass

    def test_get_replies_to_candidate:
        pass

    def test_get_live_candidate_tweet_activity:
        pass

    def test_get_live_candidate_actuality_tweets:
        pass

