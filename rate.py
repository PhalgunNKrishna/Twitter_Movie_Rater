from TwitterSearch import *
from textblob import TextBlob
import pandas as pd
import re
#import numpy as np
#from GUI import text

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

except TwitterSearchException as e:
    print(e)





