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
from matplotlib import pyplot as plt

def data_extraction():
    url = "https://www.amazon.in/s?k=digisol&s=review-rank&qid=1560834076&ref=sr_st_review-rank"

    response = requests.get(url)

    html_1 = BeautifulSoup(response.text ,'html.parser')

    '''print(html_1)'''

    print(html_1)

    products = html_1.find_all(attrs={"class" : "a-link-normal a-text-normal","target":"_blank"})
    print(len(products))

    proxies_list = ["128.199.109.241:8080", "113.53.230.195:3128", "125.141.200.53:80", "125.141.200.14:80",
                    "128.199.200.112:138", "149.56.123.99:3128", "128.199.200.112:80", "125.141.200.39:80",
                    "134.213.29.202:4444"]

    proxies = {'https': random.choice(proxies_list)}


    with open("amazon.csv","w",encoding = "UTF-8") as file:
        for product in products:
            splitted_url = product["href"].split('/')
            #print(splitted_url)
            #print(splitted_url)
            # product_review_url = "www.amazon.in"+splitted_url[1]+"product-reviews"+splitted_url[3]+"ref=cm_cr_arp_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" %(i,i)
            j=1;
            file.write(splitted_url[1] + ":")
            file.write("\n")

            for i in range(1,100):
                # print(i)
                #url = "https://www.amazon.in/Digisol-DG-HR3400-300Mbps-Wireless-Broadband/product-reviews/B00IL8DR6W/ref=cm_cr_getr_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" % (i,i)
                product_review_url = "https://www.amazon.in/" + splitted_url[1] + "/product-reviews/" + splitted_url[3] + "/ref=cm_cr_getr_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d" % (i, i)
                response = requests.get(url = product_review_url)
                html = BeautifulSoup(response.text, 'html.parser')
                reviews = html.find_all(attrs={"data-hook": "review-body"})
                reviews_dates = html.find_all(attrs={"data-hook":"review-date"})
                review_profile_name = html.find_all(attrs={"class":"a-profile-name"})
                pro = splitted_url[1];
                if(len(reviews)==0):
                    break
                for i in range(0,len(reviews)-1):
                    review = str(review_profile_name[i].text) + "," + str(reviews_dates[i].text).replace(",","") + "," + "Amazon"+","+ str(reviews[i].text).replace(","," ").replace("\n","") + "," + str(pro)+ ","+ "No" + "," + "No\n"
                    file.write(review)
                print(splitted_url[1])
            file.write("\n--------------------------------------------------\n")

                #print(review.text+"\n")

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
    with open("amazon.csv", 'r',encoding = "UTF-8") as csvfile:
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
