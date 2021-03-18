# Imports
import pandas as pd
import datetime as dt
import snscrape.modules.twitter as sntwit
import os
os.system('clear')

# Tweet Limit
limit = 10000

# Create a list of tweets to append
tweet_list = []

# Use TwitterSearchScraper to scrape tweets and append to list
for i, tweet in enumerate(
    sntwit.TwitterSearchScraper('covid pfizer vaccine since:2020-12-01 until:2020-12-31').get_items()):
    if i > limit:
        break
    tweet_list.append([tweet.date, tweet.id, tweet.content])


# Create DataFrame
December_Covid = pd.DataFrame(tweet_list, columns=['DateTime', 'Tweet_ID', 'Tweet_Text'])
#print(December_Covid.head(10))

# Save to Excel File
December_Covid.to_csv('December_Covid_Tweets.csv')