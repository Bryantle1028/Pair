from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import sys
import time
from bs4 import BeautifulSoup as bs
import pandas as pd

username = "USERNAME"
password = "PSWD"
users = ["oliviarance_", "hencanman"]

def get_tweet_text(tweet):
    tweet_text_box = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
    images_in_tweet_tag = tweet_text_box.find_all("a", {"class": "twitter-timeline-link u-hidden"})
    tweet_text = tweet_text_box.text
    for image_in_tweet_tag in images_in_tweet_tag:
        tweet_text = tweet_text.replace(image_in_tweet_tag.text, '')

    return tweet_text

def get_this_page_tweets(soup):
    tweets_list = list()
    tweets = soup.find_all("li", {"data-item-type": "tweet"})
    for tweet in tweets:
        tweet_data = None
        try:
            tweet_data = get_tweet_text(tweet)
        except Exception as e:
            continue
            #ignore if there is any loading or tweet error

        if tweet_data:
            tweets_list.append(tweet_data)
            sys.stdout.flush()

    return tweets_list

options = Options()
options.add_argument("--headless")
profile = webdriver.FirefoxProfile()
profile.set_preference("permissions.default.image", 2)
tweetDriver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)
# tweetDriver = webdriver.Firefox(firefox_profile=profile)
followingDriver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)
# followingDriver = webdriver.Firefox(firefox_profile=profile)
followingDriver.login_url = "https://twitter.com/login"
followingDriver.get(followingDriver.login_url)

username_field = followingDriver.find_element_by_class_name("js-username-field")
password_field = followingDriver.find_element_by_class_name("js-password-field")
username_field.send_keys(username)
followingDriver.implicitly_wait(1)
password_field.send_keys(password)
followingDriver.implicitly_wait(1)
followingDriver.find_element_by_class_name("EdgeButtom--medium").click()

for currentUser in users:
    print('now doing user ' + currentUser)
    followingDriver.following_url = "https://twitter.com/" + currentUser + "/following"
    followingDriver.get(followingDriver.following_url)
    tweetDriver.tweet_url = "https://twitter.com/" + currentUser
    tweetDriver.get(tweetDriver.tweet_url)
    time.sleep(5) # first load

    # Collect Following
    loopCounter = 0
    lastHeight = followingDriver.execute_script("return document.body.scrollHeight")
    while True:
        # if loopCounter > 499:
        #     break; # if the account follows a ton of people, its probably a bot, cut it off
        if loopCounter > 0 and loopCounter % 50 == 0:
            print(loopCounter)
        followingDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        newHeight = followingDriver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        loopCounter = loopCounter + 1
    print('ended at: ' + str(loopCounter))

    # Store Follows
    html_source = followingDriver.page_source
    sourcedata = html_source.encode('utf-8')
    soup=bs(sourcedata, features="html.parser")

    if soup.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Invalid username.")
        sys.exit(1)

    tempusers = [x.div['data-screen-name'] for x in soup.body.findAll('div', attrs={'data-item-type':'user'})]
    tempbios = [x.p.text for x in soup.body.findAll('div', attrs={'data-item-type':'user'})]
    fullnames = [x.text.strip() for x in soup.body.findAll('a', 'fullname')][1:] # avoid your own name
    d = {'usernames': tempusers, 'bios': tempbios, 'fullnames': fullnames}
    df = pd.DataFrame(data=d)
    df.to_csv('data/' + currentUser + 'following.csv')

    # Collect Tweets
    loopCounter = 0
    lastHeight = tweetDriver.execute_script("return document.body.scrollHeight")
    while loopCounter < 30:
        if loopCounter > 0 and loopCounter % 50 == 0:
            print(loopCounter)
        tweetDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        newHeight = tweetDriver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        loopCounter = loopCounter + 1
    print('ended at: ' + str(loopCounter))

    #Store tweets
    html_source = tweetDriver.page_source
    sourcedata = html_source.encode('utf-8')
    soup=bs(sourcedata, features="html.parser")

    if soup.find("div", {"class": "errorpage-topbar"}):
        print("\n\n Error: Invalid username.")
        sys.exit(1)

    temptweets = get_this_page_tweets(soup)
    d = {'tweets': temptweets}
    df = pd.DataFrame(data=d)
    df.to_csv('data/' + currentUser + 'tweets.csv')

tweetDriver.quit()
followingDriver.quit()