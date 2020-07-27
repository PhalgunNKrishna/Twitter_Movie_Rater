from TwitterSearch import *
from textblob import TextBlob
import tkinter as tk
from PIL import ImageTk, Image
import tweepy
import pandas as pd
import re

HEIGHT = 700
WIDTH = 800

auth = tweepy.OAuthHandler('JUBWToPuyPfmzg8n117ZTllfB', 'lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1')
auth.set_access_token('1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p', '5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1')

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")

except:
    print("Error during authentication")



def rating(avg):
    if avg <= -15:
        return "Twitter Hates"
    elif -15 < avg <= 0:
        return "Twitter Dislikes"
    elif 0 < avg <= 15:
        return "Twitter Likes"
    else:
        return "Twitter Loves"


def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # Removing @ mentions
    text = re.sub(r'#', '', text) # Removing '#'
    text = re.sub(r'RT[\s]+', '', text) # Removing retweet symbols
    text = re.sub(r'https?:\/\/\S+', '', text) # Removing hyper links
    return text


def Polarity(text):
    return TextBlob(text).sentiment.polarity


def find_polarity(topic):
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords([topic])
        tso.set_language('en')
        ts = TwitterSearch(
                consumer_key='JUBWToPuyPfmzg8n117ZTllfB',
                consumer_secret='lt0Psg46Nqzzaa4uel3wtSbaOyh9WiYIqx6ZH5xaExthndrsc1',
                access_token='1172272055183728640-nLQg9fvsLVieB9BXSsJq86a6kMmR8p',
                access_token_secret='5ogC7PXA1nmlNd5FCYtNaSIhF7tyA5K7CZzNBhi8qIhv1'
                )

        # lists that will become columns in our data frame
        user_list = []
        clean_list = []
        favorited_list = []
        retweet_list = []
        its_a_retweet = []

        count = 0

        for tweet in ts.search_tweets_iterable(tso):
            if count == 50:
                break
            tw_obj = api.get_status(tweet['id_str'])  # need the twitter object to check if it's a retweet
            if not hasattr(tw_obj, 'retweeted_status'):
                user_list.append(tweet['user']['screen_name'])  # user
                cleaned = clean_text(tweet['text'])  # removing unnecessary symbols from the tweet's string
                clean_list.append(cleaned)
                favorited_list.append(tweet['favorite_count'])  # num of favorites
                retweet_list.append(tweet['retweet_count'])  # num of retweets
                its_a_retweet.append(hasattr(tw_obj, 'retweeted_status'))
                count += 1

        # creating the data frame
        # To make a column, you need a list
        df = pd.DataFrame(user_list)
        df['Tweet Text'] = clean_list
        df['Number of Favorites'] = favorited_list
        df['Number of Retweets'] = retweet_list
        df['Polarity'] = df['Tweet Text'].apply(Polarity)
        # df['Retweet?'] = its_a_retweet

        # print(df)

        # sort data frame by polarity
        sortedDF = df.sort_values(by=['Polarity'], ignore_index=True, ascending=False)

        # sort data frame by favorites
        sortedFavDF = df.sort_values(by=['Number of Favorites'], ignore_index=True, ascending=False)

        # gathering polarity data from df
        pol_count = 0.0
        for i in df.index:
            pol_count += df['Polarity'][i] * df['Number of Favorites'][i] + df['Polarity'][i] * 2.0 * df['Number of Retweets'][i]
            pol_count += df['Polarity'][i]
        avg_pol = pol_count

        print("Average Polarity: ", avg_pol)
        print("Overall Rating: ", rating(avg_pol), '\n')
        label['text'] = "Average Polarity: " + str(avg_pol) + '\n' + "Overall Rating: " + rating(avg_pol) + '\n'

        # 5 Most Popular Tweets
        print("5 most popular tweets: ")
        label['text'] += '\n' + "5 most popular tweets: " + '\n'
        for i in range(0, 5):
            label['text'] += str(i + 1) + ") " + sortedFavDF['Tweet Text'][i] + '\n'
            print(str(i + 1) + ") " + sortedFavDF['Tweet Text'][i])

        # 5 Most Positive Tweets
        print("\n5 Most Positive Tweets: ")
        label['text'] += '\n' + "5 most positive tweets: " + '\n'
        for i in range(0, 5):
            label['text'] += str(i + 1) + ") " + sortedDF['Tweet Text'][i] + '\n'
            print(str(i + 1) + ") " + sortedDF['Tweet Text'][i])

        print("\n5 Most Negative Tweets: ")
        label['text'] += '\n' + "5 most negative tweets: " + '\n'
        j = 1
        for i in range(df['Tweet Text'].size, df['Tweet Text'].size - 5, -1):
            label['text'] += str(j) + ") " + sortedDF['Tweet Text'][i - 1] + '\n'
            print(str(j) + ") " + sortedDF['Tweet Text'][i - 1])
            j += 1

    except TwitterSearchException as e:
        print(e)


# GUI

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = ImageTk.PhotoImage(Image.open('space.jpg'))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.05, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Find Polarity", font=40, command=lambda: find_polarity(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.20, relwidth=0.90, relheight=0.75, anchor='n')

label = tk.Label(lower_frame, anchor='nw', justify='left', bd=4)
label.place(relwidth=1, relheight=1)


root.mainloop()
