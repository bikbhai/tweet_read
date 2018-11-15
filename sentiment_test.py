import re 
import sys,os
sys.path.append('/usr/local/lib/python3.5/dist-packages')
from textblob import TextBlob 
import pandas as pd
import json


def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\\w+:\\/\\/\\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return analysis,'positive'
    elif analysis.sentiment.polarity == 0: 
        return analysis,'neutral'
    else: 
        return analysis,'negative' 


def tweet_analysis(tweet_text):
	tweet_list=list()
	sentiment_list=list()
	for tweet in tweet_text:
		tweet_str,sentiment_str=get_tweet_sentiment(tweet)
		tweet_list.append(tweet_str)
		sentiment_list.append(sentiment_str)
		#print(tweet_str," ",sentiment_str)

	return tweet_list,sentiment_list

#---Get the sentiment percentage(%positine,%negative,%neutral)---
def get_sentiment_percentage(sentiment_list):
	neutral_count=0
	positive_count=0
	negative_count=0
	for sen_str in sentiment_list:
		if sen_str.lower().strip()=="neutral":
			neutral_count=neutral_count+1
		elif sen_str.lower().strip()=="positive":
			positive_count=positive_count+1
		else:
			negative_count=negative_count+1
	print("Neutral percentage ",((neutral_count/len(sentiment_list)*100)))
	print("positive percentage ",((positive_count/len(sentiment_list)*100)))
	print("Negative percentage ",((negative_count/len(sentiment_list)*100)))


def main():
	df=pd.read_csv("tweets_india.csv")
	tweet_list,sentiment_list=tweet_analysis(df.tweet_text)
	df_tweet=pd.DataFrame()
	df_tweet['tweet']=tweet_list
	df_tweet['sentiment']=sentiment_list
	df_tweet.to_csv("sentiment_analysis.csv",index=False)
	get_sentiment_percentage(sentiment_list)

main()
