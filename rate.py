from TwitterSearch import *
from textblob import TextBlob
import tweepy
import pandas as pd
import re
#import numpy as np
#from GUI import text

auth = tweepy.OAuthHandler('JUBWToPuyPfmzg8n117ZTllfB', 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1')
auth.set_access_token('1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p', '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1')

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

try:
    tso = TwitterSearchOrder()
    #tso.set_keywords(['Goofy', 'Nyancat'], or_operator = True)
    #tso.add_keyword('BMW')
    tso.set_keywords(['piss', 'after eating this'])

    ts = TwitterSearch(
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
            access_token = '1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
            access_token_secret = '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
        )

    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
        for tw in api.user_timeline(id = tweet['user']['screen_name'], lang="en"):
            if tw.text == tweet['text']:
                obj = api.get_status(tw.id)
                print("likes for this tweet: %d" % obj.favorite_count)
                print("retweets of this tweet: %d" % obj.retweet_count)





except TwitterSearchException as e:
    print(e)





