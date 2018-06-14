#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_token = ''
access_token_secret = ''

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	#try:
   	#redirect_url = auth.get_authorization_url()
	#except tweepy.TweepError:
    #	print('Error! Failed to get request token.')

	# auth.set_access_token(credentials['twitter']['token'], credentials['twitter']['token_secret']
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name, count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)
	print(alltweets[0].id)

	#save the id of the oldest tweet less one
	if len(alltweets) > 0:
		oldest = alltweets[len(alltweets) - 1].id
	else:
		print("YOOOOOO")

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsequent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[len(alltweets) - 1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))

	#cleaned_text = [re.sub(r'http[s]?:\/\/.*[\W]*', '', i.text, flags=re.MULTILINE) for i in alltweets] # remove urls
	#cleaned_text = [re.sub(r'@[\w]*', '', i, flags=re.MULTILINE) for i in cleaned_text] # remove the @twitter mentions 
	#cleaned_text = [re.sub(r'RT.*','', i, flags=re.MULTILINE) for i in cleaned_text] # delete the retweets
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, alltweets[idx]] for idx,tweet in enumerate(alltweets)]

	#write the csv	
	with open('test/%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	pass

if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("WhiskDating")