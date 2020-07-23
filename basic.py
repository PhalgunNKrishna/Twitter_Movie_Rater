from TwitterSearch import *
from textblob import TextBlob
import tweepy
import pandas as pd
import re

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
    #tso.set_keywords(['Apocalypto'])
    tso.set_keywords(['Phantom Menace'])
    tso.set_language('en')
    ts = TwitterSearch(
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
            access_token = '1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
            access_token_secret = '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
            )

    # lists that will become columns in our data frame
    user_list = []
    clean_list = []
    favorited_list = []
    retweet_list = []
    its_a_retweet = []

    count = 0

    for tweet in ts.search_tweets_iterable(tso):
                if count == 100:
                    break
                tw_obj = api.get_status(tweet['id_str'])    # need the twitter object to check if it's a retweet
                user_list.append(tweet['user']['screen_name'])  # user
                cleaned = clean_text(tweet['text']) # removing unnecessary symbols from the tweet's string
                clean_list.append(cleaned)
                favorited_list.append(tweet['favorite_count']) # num of favorites
                retweet_list.append(tweet['retweet_count']) # num of retweets
                its_a_retweet.append(hasattr(tw_obj, 'retweeted_status'))
                count += 1

    # creating the data frame
    # To make a column, you need a list
    df = pd.DataFrame(user_list)
    df['Tweet Text'] = clean_list
    df['Number of Favorites'] = favorited_list
    df['Number of Retweets'] = retweet_list
    df['Polarity'] = df['Tweet Text'].apply(Polarity)
    df['Retweet?'] = its_a_retweet

    print(df)

    #gathering polarity data from df
    pol_count = 0
    for i in df.index:
        pol_count += df['Polarity'][i] * df['Number of Favorites'][i] + 2 * df['Number of Retweets'][i]
    avg_pol = pol_count / 100
    print("average polarity = %d" % avg_pol)
    print("This movie has a rating of $d out of 5 stars" % rating)

    #5 Most Popular Tweets

    #5 Most Positive Tweets

    #5 Most Negative Tweets

except TwitterSearchException as e:
    print(e)

