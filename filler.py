#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
from datetime import datetime
from pymongo import MongoClient
chrome = webdriver.Chrome("/home/kdemac/chromedriver")

name = input("Enter Act:")


client = MongoClient("localhost")["instagram"][name]


# In[2]:


posts = list(client.find({"data":0}))


# In[8]:


def fillPost(url):
    mentions = chrome.find_element_by_tag_name("li").text
    tm = chrome.find_element_by_tag_name("time").get_attribute("datetime").split(".")[0].split("T")
    tm = datetime.strptime(tm[0]+" "+tm[1],"%Y-%m-%d %H:%M:%S")
    rlikes = list(filter(lambda x:"likes" in x.text,chrome.find_elements_by_tag_name("button")))
    maxx=0
    for lk in rlikes:
        try:
            val = int(lk.text.split()[0].replace(",",""))
            if val > maxx:
                maxx=val
        except Exception as e:
            print(e)
            maxx=0
    print(maxx,tm,mentions)
    client.update_one({"_id":url},{"$set":{"data":1,"likes":maxx,"mentions":mentions,"date":tm}})


# In[ ]:


for post in posts:
    url = post["_id"]
    chrome.get(url)
    time.sleep(0.45)
    fillPost(url)

chrome.close()
# In[4]:





# In[5]:





# In[6]:





# In[7]:





# In[ ]:




