"""
Created on Fri Sep 13 21:21:50 2019

@author: ravik
"""
from twarc import Twarc
import json
import json
import time
from datetime import datetime
from datetime import timedelta
import demoji
demoji.download_codes()

india_list = ["narendramodi", "BDUTT", "sardesairajdeep", "AmitShah", "SrBachchan"]
#name_list= ["jaketapper", "andersoncooper", "maddow", "AmitShah"]
usa_list1 = ["realDonaldTrump"]
usa_list = [ "BuzzFeedBen", "JoeBiden", "jaketapper", "andersoncooper", "maddow"]
brazil_list = ["jairbolsonaro", "BolsonaroSP", "deltanmd", "alex_borges", "LulaOficial"]

consumer_key = "l1JlcysJ830aG3xpopIs6J59E"
consumer_secret =  "sb0AJlnwlby1y2osQQ0Entl3iiTE2XDev1lkQn9m1N7wOMnQct"
access_key = "1172907669763579904-oEZ14ivUHSOr9DskIzE0GwSrvfCVyL"
access_secret = "NYmi40hpZwkyqOwwX1zdDnLp69LGtLfBQY6YnVBLUPy2X"

name_list= ["#bjp","#BJP"]
#["#hillaryclinton","#hillary","#clinton"]

prev_date = timedelta(days=5)
today = datetime.now().date()
time_range = today - prev_date
name_poi = "narendramodi"
file_name = r"C:\\Users\\ravik\\OneDrive\\Desktop\\tweet_new\\IndianHashtags\\" + name_poi+ "lang.json"
file_processed = r"C:\\Users\\ravik\\OneDrive\\Desktop\\tweet_new\\IndianHashtags\\" + name_poi+ "_langprocess.json"
def preprocessing(file, file_processed):
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
                break
            if tweet_dic['in_reply_to_status_id'] is not None:
                #print("hereh")
                tweet_dic['reply_text'] = tweet_dic['full_text']
            else:
                #print("here")
                tweet_dic['reply_text'] = None
            tweet_dic['entities']['hashtags'][0]['text'] = name_poi              #CHANGE
            tweet_dic['poi_name'] = name_poi                                     #CHANGE
            tweet_dic['poi_id'] = 18839785
            tweet_dic['user']['verified'] = False                                #CHANGE
            print(tweet_dic['poi_name'])
            tweet_dic['country'] = "India"
            full_text = tweet_dic['full_text']
            tweet_dic['text_copy'] = demoji.replace(full_text)
            tweet_dic['tweet_emotions'] = list(demoji.findall(full_text).keys())
            json.dump(tweet_dic, fp, ensure_ascii = False)
            fp.write("\n")


t = Twarc(consumer_key, consumer_secret, access_key, access_secret)
max_number = 0
for name in name_list:
    print(name)
    with open( file_name, "a", encoding='utf-8') as file:
        for tweet in t.search(q = str(name), lang='hi'):
            #print("In")
            #preprocessing(tweet, file)
            if 'retweeted_status' in tweet.keys():
                print("Its a retweet")
                continue
            else:
                json.dump(tweet, file,  ensure_ascii=False)
                file.write("\n")
                max_number +=1
                print("{} number {}".format(name, max_number))
                if max_number > 2500:
                    break
time.sleep(10)
preprocessing(file_name, file_processed)