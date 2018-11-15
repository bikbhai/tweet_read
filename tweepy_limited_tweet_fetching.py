import sys,os
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import csv
import tweepy
from tweepy import StreamListener,Stream
from datetime import datetime
from logger_config import *
import logger_config
import pandas as pd

## Twitter credentials
CONSUMER_KEY = "bezNRWxWzcloXMNaedkZYzMij"
CONSUMER_SECRET = "2WSPYdZvsp3XJ1UIgELQN7Qppuhxts6GJBjfJc9wD14Dh5lktV"
ACCESS_TOKEN = "1062335738723745792-30gESiVR2MgJF6KumGYwAYAfVXZ9Lj"
ACCESS_TOKEN_SECRET = "ctCX8HMNTfYKrMTPFzIDw3CMhgshGHyha7PUjpBTafdDk"

#---Query tag---
QUERY="cyclone gaja"

#---Configuring log filename---
log_file=os.path.splitext(os.path.basename(__file__))[0]+".log"
log = logger_config.configure_logger('default', ""+DIR+""+LOG_DIR+"/"+log_file+"")

 

#---Authenticate using api credentials--- 
def get_twitter_api_access():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	return auth

#---Get the actual interface using authentication---
def get_api_interface(auth):
	return tweepy.API(auth)

#---Get details of the user---
def get_user_details(user):
	print(user.name)
	print(user.friends_count)

#---Fetch tweets corresponding to given keyword---
def get_tweets(api,query,count):
	tweet_list=list()
	time_list=list()
	location_list=list()
	fetch_tweets=api.search(q=query,count=count)
	for tweet in fetch_tweets:
		tweet_list.append(tweet.text)
		time_list.append(str(datetime.now().strftime('%d/%m/%Y  %H:%M:%S')))
		location_list.append(tweet.user.location)
		#print(tweet.text)
		#print(tweet.user.location)
	return tweet_list,time_list,location_list

#---Create a csv file--- 
def create_csv_file(tweet_list,time_list,location_list):
	df=pd.DataFrame()
	df["tweets"]=tweet_list
	df["time"]=time_list
	df["location"]=location_list

	df.to_csv(QUERY+"_tweet_location.csv",index=False)
	return "csv file created"

#---Main function--- 
def main():
	try:
		auth=get_twitter_api_access()
		api=get_api_interface(auth)
		#get_user_details(api.me())
		tweet_list,time_list,location_list=get_tweets(api,query = QUERY, count = 200)
		status=create_csv_file(tweet_list,time_list,location_list)
		log.info(status)
	except Exception as e:
		log.error(e)

#---Main function called---
if __name__ == '__main__':
	
	try:
		main()
	except:
		pass
	
	