import csv

# For doing cool regular expressions
import re

# For sorting dictionaries
import operator

# Intialize an empty list to hold all of our tweets
tweets = []


# A helper function that removes all the non ASCII characters
# from the given string. Retuns a string with only ASCII characters.
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)



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

with open('amazon.csv', 'r',encoding = "UTF-8") as csvfile:
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

from matplotlib import pyplot as plt

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

print ("\n\nTOP NEGATIVE TWEETS")
negative_tweets = [d for d in tweets_sorted if d['sentiment'] == 'negative']
for tweet in negative_tweets[0:10]:
    #print ("Reviewer Name=%s, Sentiment Score=%.2f, Review=%s" % (tweet['id'], tweet['score'], tweet['clean']))
    print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))

print ("\n\nTOP POSITIVE TWEETS")
positive_tweets = [d for d in tweets_sorted if d['sentiment'] == 'positive']
for tweet in positive_tweets[-10:]:
    print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))


print ("\n\nTOP NEUTRAL TWEETS")
neutral_tweets = [d for d in tweets_sorted if d['sentiment'] == 'neutral']
for tweet in neutral_tweets[0:10]:
    print ("Reviewer Name = %s\nProduct: %s\nSentiment Score = %.2f \nReview = %s\nReview Date = %s       Platform = %s\n--------------------------------------------------" % (tweet['id'],tweet['product'],tweet['score'], tweet['clean'],tweet['pubdate'],tweet['platform']))
