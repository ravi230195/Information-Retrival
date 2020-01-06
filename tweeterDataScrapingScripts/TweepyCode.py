# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 18:10:22 2019

@author: ravik
"""

import tweepy
import json
import time
from datetime import datetime
from datetime import timedelta
import demoji

india_list = ["BDUTT", "sardesairajdeep", "AmitShah", "SrBachchan", "narendramodi"]
#name_list= ["jaketapper", "andersoncooper", "maddow", "AmitShah"]
usa_list1 = ["realDonaldTrump"]
usa_list = [ "BuzzFeedBen", "JoeBiden", "jaketapper", "andersoncooper", "maddow"]
brazil_list = ["jairbolsonaro", "BolsonaroSP", "deltanmd", "alex_borges"]
demoji.download_codes()

    
def preprocessing(i, file, userList):
    tweet_dic = json.loads(i)
    #date
    date= time.strftime('%Y-%m-%dT%H:00:00Z',time.strptime(tweet_dic["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))
    format_str = '%Y-%m-%dT%H:00:00Z'
    dt = datetime.strptime(date, format_str)
    final = dt + timedelta(hours=1)
    #reply_text, poi_id, poi_name
    tweet_dic['tweet_date'] = final.strftime(format_str)
    if('full_text' in tweet_dic.keys()):
        print("tweet has full_text")
    elif('text' in tweet_dic.keys()):
        print("has text instead of full_text")
        tweet_dic['full_text'] = tweet_dic['text']
    else:
        print("No full_text or text")
        return
    if tweet_dic['in_reply_to_status_id'] is not None:
        #print("wkefnwlm")
        if tweet_dic['in_reply_to_screen_name'] not in userList:
            tweet_dic['poi_name'] = tweet_dic['user']['screen_name']
            tweet_dic['poi_id'] = tweet_dic['user']['id']
        else:
            tweet_dic['poi_name'] = tweet_dic['in_reply_to_screen_name']
            tweet_dic['poi_id'] = tweet_dic['in_reply_to_user_id']
        tweet_dic['reply_text'] = tweet_dic['full_text']
    else:
        #print("welfnwelknfdwm")
        #print(tweet_dic)
        tweet_dic['poi_name'] = tweet_dic['user']['screen_name']
        tweet_dic['poi_id'] = tweet_dic['user']['id']
        tweet_dic['reply_text'] = None
    print(tweet_dic['poi_name'])
    #country
    screen_name = tweet_dic['poi_name']
    tweet_dic['country'] = "India"
    if screen_name in india_list:
        tweet_dic['country'] = "India"
    elif screen_name in usa_list:
        tweet_dic['country'] = 'USA'
    elif screen_name in brazil_list:
        tweet_dic['country'] = 'brazil'
    else:
        print("error poi {}".format(tweet_dic['id']))
    #text_xx
    #text_xx = "text_" + str(tweet_dic['lang'])
    full_text = tweet_dic['full_text']
    tweet_dic['text_copy'] = demoji.replace(full_text)
    tweet_dic['tweet_emotions'] = list(demoji.findall(full_text).keys())
    #time.sleep(1)
    json.dump(tweet_dic, file, ensure_ascii = False)
    #time.sleep(5)
    file.write("\n")



def getReplies(api, i, status_id_str, file_replies, query, numReplies = 0):
        #query = "to:" + str(i) + " since_id:" + str(status_id_str) + " filter:replies"
        #if query_sent != "":
            #query = query_sent 
        replies = tweepy.Cursor(api.search, q=query, tweet_mode = "extented").items(100)
        number_replies = numReplies
        #reply_first = replies.next()
        print("AGAIN TRYING")
        
        while True:
            try:
                reply = replies.next()
                #print(reply.id_str)
                #reply_prev = reply.id_s
                reply_prev = reply.id_str
                #print("trying this tweet id{}".format(reply.id_str))
                if not hasattr(reply, 'in_reply_to_status_id_str'):     
                    continue
                if reply.in_reply_to_status_id_str == status_id_str:
                    #print("here")
                    json.dump(reply._json,file_replies, ensure_ascii=False)
                    file_replies.write("\n")
                    print("{}  {}  reply count {} and tweet id {}".format(i, status_id_str, number_replies, reply.id_str))
                    
                    if number_replies > 20:
                        return
                    number_replies = number_replies + 1
    
            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached{}".format(e))
                time.sleep(60)
                continue
    
            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                time.sleep(60)
                continue
    
            except StopIteration:
                #print("here")
                if number_replies < 20:
                    print(number_replies)
                    getReplies(api, i, reply_prev, file_replies, "to:" + str(i) + " max_id:" + str(reply_prev) + " filter:replies", number_replies)
                break
    
            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                time.sleep(60)
                continue


def forUserTimeline(userList, api, file_name, file_name_replies, replies_needed):
    for i in userList:
        user_tweet = 1
        with open(file_name + str(i) + ".json", "a", encoding='utf-8') as file:
            for status in tweepy.Cursor(api.user_timeline, screen_name= i , tweet_mode="extended").items(3100):
                if not hasattr(status, 'retweeted_status'):
                    #print((status['id']))
                    preprocessing(json.dumps(status._json,ensure_ascii=False), file, userList)
                    #json.dump(status._json,file, ensure_ascii=False)
                    #file.write("\n")
                    print("tweet number:{} and {}".format(user_tweet,  status.id_str))
                    user_tweet = user_tweet + 1
                    #if replies_needed:
                        #if datetime.datetime.strptime(status.created_at, "%a %b %d %H:%M:%S %z %Y").date() >= time_range:#    getReplies(api, i, status.id_str, file_replies, "to:" + str(i) + " since_id:" + str(status.id_str) + " filter:replies")


def forHashTags(api, file_name, query, maxid, total_hashtagsCount = 0):
    total_count = total_hashtagsCount
    tweet_prev = 0
    with open(file_name + str(query) + ".json", "a", encoding='utf-8') as file:
        if maxid == -1:
            tweets = tweepy.Cursor(api.search, q= query, tweet_mode="extended").items(100)
        else:
            tweets = tweepy.Cursor(api.search, q= query, max_id= maxid, tweet_mode = "extented").items(100)
        print("AGAIN TRYING")
        while True:
            try:
                #print("here")
                tweet = tweets.next()
                tweet_prev = tweet.id
                #print(tweet_prev)
                if not hasattr(tweet, 'retweeted_status'):
                    #preprocessing(json.dumps(tweet._json,ensure_ascii=False), file)
                    json.dump(tweet._json,file, ensure_ascii=False)
                    file.write("\n")                        
                    total_count +=1
            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached{}".format(e))
                time.sleep(60)
                continue
    
            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                time.sleep(60)
                continue
    
            except StopIteration:
                #print("here")
                if total_count < 130 and tweet_prev != 0:
                    print(total_count)
                    forHashTags(api, file_name, str(query), tweet_prev - 1, total_count)
                elif tweet_prev == 0:
                    forHashTags(api, file_name, str(query), tweet_prev - 100, total_count)
                break
    
            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                time.sleep(60)
                continue



consumer_key = "SMQAn8XCg0JbfkJ4c1Mx50xtn"
consumer_secret =  "nO7I3themPyGKVsY0XldRIsYxp2jarnfuu2RVvSYiIypjbxChs"
access_key = "1167195181235544064-kLI0EFxKXiHok2wrtYUO6dg68WXqxO"
access_secret = "dPYbXihAeDzPwa8HRcsJfnaTtIwbTh26BpkpyLDhXNpEi"


#prev_date = datetime.timedelta(days=4)
#today = datetime.datetime.now().date()
#time_range = today - prev_date

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

file_name =  r"C:\\Users\\ravik\\OneDrive\\Desktop\\IR\\tweet\\tweet_new\\User_timeline\\Usertimeline\\"
file_name_replies =  r"C:\\Users\\ravik\\OneDrive\\Desktop\\IR\\tweet\\tweet_new\\User_timeline\\"
HashTags = [ "#barkha"]#, "#AmitShah", "#Bachan","#rajdeep", "#modi"]
HashTags1 = ["rachelmaddow", "andersoncooper", "jaketapper", "JeoBiden"]
#hashtag = "#modi OR #AMITABH"
#forHashTags(indian_list, api, file_name)
forUserTimeline(usa_list, api, file_name, file_name_replies, False)
forUserTimeline(brazil_list, api, file_name, file_name_replies, False)
forUserTimeline(india_list, api, file_name, file_name_replies, False)
#for i in HashTags:
#    forHashTags(api, file_name, i, -1,  0)

#for i in HashTags:
#    forHashTags(api, file_name, i, -1, 0)