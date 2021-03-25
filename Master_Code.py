######IMPORTING THE RELEVANT LIBRARIES#######
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import twitter_credentials
from csv import writer
import csv

from stdoutlistener import StdOutListener

#Pass the authenticate codes to access the twitter api.  Those were saved on another
#program called twitter_credentials
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)


#Opening the csv file to write the data in order to plot them in another program
header_name = ['Google', 'Tesla']
with open('sentiment.csv','w') as file:
    writer=csv.DictWriter(file, fieldnames=header_name)
    writer.writeheader()


variable1_lib = ['alfabet', 'alphabet', 'googl', 'google', 'goolge', 'gkoukle']
variable2_lib = ['tesla', 'tsla', 'telsa']
tracklist = variable1_lib + variable2_lib


myStream = tweepy.Stream(auth, StdOutListener("Google", "Tesla", variable1_lib, variable2_lib))
myStream.filter(track = tracklist)
