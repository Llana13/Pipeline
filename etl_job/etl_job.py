'''Takes data from MongoDB, transform it and store it in a postgres Database '''
import time
from datetime import datetime
from sqlalchemy import create_engine
import pymongo
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client = pymongo.MongoClient('mongodb')
tweet_db = client['tweet_db']
tweet_coll = tweet_db['tweet_coll']

def extract_new_tweets():
    '''Get tweets from MongoDB with a date greater than the last upload to postgres the output is a cursor of dictionaries'''

    new_tweets = tweet_db.tweet_coll.find({'date_added' : {'$gt' : last_update}})
    return new_tweets

def transform_data(new_tweets):
    '''Get the sentiment scores of each tweet corpus'''

    s = SentimentIntensityAnalyzer()
    sentiment_tweets = []

    for tweet in new_tweets:
        scores = s.polarity_scores(tweet['text'])
        scores['date_added'] = datetime.now() # log method
        sentiment_tweets.append(scores)

    return sentiment_tweets

last_update = 0 # needed just for the first time
client = pymongo.MongoClient('mongodb')
engine = create_engine('postgres://postgres:postgres@postgresdb:5432/tweet_pdb')


while True:
    x = extract_new_tweets()
    for doc in x:
        y = pd.DataFrame(transform_data(x))
        y.to_sql('tweet_pdb', engine, if_exists='append')

    last_update = datetime.now()
    time.sleep(10) # to avoid continiously uploading to postgres
