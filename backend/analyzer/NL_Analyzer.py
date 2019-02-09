import pandas as pd
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions
import collections
import string
import os
import psutil

process = psutil.Process(os.getpid())

tweet_df = pd.read_csv('WhiskDating_tweets.csv')

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='4bb0c588-3403-471e-b1fe-63ef24845e5a',
  password='8r2OPyacj0Am',
  version='2018-03-16')

categoryTweets = collections.defaultdict(list)
categoryRelevance = {}

for tweet in tweet_df['text']:
    try:
        response = natural_language_understanding.analyze(
        text= tweet,
        features=Features(
        categories=CategoriesOptions()))
        #use keywords and create another dictionary that maps categories to a set of keywords
    except:
        continue
    for category in response['categories']:

        label = category['label'].replace('/', '', 1)
        index = label.find('/')
        if index != -1: label = label[:index]

        categoryTweets[label].append(tweet)

for category in categoryTweets.keys():
    categoryRelevance[category] = (len(categoryTweets[category]) / len(tweet_df)) * 100

df = pd.DataFrame([categoryTweets])
df1 = pd.DataFrame([categoryRelevance])
df.join(df1, lsuffix='tweets', rsuffix='relevance')

df.to_csv('output.csv')

print (categoryTweets, categoryRelevance)
print(process.memory_info().rss)