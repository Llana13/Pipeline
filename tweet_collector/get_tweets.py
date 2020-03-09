import config # where the authentication credentials are
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo
from datetime import datetime



def authenticate():
    """Function for Twitter Authentication"""
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #it is a python dictionary.
        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count'],
        'date_added': datetime.now() #add the date and time in which was added
                }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        tweet_db.tweet_coll.insert_one(tweet) # insert the whole tweet in database.collection

    def on_error(self, status):
        if status == 420:
            print(status)
            return False


client = pymongo.MongoClient('mongodb')
tweet_db = client['tweet_db']
tweet_coll = tweet_db['tweet_coll']

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    # Change the track in order to intercept different tweets
    stream.filter(track=['data science'], languages=['en'])
