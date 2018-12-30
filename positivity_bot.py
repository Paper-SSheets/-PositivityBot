import tweepy
import time
import random

# This is where we'll actually store the #positivity
from positive_sayings import *

# @see keys.py - These are the Twitter-generated keys for your program.
from keys import *

# NOTE: flush = True is just for running this		#
# script with PythonAnywhere's always-on task.		#
# https://help.pythonanywhere.com/pages/AlwaysOnTasks/	#
print('this is my twitter bot', flush = True)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush = True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
	
    #  NOTE: We need to use tweet_mode = 'extended'	#
    #  below to show all full tweets (with full_text).	#
    #  Without it, long tweets would be cut off.	#
    mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')
	
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#positivity' in mention.full_text.lower():
            print('found #positivity!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + ' ' + 
			random.choice(positive_sayings) + '#positivity', mention.id)	

# This will keep the bot activated, however, you need 
# to pay to keep the script going. See YouTube links.
while True:
    reply_to_tweets()
    time.sleep(10)
