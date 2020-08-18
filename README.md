# Twitter_Movie_Rater  

By Phalgun Krishna and Ryan Bui  

A side project that rates movies based on tweets by utlizing sentiment analysis, a type of natural language processing. This project includes a GUI for users to easily input movie titles as well as the 5 most popular tweets, 5 most negative tweets, and 5 most positive tweets about the movie.


# Instructions to Run Project  
**1.** Make sure you have all the necessary packages we used in our implementations of standard.py and premium.py. If not, run the following command:  
```c
pip install --user --requirement requirements.txt  
```  
**2.** Run either of the two .py files, standard.py or premium.py using the command: 
```c 
python standard.py
``` 
or  

```c
python premium.py
```  
**Note:** standard.py utilizes the standard Twitter developer account subscription. The advantage in using standard.py is that Twitter API calls are limitless when using it. However, the disadvantages to using this program are that it can only collect tweets published in the past 30 days and runs noticeably slower than premium.py. While premium.py runs faster than standard.py and collects tweets dating to 2006, only 50 API calls can be made a month. **Therefore, please use premium.py sparingly.**  
**3.** A python GUI will appear. Enter the movie title at the top and click "Find Polarity"  
**4.** The top 5 most positive tweets, negative tweets, popular tweets will show in the GUI as well as the average polarity and overall rating of the movie will appear in the GUI. This information along with the polarity of the 15 showcased tweets is also displayed on Terminal.

# Overview of the Project

## standard.py packages used
With regard to standard.py, we found that the TwitterSearch and Tweepy packages worked best in tandem. Because TwitterSearch could only find tweets written in the last 30 days, it was perfectly suitable for the most basic developer account functions needed in standard.py. Tweepy was then used to to identify the tweet object corresponding to the tweet text found by TwitterSearch. The tweet object was needed to find the tweet's retweet status. A tweet's retweet status, the number of favorites it got, and number of retweets it had were all needed to scale the tweet's polarity. This polarity scaling based on popularity is detailed later in this README.  

The following snippet of code shows the metadata of the tweet and how the TwitterSearch and Tweepy packages were used: 

```c
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
```
## premium.py packages used
We could not use TwitterSearch for premium.py because it could only retrieve tweets published in the past 30 days. Therefore we used the searchtweets package as it was developed especially for premium developer accounts. We used the Medium article, https://medium.com/swlh/extracting-tweets-using-twitter-premium-search-api-and-python-2d025144e8a4 ,  to guide our use of searchtweets. The article also explains why the .yaml file was needed for premium.py. The tweepy package was again used to find the retweet status of tweets found through searchtwitter.


## Properties Common to Both Programs
As mentioned earlier, a tweet's polarity (the tone of the tweet's message) was scaled based on how popular it was with other users.  
Our scaling algorithm is shown here:

```c
pol_count = 0.0
    for i in df.index:
        pol_count += df['Polarity'][i] * df['Number of Favorites'][i] + df['Polarity'][i] * 2.0 * df['Number of Retweets'][i]
        pol_count += df['Polarity'][i]
        avg_pol = float(pol_count/50.0)
```  

While this algorithm was original, the clean_text(), Polarity(), and idea to use dataframes were all taken from the YouTube video:  
https://www.youtube.com/watch?v=ujId4ipkBio&fbclid=IwAR3k1Y7ApJsGTCBB6sUjhVGmOWZbbcNE97_8pEXjl-EPMtPtlRYHolXTwfA
