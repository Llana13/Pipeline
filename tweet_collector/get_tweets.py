'''Intercept tweets via Twitter API and stores them in a mongoDB'''

import json
import logging
from datetime import datetime
import pymongo
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import config


def authenticate():
    """Function for Twitter Authentication"""
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):
    '''Listener Class '''

    def on_data(self, data):
        '''This defines what is done with every single tweet as it is intercepted'''

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
        '''On error 420 print the status '''
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
    stream.filter(track=['data science'], languages=['en'])
