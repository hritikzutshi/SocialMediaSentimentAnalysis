# -*- coding: utf-8 -*-
from __future__ import unicode_literals,print_function

from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse

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

# Create your views here.

def trending(request):
    return render(request,'examples/trending.html')

def history(request):
    return render(request,'examples/history.html') 

def home(request):
    return render(request,'examples/home.html')    
 
def map(request):
    return render(request,'examples/map.html')    

def aboutus(request):
    return render(request,'examples/aboutus.html') 
    
     

def covid(request):
    MONGO_HOST= 'mongodb://localhost/TwitterDB'
    search_words = ['#corona' , '#covid-19' , '#covid19' , '#coronavirus' , '#lockdown'] 
    consumer_key = "WAceP6IUvkzy7JXB90Q90W8qI"
    consumer_secret = "tbKwLlCybxuc3f14OoCblYOCf10NEy1Tl5W8Gl9HUkupasAltt"
    access_token = "1098646153778782208-5DHrlpMc2mm3XGaKOLdJTVBxsO0JKP"
    access_secret_token = "bHHihlwuT20vw6Fl2gBwuhf0pY6KEhmXEmOXXvbnGZ7rG"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth)
    geolocator = Nominatim(user_agent="myapp")
    world_map= folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(world_map)
    colormap = branca.colormap.linear.RdYlGn_10.scale(-1, 1)
    #colormap = cmp.LinearColormap(colors=branca.colormap.linear.RdYlGn_10.scale(-1, 1), index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
    colormap = colormap.to_step(index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
    colormap.caption = 'Sentiment of tweets'
    colormap.add_to(world_map)

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
                folium.CircleMarker(location = [lat, long], radius=5,color=colormap(polarity),fill_color=colormap(polarity), fill 				=True).add_to(world_map)
            
            except Exception as e:
                print(e)
    try:
        listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
        streamer = tweepy.Stream(auth=auth, listener=listener)
        print("Tracking: " + str(search_words))
        streamer.filter(track=search_words)
        print("output file generated")        
    except Exception as e:
        print(e)
    sttr = world_map.get_root().render()
    context = {'map': sttr}
    return render(request, 'examples/covid.html', context)

def pb1(request):
    return render(request,'examples/progressbar1.html')

def covidstat(request):
    return render(request,'examples/covidstat.html')    

        
