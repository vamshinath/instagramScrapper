#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
from datetime import datetime
from pymongo import MongoClient

name = input("Enter Act:")

chrome = webdriver.Chrome("/home/kdemac/chromedriver")

client = MongoClient("localhost")["instagram"][name]



def downloadImg():

    link=''
    imgs=chrome.find_elements_by_tag_name("img")
    for img in imgs:
        try:
            if "s150x" not in img.get_attribute("src"):
                link=img.get_attribute("src")
                chrome.get(link)
                time.sleep(2)
                print(link)
                break
        except Exception as e:
            e=0

# In[2]:

#"mentions":{"$regex":"@"}
posts = list(client.find({"data":1,"viewed":False}).sort("likes",-1))
for post in posts:
    chrome.get(post["_id"])
    opt=input("d for download:")
    if opt == "d":
        downloadImg()
    client.update_one({"_id":post["_id"]},{"$set":{"viewed":True}})


# In[ ]:




