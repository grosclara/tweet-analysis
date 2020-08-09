from tweepy.streaming import StreamListener
import tweepy

class StdOutListener(StreamListener):

    """ def on_data(self, data):
        print(data)
        return True """
    
    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        if  str(status) == "420":
            print(status.text)
            print("You exceed a limited number of attempts to connect to the streaming API")
            return False
        else:
            return True

