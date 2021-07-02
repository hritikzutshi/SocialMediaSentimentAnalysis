from __future__ import unicode_literals,print_function
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
import tweepy as tw
import json
import pandas as pd
from pymongo import MongoClient
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
import branca.colormap as cmp
import sys , csv , re
from textblob import TextBlob
import matplotlib.pyplot as plt
import branca
import folium.plugins as plugins
from json import dumps
from subprocess import run,PIPE
import io

res=sys.argv

consumer_key = "UODXYhgdi5iSUkb8B3BIludZ0"
consumer_secret = "JxXDM9xoSjFGXlsWWPRLFGcHeahOKpx7W9uAKWsM0BVHOhyN8f"
access_token = "964513788606189570-oIVsHe3QKcReJDE3Z2lSiFjga9CTcUc"
access_token_secret = "mQzFGI4dIfftUGbzND5ZB67ddCkZfYMFMtG0OsoamDyVi"

#authorization and authentication
auth = tw.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token,access_token_secret) 
api = tw.API(auth) 
 #india : 23424848
india_trends = api.trends_place(23424848)

hashtags = []
trends = india_trends[0]['trends']
for trend in trends:
    name = trend['name']
    hashtags.append(name)

with io.open('trending.csv', 'a', encoding="utf-8") as csvfile:
    fieldnames = ['user','date','location','text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for word in res:
        tweets = tw.Cursor(api.search,q=word, lang='en',
        tweet_mode='extended').items(100)
        for tweet in tweets:
            #print(tweet)
            userid = tweet.user.screen_name
            date = tweet.user.created_at
            location = tweet.user.location
            text = tweet.full_text
            writer.writerow({'user':userid, 'date':date,'location':location,'text':text})
print("hey!!")
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

data = pd.read_csv("E:/BE Project/djangotest/trending.csv",engine="python")
data.to_csv("E:/BE Project/djangotest/trending.csv", header=['User','Date','Location','Text'], index=False)
data = pd.read_csv("E:/BE Project/djangotest/trending.csv",engine="python")

counters = []
hashtags = ['Mucormycosis','BlackFungus','corona']

#frequency counting of hashtags

for sub in hashtags:
    num =0
    for i in range(len(data)-1):
        tweet = data.Text[i]
        if sub in tweet:
            num+=1
    counters.append(num)

  
