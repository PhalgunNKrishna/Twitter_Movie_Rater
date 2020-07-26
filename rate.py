from searchtweets import load_credentials
from searchtweets import collect_results
from searchtweets import gen_rule_payload

from textblob import TextBlob
import yaml
import pandas as pd
import re
import numpy as np
import tweepy
#from GUI import text

def rating(avg):
    if avg <= -5:
        return "Very Bad Movie"
    elif -5 < avg <= 0:
        return "Poor Movie"
    elif 0 < avg <= 5:
        return "Decent Movie"
    else:
        return "Great Movie"

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

config = dict(
        search_tweets_api = dict(
            account_type = 'premium',
            endpoint = 'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json',
            consumer_key = 'JUBWToPuyPfmzg8n117ZTllfB',
            consumer_secret = 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1'
            )
        )

premium_search_args = load_credentials("twitter_keys_fullarchive.yaml",
        yaml_key="search_tweets_api",
        env_overwrite=False)


#query = "If this were green KSI"
query = "Apocalytpo"
rule = gen_rule_payload(query, from_date="2017-09-01", to_date="2020-07-26", results_per_call=100)
tweets = collect_results(rule,
        max_results=100,
        result_stream_args=premium_search_args)

# lists that will become columns in our data frame
user_list = []
clean_list = []
favorited_list = []
retweet_list = []
its_a_retweet = []

for tweet in tweets:
    tw_obj = api.get_status(tweet.id)
    if not hasattr(tw_obj, 'retweeted_status'):
        user_list.append(tw_obj.user.screen_name)
        cleaned = clean_text(tweet.text)
        clean_list.append(cleaned)
        favorited_list.append(tweet.favorite_count)
        retweet_list.append(tweet.retweet_count)

# creating the data frame
# To make a column, you need a list
df = pd.DataFrame(user_list)
df['Tweet Text'] = clean_list
df['Number of Favorites'] = favorited_list
df['Number of Retweets'] = retweet_list
df['Polarity'] = df['Tweet Text'].apply(Polarity)

# sort data frame by polarity
sortedDF = df.sort_values(by=['Polarity'], ignore_index=True, ascending=False)

# sort data frame by favorites
sortedFavDF = df.sort_values(by=['Number of Favorites'], ignore_index=True, ascending=False)

 # gathering polarity data from df
pol_count = 0.0
for i in df.index:
    pol_count += df['Polarity'][i] * df['Number of Favorites'][i] + df['Polarity'][i] * 2.0 * df['Number of Retweets'][i]
    pol_count += df['Polarity'][i]
    avg_pol = float(pol_count/50.0)

print("Average Polarity: ", avg_pol)
print("Overall Rating: ", rating(avg_pol), '\n')

# 5 Most Popular Tweets
print("5 most popular tweets: ")
for i in range(0, 5):
    print(str(i + 1) + ") " + sortedFavDF['Tweet Text'][i] + ". Number of Favorites: ", sortedFavDF['Number of Favorites'][i])

# 5 Most Positive Tweets
print("\n5 Most Positive Tweets: ")
for i in range(0, 5):
    print(str(i + 1) + ") " + sortedDF['Tweet Text'][i] + ". Polarity: ", sortedFavDF['Polarity'][i])

print("\n5 Most Negative Tweets: ")
j = 1
for i in range(df['Tweet Text'].size, df['Tweet Text'].size - 5, -1):
    print(str(j) + ") " + sortedDF['Tweet Text'][i - 1] + ". Polarity: ", sortedFavDF['Polarity'][i - 1])
    j += 1







