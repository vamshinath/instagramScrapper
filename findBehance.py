#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
from datetime import datetime
from pymongo import MongoClient
import requests

usrag = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"


name = input("Enter Act:")

client = MongoClient("localhost")["instagram"][name]


# In[2]:


posts = list(client.find({"data":1,"viewed":False,"mentions":{"$regex":"@"}}).sort("likes",-1))
for post in posts:
    # chrome.get(post["_id"])
    # input()
    # client.update_one({"_id":post["_id"]},{"$set":{"viewed":True}})
    words=post["mentions"].split()
    ids=list(filter(lambda x: x.startswith("@"),words))
    
    for id in ids:
        try:
            tries=5
            while tries != 0:
                try:
                    uri = "https://www.instagram.com/"+id[1:]
                    status = "behance" in requests.get(uri,headers={"User-Agent":usrag}).text
                    break
                except Exception as e:
                    time.sleep(2)
                    print("next try")
                    status = "behance" in requests.get(uri,headers={"User-Agent":usrag}).text
                tries-=1

            if status :
                print(uri)

            try:
                if status:
                    try:
                        MongoClient("localhost")["instagram"]["people"].insert_one({"_id":uri,"behance":status,"count":1})
                    except Exception as e:
                        pct = int(list(MongoClient("localhost")["instagram"]["people"].find({"_id":uri}))[0]["count"])

                        MongoClient("localhost")["instagram"]["people"].update_one({"_id":uri},{"$set":{"behance":status,"count":pct+1}})
                else:
                    MongoClient("localhost")["instagram"]["people"].insert_one({"_id":uri,"behance":status,"count":1})
            except Exception as e:
                pct = int(list(MongoClient("localhost")["instagram"]["people"].find({"_id":uri}))[0]["count"])
                MongoClient("localhost")["instagram"]["people"].update_one({"_id":uri},{"$set":{"behance":status,"count":pct+1}})
        except Exception as e:
            print(e)
            break
# In[ ]:




