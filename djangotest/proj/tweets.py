import tweepy
import json

from pymongo import MongoClient




class TwitterStream(tweepy.StreamListener):   

    def on_connect(self):
        # Function called to connect to the Twitter Streaming API
        print("You are now connected to the Twitter streaming API.")
 
    def on_error(self, status_code):
        # Function displays the error or status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #Function connects to the defined MongoDB and stores the filtered tweets
        try:
            #Connect to MongoDB host
            client = MongoClient(MONGO_HOST)

            #Use defined database (here: tweets)
            db = client[DATABASE]

            # Decode the JSON data from Twitter
            datajson = json.loads(data)
            
            #Pick the 'text' data from the Tweet
            tweet_message = datajson['text']

            #Show the text from the tweet we have collected
            print(tweet_message)
            
            #Store the Tweet data in the defined MongoDB collection
            db[COLLECTION].insert(datajson)
        except Exception as e:
           print(e)