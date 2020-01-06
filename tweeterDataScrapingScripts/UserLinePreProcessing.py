#!/usr/bin/env python
# coding: utf-8

# In[14]:


from twarc import Twarc
import json
import tweepy
import json
import time
from datetime import datetime
from datetime import timedelta
import demoji

india_list = ["SenSanders"]#, "AmitShah", "SrBachchan"]"narendramodi", "BDUTT", 
#name_list= ["jaketapper", "andersoncooper", "maddow", "AmitShah"]
usa_list = ["JoeBiden", "jaketapper", "maddow"]
#["HillaryClinton", ["SenSanders", "JoeBiden", "jaketapper", "maddow"]
brazil_list = ["jairbolsonaro", "BolsonaroSP", "deltanmd", "alex_borges", "LulaOficial"]
demoji.download_codes()

def preprocessing(file, file_processed, userList):
    with open(file, "r", encoding='utf-8') as f, open(file_processed, "a", encoding='utf-8') as fp:
        lines = f.readlines()
        for line in lines:
            tweet_dic = json.loads(line)
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
            #tweet_dic['country'] = "India"
            if screen_name in india_list:
                tweet_dic['country'] = "India"
            elif screen_name in usa_list:
                tweet_dic['country'] = 'USA'
            elif screen_name in brazil_list:
                tweet_dic['country'] = 'Brazil'
            else:
                print("error poi {}".format(tweet_dic['id']))
            print(tweet_dic['country'])
            full_text = tweet_dic['full_text']
            tweet_dic['text_copy'] = demoji.replace(full_text)
            tweet_dic['tweet_emotions'] = list(demoji.findall(full_text).keys())
            #time.sleep(1)
            json.dump(tweet_dic, fp, ensure_ascii = False)
            #time.sleep(5)
            fp.write("\n")

file_name = r"C:\\Users\\ravik\\OneDrive\\Desktop\\UsertimelineReplies\\"

for name in india_list:
    file = file_name + str(name) + ".json"
    file_processed = file_name + str(name) + "_processed.json"
    preprocessing(file, file_processed, india_list)


# In[ ]:





# In[ ]:




