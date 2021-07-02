# -*- coding: utf-8 -*-
from __future__ import unicode_literals,print_function
from asyncio import sleep
import base64
import codecs
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from requests import api
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
from IPython.display import HTML
import plotly.graph_objects as px
from .lime_explainer import explainer, tokenizer, METHODS
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from tkinter import *  
from tkinter import messagebox  
  
# Create your views here.



def trending(request):
    consumer_key = "QCNcrf5aduIVeX347KX81RQ5z"
    consumer_secret = "viSddLLOfgQA3beUwGjz1JIbYjnRtolag4g8DifnjsyTOSqnew"
    access_token = "964513788606189570-ZZvpjC4SWR5HH4q2Q0vhGEPXvy6RHS5"
    access_token_secret = "Fh6tjUmZjzOybRCxYO6LHXTkpjM17nwcsLkko3JpRDgGY"
    
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

    res=[]
    subs = ['COVID-19','Corona','WHO','secondwave','Indiafightscorona','healthcare','White Fungus','WhiteFungus','BlackFungus','white fungus','Healthcare','Palestine','Storms','Storm','Tauktae','GazzaUnderAttack','savepalestinians','Gazzaunderattack','GenocideinGaza','IsaraelTerrorist','storm','health','Health','corona','COVID-19','covid19','Covid','earthquake','crisis','flood','Flood','Ocean','ocean','Arabiansea','Arabic','TauktaeCyclone','mumbairain','cyclone','karnatakarain','KarnatakaRain','KarnatakaRain','Tauktae','KeralaFlood','Mumbai','NDRF','rainfall','NDMA','lightning','Thunderstorm','thunderstorm','cyclone','Cyclone','CYCLONE','indiafigtscorona','quartine','lockdown','gujrat','Gujrat','terror','Terror']
    for i in hashtags:
        for sub in subs:
            if sub in i:
                res.append(i)
    print(res)
    res=dumps(res)
    return render(request,'examples/trending.html',{'res':res})


def history(request):
    return render(request,'examples/history.html') 

def demo(request):
    return render(request,'examples/demo.html') 

def home(request):
    return render(request,'examples/home.html')    

def map(request):
    exp = ""
    if request.method == 'POST':
        text = request.POST.get('entry')
        method = request.POST.get('classifier')
        n_samples = request.POST.get('n_samples')

        if any(not v for v in [text]):
            raise ValueError("Please do not leave text fields blank.")

        if method != "base":
            exp = explainer(method,
                            path_to_file=METHODS[method]['file'],
                            text=text,
                            lowercase=METHODS[method]['lowercase'],
                            num_samples=1000)
            exp.show_in_notebook(text="true")
            exp.save_to_file('/home/hertz/MyGit/djangotest/proj/static/html/ex.html')   
    return render(request,'examples/map.html',{'exp':exp})    

def piechart(request):
    return render(request,'examples/piechart.html')

def world(request):
    return render(request,'examples/world.html')

def worldcomp(request):
    return render(request,'examples/comp.html') 

def states(request):
    return render(request,'examples/states.html')

def aboutus(request):
    return render(request,'examples/aboutus.html') 

def compn(request):
    return render(request,'examples/comp.html') 



def external(request):
    inpt=request.POST.getlist('optCheck')
    if(len(inpt)==0):            
        top=Tk()    
        top.geometry("100x100")      
        messagebox.showerror("alert","Please select or enter atleast one hashtag!!!")  
        top.mainloop()  
        return render(request,'examples/trending.html')
    else:
        print("Values:",inpt) 
        consumer_key = "QCNcrf5aduIVeX347KX81RQ5z"
        consumer_secret = "viSddLLOfgQA3beUwGjz1JIbYjnRtolag4g8DifnjsyTOSqnew"
        access_token = "964513788606189570-ZZvpjC4SWR5HH4q2Q0vhGEPXvy6RHS5"
        access_token_secret = "Fh6tjUmZjzOybRCxYO6LHXTkpjM17nwcsLkko3JpRDgGY"
        
        #authorization and authentication
        auth = tw.OAuthHandler(consumer_key, consumer_secret) 
        auth.set_access_token(access_token,access_token_secret) 
        api = tw.API(auth) 
    

        with io.open('trending.csv', 'w', encoding="utf-8") as csvfile:
            fieldnames = ['user','date','location','text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for word in inpt:
                tweets = tw.Cursor(api.search,q=word, lang='en',
                tweet_mode='extended').items(300)
                for tweet in tweets:
                  #  print(tweet)
                    userid = tweet.user.screen_name
                    date = tweet.user.created_at
                    location = tweet.user.location
                    text = tweet.full_text
                    writer.writerow({'user':userid, 'date':date,'location':location,'text':text})

    
    
        maxInt = sys.maxsize

        while True:
                # decrease the maxInt value by factor 10 
                # as long as the OverflowError occurs.

                try:
                    csv.field_size_limit(maxInt)
                    break
                except OverflowError:
                    maxInt = int(maxInt/10)

        data = pd.read_csv("/home/hertz/MyGit/djangotest/trending.csv",engine="c")
       # data = csv.reader(codecs.open("//home/hertz/MyGit/djangotest/trending.csv", 'rU', 'utf-16'))

        data.to_csv("/home/hertz/MyGit/djangotest/trending.csv", header=['User','Date','Location','Text'], index=False)
        data = pd.read_csv("/home/hertz/MyGit/djangotest/trending.csv",engine="python")

        cnt = []
        hashtags = inpt

            #frequency counting of hashtags

        for sub in hashtags:
            num =0
            for i in range(len(data)-1):
                tweet = data.Text[i]
                if sub in tweet:
                    num+=1
            cnt.append(num)

            
        print(hashtags)
        print(cnt)

        
        my_path = os.path.abspath("/home/hertz/MyGit/djangotest/proj/static/img/") # Figures out the absolute path for you in case your working directory moves around.
        my_file = 'bar2.png'
        plt.figure(figsize=(17,8))
        New_Colors = ['green','blue','purple','brown','teal']
        plt.bar(hashtags,cnt,color=New_Colors)
        plt.title('Tweet count for each hashtag')
        plt.xlabel('Hashtags')
        plt.ylabel('Number of Tweets')
        plt.savefig(os.path.join(my_path, my_file))

        plt.clf()
        my_path = os.path.abspath("/home/hertz/MyGit/djangotest/proj/static/img/") # Figures out the absolute path for you in case your working directory moves around.
        my_file = 'trend1.png'
        hashtags = inpt
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        num=0
        positives = []
        negatives = []
        neutrals = []
        for hashtag in hashtags:
            for tweet in data.iterrows():
                text = tweet[1]['Text']
                if hashtag in text:
                    analysis = TextBlob(text)
                    polarity = analysis.sentiment.polarity
                    if (analysis.sentiment.polarity == 0):  
                        neutral += 1
                    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                        wpositive += 1
                    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                        positive += 1
                    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                        spositive += 1
                    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                        wnegative += 1
                    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                        negative += 1
                    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                        snegative += 1 
            positives.append(wpositive+positive+spositive)
            negatives.append(wnegative+negative+snegative)
            neutrals.append(neutral)


        print(hashtags)
        print(neutrals)
        print(positives)
        print(negatives)
        labels = ['Positive [' + str(positive) + ']', 'Weakly Positive [' + str(wpositive) + ']','Strongly Positive [' + str(spositive) + ']', 'Neutral [' + str(neutral) + ']',
                        'Negative [' + str(negative) + ']', 'Weakly Negative [' + str(wnegative) + ']', 'Strongly Negative [' + str(snegative) + ']']
        sizes = [positive, wpositive, spositive,neutral, negative, wnegative, snegative]
        colors = ['lightgreen','yellowgreen','darkgreen', 'gold','red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('Pie chart of Sentiment Analaysis for Trending Hashtags')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(my_path, my_file))
    
        plt.clf()
        my_path = os.path.abspath("//home/hertz/MyGit/djangotest/proj/static/html/") # Figures out the absolute path for you in case your working directory moves around.
        my_file = 'trend2.html'
        X = hashtags
        cmap1 = ['red','green','orange']
        plot = px.Figure(data = [px.Bar(name='Negative' , x = X,y = negatives,width=0.2 ), 
                                px.Bar(name='Positive' , x = X,y = positives,width=0.2),
                                px.Bar(name='Neutral' , x = X,y = neutrals ,width=0.2)
                                ])
        plot.update_layout(barmode='stack',colorway=cmap1)
        plot.write_html(os.path.join(my_path,my_file))

        plt.clf()
        my_path = os.path.abspath("/home/hertz/MyGit/djangotest/proj/static/img/") # Figures out the absolute path for you in case your working directory moves around.
        my_file = 'trend3.png'
        plt.figure(figsize=(18,8))
        plt.plot(hashtags,neutrals,color='gold',label='Neutral Tweets')
        plt.plot(hashtags,positives,color='green',label='Positive Tweets')
        plt.plot(hashtags,negatives,color='red',label='Negative Tweets')
        plt.title(' Positive vs Negative vs Neutrals')
        plt.legend(framealpha=0.3, frameon=True,loc='upper center', ncol=3)
        plt.savefig(os.path.join(my_path, my_file))
        return render(request,'examples/trending_output.html',{'out':inpt,'counter':cnt})     

def covid(request):
    MONGO_HOST= 'mongodb://localhost/TwitterDB'
    search_words = ['#corona' , '#covid-19' , '#covid19' , '#coronavirus' , '#lockdown'] 
    consumer_key = "WAceP6IUvkzy7JXB90Q90W8qI"
    consumer_secret = "tbKwLlCybxuc3f14OoCblYOCf10NEy1Tl5W8Gl9HUkupasAltt"
    access_token = "1098646153778782208-5DHrlpMc2mm3XGaKOLdJTVBxsO0JKP"
    access_secret_token = "bHHihlwuT20vw6Fl2gBwuhf0pY6KEhmXEmOXXvbnGZ7rG"
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret_token)
    api = tw.API(auth)
    geolocator = Nominatim(user_agent="myapp")
    world_map= folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(world_map)
    colormap = branca.colormap.linear.RdYlGn_10.scale(-1, 1)
    #colormap = cmp.LinearColormap(colors=branca.colormap.linear.RdYlGn_10.scale(-1, 1), index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
    colormap = colormap.to_step(index=[-1, -0.6, -0.3, 0.1,0, 0.3,0.6,1])
    colormap.caption = 'Sentiment of tweets'
    colormap.add_to(world_map)

    class StreamListener(tw.StreamListener):    
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
        listener = StreamListener(api=tw.API(wait_on_rate_limit=True)) 
        streamer = tw.Stream(auth=auth, listener=listener)
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

        
