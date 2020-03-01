#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import time
chrome = webdriver.Chrome("/home/kdemac/chromedriver")
from pymongo import MongoClient


# In[2]:


posts=[]
name = input("Enter Act:")
client = MongoClient("localhost")["instagram"][name]


# In[3]:


chrome.get("https://www.instagram.com/accounts/login/?source=auth_switcher")


# In[4]:


def getPosts():
    global posts
    
    
    alla = chrome.find_elements_by_tag_name("a")
    for a in alla:
        try:
            if "/p/" in a.get_attribute("href") and not a.get_attribute("href") in posts:
                posts.append(a.get_attribute("href"))
                client.insert_one({"_id":a.get_attribute("href"),"data":0,"viewed":False})
                print(a.get_attribute("href"))
        except Exception as e:
            print(e)
            
    current = chrome.execute_script("return document.body.scrollHeight")
    chrome.execute_script("window.scrollTo(0, {})".format(current))
    time.sleep(2.34)
    new = chrome.execute_script("return document.body.scrollHeight")
    if current == new:
        print("reached end")
    else:
        getPosts()
    
    
            
    


# In[5]:


input()
getPosts()
chrome.close()


# In[ ]:




