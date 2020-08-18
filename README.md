# Twitter_Movie_Rater  

By Phalgun Krishna and Ryan Bui  

A side project that rates movies based on tweets by utlizing sentiment analysis, a type of natural language processing. This project includes a GUI for users to easily input movie titles as well as the 5 most popular tweets, 5 most negative tweets, and 5 most positive tweets about the movie.


## Instructions to Run Project  
1. Make sure you have all the necessary packages we used in our implementations of standard.py and premium.py. If not, run the following command:  
```c
pip install --user --requirement requirements.txt  
```  
2. Run either of the two .py files, standard.py or premium.py using the command: 
```c 
python standard.py
``` or  
```c
python premium.py
```  
**Note:** standard.py utilizes the standard Twitter developer account subscription. The advantage in using standard.py is that Twitter API calls are limitless when using it. However, the disadvantages to using this program are that it can only collect tweets published in the past 30 days and runs noticeably slower than premium.py. While premium.py runs faster than standard.py and collects tweets dating to 2006, only 50 API calls can be made a month. **Therefore, please use premium.py sparingly.**  
3. A python GUI will appear. Enter the movie title at the top and click "Find Polarity"  
4. The top 5 most positive tweets, negative tweets, popular tweets will show in the GUI as well as the average polarity and overall rating of the movie will appear in the GUI. This information along with the polarity of the 15 showcased tweets is also displayed on Terminal.
