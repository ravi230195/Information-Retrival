import json
import datetime
import demoji

usa_list = ["realDonaldTrump", "jaketapper", "andersoncooper", "maddow"]
brazil_list = ["jairbolsonaro", "BolsonaroSP", "deltanmd", "alex_borges"]
india_list = ["BDUTT", "sardesairajdeep", "AmitShah", "SrBachchan", "narendramodi"]

with open(r"/home/ubuntu/solr-8.2.0/n.json", 'r+', encoding='utf-8') as file, open(r"/home/ubuntu/solr-8.2.0/preprocess.json", 'a', encoding='utf-8') as pre:
        i = file.read().splitlines()
        print(len(i))
        for tweet in range(0, len(i)):
            tweet_dic = json.loads(i[tweet])
            #date
            date= datetime.datetime.strptime(tweet_dic["created_at"], "%a %b %d %H:%M:%S %z %Y").date()
            #reply_text, poi_id, poi_name
            tweet_dic['tweet_date'] = str(date)+ "T" + date.strftime("%H:%M:%SZ")
            if tweet_dic['in_reply_to_status_id'] is not None:
                print("hereh")
                tweet_dic['poi_name'] = tweet_dic['in_reply_to_screen_name']
                tweet_dic['reply_text'] = tweet_dic['full_text']
                tweet_dic['poi_id'] = tweet_dic['in_reply_to_user_id']
            else:
                print("here")
                tweet_dic['poi_name'] = tweet_dic['user']['screen_name']
                tweet_dic['poi_id'] = tweet_dic['user']['id']
                tweet_dic['reply_text'] = None
                print(tweet_dic['poi_name'])
            #country
            screen_name = tweet_dic['poi_name']
            if screen_name in india_list:
                tweet_dic['country'] = "India"
            elif screen_name in usa_list:
                tweet_dic['country'] = 'USA'
            elif screen_name in brazil_list:
                tweet_dic['country'] = 'brazil'
            else:
                print("error poi{}".format(tweet_dic['id']))
            #text_xx
            text_xx = "text_" + str(tweet_dic['lang'])
            full_text = tweet_dic['full_text']
            tweet_dic[text_xx] = demoji.replace(full_text)
            tweet_dic['tweet_emotions'] = list(demoji.findall(full_text).keys())
            json.dump(tweet_dic,pre,sort_keys=True,ensure_ascii = False)
            pre.write("\n")

