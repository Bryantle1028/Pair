#!/usr/bin/env python
# encoding: utf-8

import urllib.parse
import oauth2 as oauth
import tweepy #https://github.com/tweepy/tweepy
import csv
import re

#Twitter API credentials
consumer_key = "yNu3JeFzWJXqUvmoT03H30PXr"
consumer_secret = "f1NdJYV4A6cb64QYaFmshyDhQCl4BRzyJkNVqOF0h4otWrSae0"

#Twitter URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = b'https://api.twitter.com/oauth/authorize'

def authFlow():
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)

	# Step 1: Get a request token. This is a temporary token that is used for 
	# having the user authorize an access token and to sign the request to obtain 
	# said access token.
	    
	resp, content = client.request(request_token_url, "GET")
	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])

	request_token = dict(urllib.parse.parse_qsl(content))

	print("Request Token: ")
	print(request_token[b'oauth_token'])

	# Step 2: Redirect to the provider. Since this is a CLI script we do not 
	# redirect. In a web application you would redirect the user to the URL
	# below.

	print("Go to the following link in your browser:")
	print(b"%s?oauth_token=%s" % (authorize_url, request_token[b'oauth_token']))

	# After the user has granted access to you, the consumer, the provider will
	# redirect you to whatever URL you have told them to redirect to. You can 
	# usually define this in the oauth_callback argument as well.
	oauth_verifier = input('What is the PIN? ')

	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the 
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this 
	# access token somewhere safe, like a database, for future use.
	token = oauth.Token(request_token[b'oauth_token'],
	    request_token[b'oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)

	resp, content = client.request(access_token_url, "POST")
	access_token = dict(urllib.parse.parse_qsl(content))

	return access_token	

def get_all_tweets(userId, access_token):
	#authorize twitter, initialize tweepy
	page = 0
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token[b'oauth_token'], access_token[b'oauth_token_secret'])
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	allfavs = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = userId,count=200)
	new_favs = api.favorites(userId, page)

	#save most recent tweets
	alltweets.extend(new_tweets)
	allfavs.extend(new_favs)

	#save the id of the oldest tweet less one
	if len(alltweets) > 0:
		oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0 || len(new_favs) > 0:
		print ("getting tweets before %s" % (oldest))
		page += 1
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = userId,count=200,max_id=oldest)
		new_favs = api.favorites(userId, page)

		#save most recent tweets
		alltweets.extend(new_tweets)
		allfavs.extend(new_favs)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
		print ("...%s favs downloaded so far" % (len(allfavs)))
	cleaned_text = [re.sub(r'http[s]?:\/\/.*[\W]*', '', i.text, flags=re.MULTILINE) for i in alltweets] # remove urls
	cleaned_text = [re.sub(r'@[\w]*', '', i, flags=re.MULTILINE) for i in cleaned_text] # remove the @twitter mentions
	cleaned_favs = [re.sub(r'http[s]?:\/\/.*[\W]*', '', i.text, flags=re.MULTILINE) for i in allfavs] # remove urls
	cleaned_favs = [re.sub(r'@[\w]*', '', i, flags=re.MULTILINE) for i in cleaned_favs] # remove the @twitter mentions
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, cleaned_text[idx].encode("utf-8")] for idx,tweet in enumerate(alltweets)]
	outfavs = [[tweet.id_str, tweet.created_at, cleaned_favs[idx].encode("utf-8")] for idx,tweet in enumerate(allfavs)]

	#write the csv	
	with open('data/%s_tweets.csv' % userId, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
		writer.writerow(["|||"])
		writer.writerows(outfavs)

	pass

if __name__ == '__main__':
	#pass in the username of the account you want to download
	access_token = authFlow()
	get_all_tweets("SCREEN_NAME", access_token)
