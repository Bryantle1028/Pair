#!/usr/bin/env python
# encoding: utf-8

import urlparse
import oauth2 as oauth
import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = ""
consumer_secret = ""

#Twitter URLs
request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'

def authFlow():
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)

	# Step 1: Get a request token. This is a temporary token that is used for 
	# having the user authorize an access token and to sign the request to obtain 
	# said access token.
	    
	resp, content = client.request(request_token_url, "GET")
	if resp['status'] != '200':
	    raise Exception("Invalid response %s." % resp['status'])

	request_token = dict(urlparse.parse_qsl(content))

	print "Request Token:"
	print "    - oauth_token        = %s" % request_token['oauth_token']
	print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
	print 

	# Step 2: Redirect to the provider. Since this is a CLI script we do not 
	# redirect. In a web application you would redirect the user to the URL
	# below.

	print "Go to the following link in your browser:"
	print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	print 

	# After the user has granted access to you, the consumer, the provider will
	# redirect you to whatever URL you have told them to redirect to. You can 
	# usually define this in the oauth_callback argument as well.
	oauth_verifier = raw_input('What is the PIN? ')

	# Step 3: Once the consumer has redirected the user back to the oauth_callback
	# URL you can request the access token the user has approved. You use the 
	# request token to sign this request. After this is done you throw away the
	# request token and use the access token returned. You should store this 
	# access token somewhere safe, like a database, for future use.
	token = oauth.Token(request_token['oauth_token'],
	    request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)

	resp, content = client.request(access_token_url, "POST")
	access_token = dict(urlparse.parse_qsl(content))

	return access_token	

def get_all_tweets(screen_name, access_token):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	# oldest = alltweets[-1].id - 1

	if len(alltweets) > 0:
		oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		# oldest = alltweets[-1].id - 1

		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	access_token = authFlow()
	get_all_tweets("SCREEN NAME", access_token)