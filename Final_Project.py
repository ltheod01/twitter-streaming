######IMPORTING THE RELEVANT LIBRARIES#######
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from csv import writer
import json
from textblob import TextBlob
import re
import csv


#This is the file where you store your twitter user_credentials
import your_twitter_credentials

#This part is to take care of emojis & characters that are outside
#the BMP (Basic Multilingual Plane)
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


#Pass the authenticate codes to access the twitter api.  Those were saved on another
#program called twitter_credentials which you need to create including your credentials to access twitter.
auth = tweepy.OAuthHandler(your_twitter_credentials.CONSUMER_KEY, your_twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(your_twitter_credentials.ACCESS_TOKEN, your_twitter_credentials.ACCESS_TOKEN_SECRET)

n = 0

#Opening the csv file to write the data in order to plot them in another program
header_name = ['Dogecoin', 'Bitcoin']
with open('sentiment.csv','w') as file:
    writer=csv.DictWriter(file, fieldnames=header_name)
    writer.writeheader()

btc = 0
doge = 0
variable1_lib = ['Bitcoin', 'BTC','bitcoin', 'BITOCIN']
variable2_lib = ['Doge', 'doge', 'dogecoin','DOGE']
    
#Basic listener class that just imports the received tweets to the CSV file
class StdOutListener(StreamListener):


#####Data includes all data for the relevant tweet.  We can use data to get viewers, likes etc
#####Text = (status.text.translate(non_bmp_map))
#####Follower = str(status.user.followers_count)
#####Name = status.author.screen_name

    def on_status(self,status):
        followers = json.loads(status)
        print(followers['followers_count'])

    def on_data(self,data):
        raw_twitts = json.loads(data)
        
        try:
            tweets = raw_twitts['text']
            #We turn the tweets to readable text by python.
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\s+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT', ' ', tweets).split())

            blob=TextBlob(tweets.strip())

            global btc
            global n
            global doge
            global variable1_lib
            global variable2_lib
            global positive_wording
            global negative_wording

            score_variable1 = 0
            score_variable2 = 0

###########Iritate through each tweet and add score depending upon the sentiment and the number of likes######### 
            for sent in blob.sentences:
                sentiment = sent.sentiment.polarity
                for word in sent.split():
                    if word in variable1_lib:
                        score_variable1 += 1*sentiment
                    elif word in variable2_lib:
                        score_variable2 += 1*sentiment

            btc = btc + score_variable1
            doge = doge +score_variable2

            with open('sentiment.csv','a') as file:
                writer = csv.DictWriter(file, fieldnames = header_name)
                info = {'Dogecoin': doge, 'Bitcoin': btc}
                writer.writerow(info)

            print('Tweet number:', n)
            n+=1
            
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
        
    def on_error(self,status):
        if status==420:
            #Returning false on_data method in case rate limit occurs.
            return False
        print(status)


myStream = tweepy.Stream(auth, StdOutListener())
myStream.filter(track =['Bitcoin', 'BTC','bitcoin', 'BITOCIN', 'Doge', 'doge', 'dogecoin','DOGE'])
