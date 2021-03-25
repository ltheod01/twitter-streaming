from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import re
from csv import writer
import csv
from numpy import log as ln
n = 0

header_name = ['Google', 'Tesla']
with open('sentiment.csv','w') as file:
    writer=csv.DictWriter(file, fieldnames=header_name)
    writer.writeheader()

score_variable1 = 0
score_variable2 = 0    
#Basic listener class that just imports the received tweets to the CSV file
class StdOutListener(StreamListener):

#####Data includes all data for the relevant tweet.  We can use data to get viewers, likes etc
    def __init__(self, search1, search2, associated_search1_list, associated_search2_list):
       self.var1 = search1
       self.var2 = search2
       self.assvar1 = associated_search1_list
       self.assvar2 = associated_search2_list
    
    def on_data(self,data):
        raw_twitts = json.loads(data)

        followers = (raw_twitts["user"]["followers_count"])
        followers=ln(followers) if followers>0 else 1
            
            
        try:
            tweets = raw_twitts['text']
            #We turn the tweets to readable text by python.
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\s+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT', ' ', tweets).split())

            blob=TextBlob(tweets.strip())

            global score_variable1
            global score_variable2
            global n

            for sent in blob.sentences:
                
                intersection_set3 = set.intersection(set(sent.lower().split()), set(self.assvar1), set(self.assvar2))
                intersection_set21 = set.intersection(set(sent.lower().split()), set(self.assvar1))
                intersection_set22 = set.intersection(set(sent.lower().split()), set(self.assvar2))
                sentiment = sent.sentiment.polarity

                
                if not len(intersection_set3)==0:
                    score_variable1 += followers*sentiment
                    score_variable2 += followers*sentiment    
                elif len(intersection_set21)!=0:
                    score_variable1 += followers*sentiment
                elif len(intersection_set22)!=0:
                    score_variable2 = score_variable2 + followers*sentiment



            with open('sentiment.csv','a') as file:
                writer = csv.DictWriter(file, fieldnames = header_name)
                info = {self.var1: score_variable1, self.var2: score_variable2}
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
