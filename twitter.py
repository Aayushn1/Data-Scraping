import tweepy
import csv
consumer_key = 'GolH1wZJNnyXCvhAPM0HzMySW'
consumer_secret = 'unH3JVE9tBZDy805b2w4QYFwsTu5fhTAB1eSMvffF9Qv8usuRq'
access_token = '1133649472750141440-fpMTLcyZOZWvytRGoTCmjB4DAjue5k'
access_token_secret = '2VC3HoQR8P3o057qDgRTZZPDkI0IPjyRnpFhp56edvJPV'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)


count = 200

query = "Digisol"
language = "en"


fetched_tweets = api.search(q = query,lang = language,count = 100)

list1 = []
with open("twitter.csv","w",encoding="UTF-8") as file:
    for tweet in fetched_tweets:
        file.write(tweet.text)
        file.write("\n")

print(list1)






