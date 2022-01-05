import tweepy
from textblob import TextBlob # Biasa digunakan untuk NLP
import re 
import sys
import csv
import pandas as pd
import datetime
from datetime import timedelta # Untuk menghitung perbedaan hari

consumer_key = '' # Isi dengan key sendiri
consumer_secret = '' # Isi dengan key sendiri
access_token = '' # Isi dengan key sendiri
access_secret = '' # Isi dengan key sendiri

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

data = []

tempPos = 0
tempNeg = 0
tempNeu = 0

# # Mengatur waktu
# today = datetime.datetime.now()
# today = today.replace(hour=23, minute=59, second=59, microsecond=999999) # Set from the beginning of the day
# timeInterval = 2 # 2 because we want 2 days before today
# ereyesterday = today - datetime.timedelta(timeInterval) #ereyesterday = https://en.wiktionary.org/wiki/ereyesterday
# duration = ereyesterday + datetime.timedelta(timeInterval) # equivalent to today

# twoDaysAgo = datetime.datetime.today() - timedelta(days = 2)
# print(twoDaysAgo)
# print(type(twoDaysAgo))
# dateTwoDaysAgo = twoDaysAgo.date()

for tweets in tweepy.Cursor(api.search_tweets, q = "#covid19 -filter:retweets", count = 100, lang = "id").items():
	# print(tweets.created_at, tweets.text)
	tweetDate = tweets.created_at
	text = tweets.text
	textWords = text.split()
	newTweetDate = tweetDate.date()
	today = datetime.date.today()

	dateDiff = (today - newTweetDate).days


	# print("============================================")
	# print(type(tweetDate)) --> datetime.datetime
	# print(tweetDate) --> 2021-11-24 08:44:43+00:00
	# print(type(newTweetDate)) --> datetime.date
	# print(newTweetDate) --> 2021-11-24
	# print("============================================")

	# print("============================================")
	# print("Testing delta:")
	# print(dateDiff)
	# print("============================================")

	if dateDiff <= 2:
		print(tweetDate, text)
		cleanedTweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)"," ", text).split())

		analysis = TextBlob(cleanedTweets)

		if(analysis.sentiment.polarity > 0):
			polarity = 'Positive'
			tempPos += 1

		elif(analysis.sentiment.polarity < 0):
			polarity = 'Negative'
			tempNeg += 1

		elif(0 <= analysis.sentiment.polarity <=0.2):
			polarity = 'Neutral'
			tempNeu += 1

		dic = {}
		dic['Sentiment'] = polarity
		dic['Polarity'] = analysis.sentiment.polarity
		dic['Tweet Date'] = tweetDate
		dic['Tweet'] = cleanedTweets
		data.append(dic)
	
	else:
		print("Tweet is older than 2 days")
		continue
	
df = pd.DataFrame(data)
df.to_csv('video.csv')

print(tempPos)
print(tempNeg)
print(tempNeu)