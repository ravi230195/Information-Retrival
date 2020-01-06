#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 21:21:50 2019

@author: ravik
"""
from twarc import Twarc
import json
import tweepy
import json
import time
from datetime import datetime
from datetime import timedelta
import demoji

india_list = ["narendramodi", "BDUTT", "sardesairajdeep", "AmitShah", "SrBachchan"]
#name_list= ["jaketapper", "andersoncooper", "maddow", "AmitShah"]
usa_list1 = ["realDonaldTrump"]
usa_list = ["SenSanders"]
#[ "JoeBiden", "jaketapper", "andersoncooper", "maddow", "BuzzFeedBen"]
brazil_list = ["jairbolsonaro", "BolsonaroSP", "deltanmd", "alex_borges"]


consumer_key = "V4IIziI3Wz4q49NQU9olkzw98"
consumer_secret =  "2x8Q0WyWNV86XEWRAuYhJB0kUu4M9BosgemxMjnPbiu00t5HE7"
access_key = "602847795-0GJCA5vujrexWTCfK6ZtxZD2MZ8pCuA1zBKO5fNa"
access_secret = "6cN8sgBp7DiDITJbg0uCSlWoeY84YoLJs5HOxzxmqtjEj"


prev_date = timedelta(days=10)
today = datetime.now().date()
time_range = today - prev_date

t = Twarc(consumer_key, consumer_secret, access_key, access_secret)
for name in usa_list:
    print(name)
    file_name = r"C:\\Users\\ravik\\OneDrive\\Desktop\\UsertimelineReplies\\" + str(name) + ".json"
    max_poi_tweet = 0
    with open( file_name, "a", encoding='utf-8') as file:
        for tweet in t.timeline(screen_name=name):
            if 'retweeted_status' in tweet.keys():
                print("Its a retweet")
                continue
            if max_poi_tweet > 3000:
                break
            json.dump(tweet, file,  ensure_ascii=False)
            file.write("\n")
            max_poi_tweet +=1
            max_replies = 0
            if datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y").date() >= time_range:
                for reply in t.replies(tweet):
                    #print("In")
                    #preprocessing(tweet, file)
                    if 'retweeted_status' in tweet.keys():
                        print("Its a retweet")
                        continue
                    else:
                        json.dump(reply, file,  ensure_ascii=False)
                        file.write("\n")
                        max_replies +=1
                        print("{} tweet {} reply number {}".format(name, max_poi_tweet, max_replies))
                        if max_replies > 21:
                            break
            else:
                print("{} tweet {} Date didnt satisfy".format(name, max_poi_tweet))
#time.sleep(10)
#preprocessing(file_name, file_processed)


# In[ ]:




