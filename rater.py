from TwitterSearch import *
import tweepy
from textblob import TextBlob
import pandas as pd
import re
#import numpy as np
#from GUI import text


# tweepy API authentication
auth = tweepy.OAuthHandler('JUBWToPuyPfmzg8n117ZTllfB', 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1')
auth.set_access_token('1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p', '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1')
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['piss', 'after eating this'])

    # TwitterSearch authentication
    ts = TwitterSearch(
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
            access_token = '1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
            access_token_secret = '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
        )

    # for tweet in ts.search_tweets_iterable(tso):
    #     print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

    # Extract 10 tweets from selected user
    posts = api.user_timeline(screen_name="BillGates", count=10, language="en", tweet_mode="extended")

    # Print the last 5 tweets
    i = 1
    print("Last 5 tweets: \n")
    for tweet in posts[0:5]:
        print(str(i) + ') ' + tweet.full_text + '\n')
        i += 1

except TwitterSearchException as e:
    print(e)





