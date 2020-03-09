import logging
import time
from datetime import datetime
from sqlalchemy import create_engine
import pymongo
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Declare db and collection because if etl is 'read' before get_tweets it won't find them
client = pymongo.MongoClient('mongodb')
tweet_db = client['tweet_db']
tweet_coll = tweet_db['tweet_coll']

# creates a cursor of dictionaries
def extract_new_tweets():
    # all tweets with timestamp greater than last_udate (last update date)
    new_tweets = tweet_db.tweet_coll.find({ 'date_added' : { '$gt' : last_update }})

    return new_tweets

def transform_data(new_tweets):

    s = SentimentIntensityAnalyzer()
    sentiment_tweets = []

    # loop over every new tweet to perform the sentiment analysis (just in the tweet text)
    # also add a timestamp as log method
    for tweet in new_tweets:
        scores = s.polarity_scores(tweet['text'])
        scores['date_added'] = datetime.now()
        sentiment_tweets.append(scores)

    return sentiment_tweets

last_update = 0 # needed just for the first time
client = pymongo.MongoClient('mongodb') # to double-check if is still necessary to indicate it again
engine = create_engine('postgres://username:password@host:port/database')
# call to postgres, user, password, host(that I to talk to),port (of the host I to talk to),db

# Infinite loop for the tweet collection
while True:
    x = extract_new_tweets() # it creates cursor, loop over each doc to extract the correct data
    for doc in x:
        y = pd.DataFrame(transform_data(x))
        y.to_sql('tweet_pdb',engine,if_exists='append')

    # Log to filter the tweets to extract
    last_update = datetime.now()
    # Lag so that the export to postgres not happend continiously
    time.sleep(10)
