import sys,os
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import csv
import tweepy
from tweepy import StreamListener,Stream
from datetime import datetime
from logger_config import *
import logger_config

## Twitter credentials
CONSUMER_KEY = "bezNRWxWzcloXMNaedkZYzMij"
CONSUMER_SECRET = "2WSPYdZvsp3XJ1UIgELQN7Qppuhxts6GJBjfJc9wD14Dh5lktV"
ACCESS_TOKEN = "1062335738723745792-30gESiVR2MgJF6KumGYwAYAfVXZ9Lj"
ACCESS_TOKEN_SECRET = "ctCX8HMNTfYKrMTPFzIDw3CMhgshGHyha7PUjpBTafdDk"

#---Query---
QUERY='cyclone gaja'

#---Configuring log filename---
log_file=os.path.splitext(os.path.basename(__file__))[0]+".log"
log = logger_config.configure_logger('default', ""+DIR+""+LOG_DIR+"/"+log_file+"")

#---Class for listening live streams---
class StdOutListener(StreamListener):
    def on_status(self, status):
    # Prints the text of the tweet
        tweet_str=str(status.text)
        tweet_location=str(status.user.location)
        log.info(tweet_str)
        time_str=str(datetime.now().strftime('%d/%m/%Y  %H:%M:%S'))
        with open(QUERY+'_tweets_.csv','a') as writeFile:
        	writer=csv.writer(writeFile)
        	writer.writerow([tweet_str,time_str,tweet_location])

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening
 

#---Authenticate using api credentials--- 
def get_twitter_api_access():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	return auth

#---Get live streaming tweets---
def get_live_streams(auth, listener):
	stream = Stream(auth, listener)
	stream.filter(track=[QUERY])

#---Main function--- 
def main():
	try:
		listener = StdOutListener()
		auth=get_twitter_api_access()
		get_live_streams(auth,listener)
	except Exception as e:
		log.error(e)

#---Main function called---
if __name__ == '__main__':
	while True:	
		try:
			main()
		except:
			pass
	
	