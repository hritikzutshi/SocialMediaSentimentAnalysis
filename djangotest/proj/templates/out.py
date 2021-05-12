#!/usr/bin/env python
# coding: utf-8

# In[15]:


from __future__ import print_function
from http.client import IncompleteRead
import tweepy
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


# In[16]:


MONGO_HOST= 'mongodb://localhost/TwitterDB'


# In[17]:


search_words = ['#corona' , '#covid-19' , '#covid19' , '#coronavirus' , '#lockdown'] 


# In[18]:


consumer_key = "UODXYhgdi5iSUkb8B3BIludZ0"
consumer_secret = "JxXDM9xoSjFGXlsWWPRLFGcHeahOKpx7W9uAKWsM0BVHOhyN8f"
access_token = "964513788606189570-oIVsHe3QKcReJDE3Z2lSiFjga9CTcUc"
access_secret_token = "mQzFGI4dIfftUGbzND5ZB67ddCkZfYMFMtG0OsoamDyVi"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret_token)
api = tweepy.API(auth)
date_since = "2020-01-1"
until="2020-01-30"
geolocator = Nominatim(user_agent="myapp")
world_map= folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
colormap = branca.colormap.linear.RdYlGn_10.scale(-1, 1)
#colormap = cmp.LinearColormap(colors=branca.colormap.linear.RdYlGn_10.scale(-1, 1), index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
colormap = colormap.to_step(index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
colormap.caption = 'Sentiment of tweets'
colormap.add_to(world_map)


# In[19]:



def PlotOnMap(location,text):
    
    try:
        location = geolocator.geocode(location)
        lat = location.latitude
        long = location.longitude
    except:
        lat = 19.7515
        long = 75.7139
    radius=4
    analysis = TextBlob(text)
    polarity += analysis.sentiment.polarity
    folium.Circle(location = [lat, long], radius=radius,color=colormap(polarity), fill =True).add_to(world_map)
    """
    if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
        neutral += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='yellow', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
        wpositive += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='light green', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
        positive += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='green', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
        spositive += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='dark green', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
        wnegative += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='pink', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
        negative += 1
        folium.CircleMarker(location = [lat, long], radius=radius,color='maginta', fill =True).add_to(world_map)
    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
        snegative += 1 
        folium.CircleMarker(location = [lat, long], radius=radius,color='voilet', fill =True).add_to(world_map)
    """
    


# In[20]:


class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 

    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.TwitterDB
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            #print(datajson)
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['user']['created_at']
            username = datajson['user']['name']
            location = datajson['user']['location']
            text = datajson['text']
            positive = 0
            wpositive = 0
            spositive = 0
            negative = 0
            wnegative = 0
            snegative = 0
            neutral = 0
            db.LiveStream.insert({'user':username ,'Date':created_at,'Location':location,'Tweet':text })
            polarity = 0
            try:
                location = geolocator.geocode(location)
                lat = location.latitude
                long = location.longitude
            except:
                lat = 19.7515
                long = 75.7139
            radius=7
            analysis = TextBlob(text)
            polarity = analysis.sentiment.polarity
            folium.CircleMarker(location = [lat, long], radius=5,color=colormap(polarity),fill_color=colormap(polarity), fill =True, ).add_to(world_map)
           
        except Exception as e:
            print(e)


# In[21]:


listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(search_words))
streamer.filter(track=search_words)


# In[22]:


world_map.save('index.html')


# In[ ]:




