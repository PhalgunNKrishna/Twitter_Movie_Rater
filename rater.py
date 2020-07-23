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

    # Extract 10 tweets from selected user
    posts = api.search("Hamilton", count=100, lang="en")

    # Print the last 5 tweets
    i = 1
    total_sentiment = 0
    postive_feeling = 0
    negative_feeling = 0
    neutral_feeling = 0
    print("Last 100 tweets: \n")
    for tweet in posts:
        cleaned_tweet = clean_text(tweet.text)
        analysis = TextBlob(cleaned_tweet)
        print(str(i) + ') ' + cleaned_tweet)
        print(analysis.sentiment, '\n')
        feelings = Polarity(cleaned_tweet)
        total_sentiment += feelings
        if feelings > 0:
            postive_feeling += 1
        elif feelings < 0:
            negative_feeling += 1
        else:
            neutral_feeling += 1
        i += 1

    print("Overall sentiment (higher = more liked): ", total_sentiment)
    print("Positive responses: ", postive_feeling)
    print("Neutral responses: ", neutral_feeling)
    print("Negative responses: ", negative_feeling)



except TwitterSearchException as e:
    print(e)
