from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re
from bs4 import BeautifulSoup as bs
from dateutil import parser
import pandas as pd
import itertools
import matplotlib.pyplot as plt


tweetDriver = webdriver.Firefox()
tweetDriver.tweet_url = "https://twitter.com/oliviarance_"
tweetDriver.get(tweetDriver.tweet_url)
followingDriver = webdriver.Firefox()
followingDriver.following_url = "https://twitter.com/oliviarance_/following"
followingDriver.get(followingDriver.following_url)

for i in range(6):
    tweetDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print("tweet" + str(i))

time.sleep(10)

for i in range(6):
    followingDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print("follow" + str(i))

# SAVING TWEET DATA
html_source = tweetDriver.page_source
sourcedata = html_source.encode('utf-8')
soup = bs(sourcedata, features="html.parser")
tweets = [soup.body.findAll('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')]
d = {'tweets': tweets}
df = pd.DataFrame(data=d)
df.to_csv('data/tweets.csv')
# CLOSE DATA

tweetDriver.quit()

#SAVING FOLLOWING DATA
html_source = followingDriver.page_source
sourcedata = html_source.encode('utf-8')
soup = bs(sourcedata, features="html.parser")
following = [x.div['data-screen-name'] for x in soup.body.findAll('div', attrs={'data-item-type':'user'})]
bios = [x.p.text for x in soup.body.findAll('div', attrs={'data-item-type':'user'})]
fullnames = [x.text.strip() for x in soup.body.findAll('a', 'fullname')][1:] # avoid your own name
d = {'usernames': following, 'bios': bios, 'fullnames': fullnames}
df = pd.DataFrame(data=d)
df.to_csv('data/following.csv')
# CLOSE DATA

followingDriver.quit()