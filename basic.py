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

def Polarity(text):
    return TextBlob(text).sentiment.polarity


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
    tso.set_keywords(['Hamilton'])
    tso.set_count(50)
    #tso.set_keywords(['Benefits of having sites on Cloudflare:'])
    #tso.set_keywords(['Also planning something fun for Tuesday'])
    ts = TwitterSearch(
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
            access_token = '1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
            access_token_secret = '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
            )

    # lists that will become columns in our data frame
    clean_list = []
    favorited_list = []
    retweet_list = []
    its_a_retweet = []

    # next 4 lines ending with "obj = api.get..." are to find the actual tweet object
    for tweet in ts.search_tweets_iterable(tso):
                #tw_obj = api.get_status(tweet['id'])
                cleaned = clean_text(tweet['text']) # removing unnecessary symbols from the tweet's string
                clean_list.append(cleaned)
                #favorited_list.append(obj.favorite_count)
                #retweet_list.append(obj.retweet_count)
                favorited_list.append(tweet['favorite_count'])
                retweet_list.append(tweet['retweet_count'])
                #its_a_retweet.append(hasattr(tw_obj, 'retweeted_status'))

    # creating the data frame
    # To make a column, you need a list
    df = pd.DataFrame( [tweet['user']['screen_name'] for tweet in ts.search_tweets_iterable(tso)] , columns = ['User'] )
    df['Tweet Text'] = clean_list
    df['Number of Favorites'] = favorited_list
    df['Number of Retweets'] = retweet_list
    df['Polarity'] = df['Tweet Text'].apply(Polarity)

    print(df)



except TwitterSearchException as e:
    print(e)

