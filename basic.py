from TwitterSearch import *
from textblob import TextBlob
import tweepy
import pandas as pd
import re
#import numpy as np
#from GUI import text

def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # Removing @ mentions 
    text = re.sub(r'#', '', text) # Removing '#' 
    text = re.sub(r'RT[\s]+', '', text) # Removing retweet symbols
    text = re.sub(r'https?:\/\/\S+', '', text) # Removing hyper links

    return text

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
    tso.set_keywords(['piss', 'after eating this'])
    ts = TwitterSearch(
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
            access_token = '1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
            access_token_secret = '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
        )

    clean_list = []
    favorited_list = []
    retweet_list = []

    for tweet in ts.search_tweets_iterable(tso):
        for tw in api.user_timeline(id = tweet['user']['screen_name'], lang="en"):
            if tw.text == tweet['text']:
                obj = api.get_status(tw.id)
                cleaned = clean_text(obj.text)
                clean_list.append(cleaned)
                favorited_list.append(obj.favorite_count)
                retweet_list.append(obj.retweet_count)

    df = pd.DataFrame( [tweet['user']['screen_name'] for tweet in ts.search_tweets_iterable(tso)] , columns = ['User'] )

    df['Tweet Text'] = clean_list
    df['Number of Favorites'] = favorite_count
    df['Number of Retweets'] = retweet_count

    

except TwitterSearchException as e:
    print(e)

