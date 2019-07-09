import csv
import requests
from bs4 import BeautifulSoup
import json
import time
# For doing cool regular expressions
import re
import schedule
# For sorting dictionaries
import operator


def data_extraction():
    url = "https://www.flipkart.com/computers/pr?sid=6bo&q=digisol&otracker=categorytree&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.brand%255B%255D%3DDigisol"

    response = requests.get(url)
    html = BeautifulSoup(response.text,'html.parser')

    products = html.find_all(attrs={"class":"_2cLu-l"})
    print(len(products))

    with open('flipkart.csv',"w",encoding="UTF-8") as file:
        for product in products:
            time.sleep(10)
            address = "https://www.flipkart.com" + product["href"]
            response1 = requests.get(address)
            html1 = BeautifulSoup(response1.text,'html.parser')
            #print(html1)
            all_reviews = html1.find(attrs={"class":"swINJg _3nrCtb"})

            if(all_reviews == None):
                continue

            print(product["title"]+"\n")
            file.write(product["title"]+" :\n")
            j = 0;
            for i in range(1,100):

                rev_address ="https://www.flipkart.com" + all_reviews.parent["href"] + "&page=%d" %(i)

                review_response = requests.get(rev_address)

                review_html = BeautifulSoup(review_response.text,'html.parser')
                names = review_html.find_all(attrs = {"class" : "_3LYOAd _3sxSiS"})
                pro = product["title"]
                dates = review_html.find_all(attrs = {"class":"_3LYOAd"})
                #print(dates)
                review_text = review_html.find_all(attrs={"class":"qwjRop"})

                if(len(review_text)==0):
                    break

                for i in range(0,len(review_text)-1):
                    rev_text = review_text[i].div.div.text.replace(","," ")
                    review = str(names[i].text) +"," + str(dates[1+2*i].text.replace(","," ")) +"," + "Flipkart" + "," + rev_text + "," + product["title"] + "," + "No" + "," + "No\n"
                    file.write(review)

            file.write("\n--------------------------------------------------\n")
            #print(rev_address)

# A helper function that removes all the non ASCII characters
# from the given string. Retuns a string with only ASCII characters.
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def job():
    print("hello")

# LOAD AND CLEAN DATA

# Load in the input file and process each row at a time.
# We assume that the file has three columns:
# 0. The tweet text.
# 1. The tweet ID.
# 2. The tweet publish date
#
# Create a data structure for each tweet:
#
# id:       The ID of the tweet
# pubdate:  The publication date of the tweet
# orig:     The original, unpreprocessed string of characters
# clean:    The preprocessed string of characters
# pubdate:  Date on which review was added
# product:  Product for which review was done
def analysis():
    tweets = []
    with open("flipkart.csv", 'r',encoding = "UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:

            tweet= dict()
            if(len(row)<6):
                continue
            tweet['orig'] = row[3]
            tweet['id'] = (row[0])
            tweet['pubdate'] = row[1]
            tweet['platform'] = row[2]
            tweet['product'] = row[4]

            # Ignore retweets
            if re.match(r'^RT.*', tweet['orig']):
                continue

            tweet['clean'] = tweet['orig']

            # Remove all non-ascii characters
            tweet['clean'] = strip_non_ascii(tweet['clean'])

            # Normalize case
            tweet['clean'] = tweet['clean'].lower()

            # Remove the hashtag symbol
            tweet['clean'] = tweet['clean'].replace(r'#', '')

            tweets.append(tweet)

    # Create a data structure to hold the lexicon.
    # We will use a Python diction. The key of the dictionary will be the word
    # and the value will be the word's score.
    lexicon = dict()

    # Read in the lexicon.
    with open('subjectivity_clues_hltemnlp05/lexicon_easy.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lexicon[row[0]] = int(row[1])

    # Use lexicon to score tweets
    for tweet in tweets:
        score = 0
        for word in tweet['clean'].split():
            if word in lexicon:
                score = score + lexicon[word]

        tweet['score'] = score
        if (score > 0):
            tweet['sentiment'] = 'positive'
        elif (score < 0):
            tweet['sentiment'] = 'negative'
        else:
            tweet['sentiment'] = 'neutral'


    # Print out summary stats
    total = float(len(tweets))
    num_pos = sum([1 for t in tweets if t['sentiment'] == 'positive'])
    num_neg = sum([1 for t in tweets if t['sentiment'] == 'negative'])
    num_neu = sum([1 for t in tweets if t['sentiment'] == 'neutral'])
    print ("Positive: %5d (%.1f%%)" % (num_pos, 100.0 * (num_pos/total)))
    print ("Negative: %5d (%.1f%%)" % (num_neg, 100.0 * (num_neg/total)))
    print ("Neutral:  %5d (%.1f%%)" % (num_neu, 100.0 * (num_neu/total)))

    #To plot the sentiment score on a histogram
    score = []

    for tweet in tweets:
        score.append(tweet['score'])
    bins = [-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
    plt.hist(score,bins = bins)
    plt.title("Sentiment Score of Reviews")
    plt.xlabel("Sentiment Score")
    plt.ylabel("No. of Reviews")
    plt.show()

    # Print out some of the tweets
    tweets_sorted = sorted(tweets, key=lambda k: k['score'])

    print ("\n\nTOP NEGATIVE REVIEWS")
    negative_tweets = [d for d in tweets_sorted if d['sentiment'] == 'negative']
    for tweet in negative_tweets[0:10]:
        #print ("Reviewer Name=%s, Sentiment Score=%.2f, Review=%s" % (tweet['id'], tweet['score'], tweet['clean']))
        print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))

    print ("\n\nTOP POSITIVE REVIEWS")
    positive_tweets = [d for d in tweets_sorted if d['sentiment'] == 'positive']
    for tweet in positive_tweets[-10:]:
        print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))


    print ("\n\nTOP NEUTRAL REVIEWS")
    neutral_tweets = [d for d in tweets_sorted if d['sentiment'] == 'neutral']
    for tweet in neutral_tweets[0:10]:
        print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))

schedule.every().day.at("00:00").do(data_extraction)
#schedule.every(24).seconds.do(job)
schedule.every().day.at("00:00").do(analysis)        
        
while True:
    schedule.run_pending()
    time.sleep(1)
