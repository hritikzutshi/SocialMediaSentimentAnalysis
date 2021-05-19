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


MONGO_HOST= 'mongodb://localhost/TwitterDB'
search_words = ['#corona' , '#covid-19' , '#covid19' , '#coronavirus' , '#lockdown'] 
consumer_key = "WAceP6IUvkzy7JXB90Q90W8qI"
consumer_secret = "tbKwLlCybxuc3f14OoCblYOCf10NEy1Tl5W8Gl9HUkupasAltt"
access_token = "1098646153778782208-5DHrlpMc2mm3XGaKOLdJTVBxsO0JKP"
access_secret_token = "bHHihlwuT20vw6Fl2gBwuhf0pY6KEhmXEmOXXvbnGZ7rG"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret_token)
api = tweepy.API(auth)

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
            print(datajson['text'])

            db['tweets'].insert(datajson)

        except Exception as e:
            print(e)

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(search_words))
streamer.filter(track=search_words)


