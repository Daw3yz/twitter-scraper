import re
from requests_html import HTMLSession, HTML
from datetime import datetime
from urllib.parse import quote
from lxml.etree import ParserError
import csv

session = HTMLSession()

def get_element_attr(element, attr='href="'):
    element = element.html
    #Get load more link
    urlIndex = element.find(attr) + len(attr)
    url = ""

    for char in element[urlIndex:]:
        if char == '"':
            break
        url+=char
    return url
    

def get_tweets(query, pages=1):
    """Gets tweets for a given user, via the Twitter frontend API."""


    url = f"https://mobile.twitter.com/search/timeline?f=tweets&vertical=default&q={query}&src=tyah&reset_error_state=false&"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": f"https://twitter.com/{query}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }

    tweets = []

    for x in range(pages):
        try:
            html = session.get(url, headers=headers)
            html = HTML(html=html.text, url="bunk", default_encoding="utf-8")

            tweet_table = html.find("table.tweet")
        except:
            break

        for tweet in tweet_table:
            try:
                tweet_id = tweet.find("div.tweet-text")[0]
                tweet_id = get_element_attr(tweet_id, 'data-id="')
            except:
                tweet_id = None

            try:
                tweet_url = "https://twitter.com" + get_element_attr(tweet)
            except:
                tweet_url = None

            try:
                fullname = tweet.find("strong.fullname")[0].text
            except Exception as e:
                fullname = None

            try:
                username = tweet.find("div.username")[0].text
            except:
                username = None
            
            try:
                time = tweet.find("td.timestamp")[0].text
            except:
                time = None
            
            try:
                text = tweet.find("div.tweet-text")[0].text
            except Exception as e:
                print (e)
                text=None

            tweets.append(
                {
                    "tweetId": tweet_id,
                    "tweetUrl": tweet_url,
                    "fullname": fullname,
                    "username": username,
                    #"userId": user_id,
                    #"isRetweet": is_retweet,
                    #"isPinned": is_pinned,
                    "time": time,
                    "text": text,
                    #"replies": replies,
                    #"retweets": retweets,
                    #"likes": likes,

                    #TODO get this, it exists in the mobile version
                    #"entries": {
                    #    "hashtags": hashtags,
                    #    "urls": urls,
                    #    "photos": photos,
                    #    "videos": videos,
                    #},
                }
            )

        url = html.find("div.w-button-more")[0]
        #Get load more link
        url = "https://twitter.com" + get_element_attr(url)
    return tweets

def to_csv(tweets, filename="tweets"):
    filename += ".csv"
    keys = tweets[0].keys()
    with open(filename, 'w', newline='', encoding='utf16')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tweets)


# for searching:
#
# https://twitter.com/i/search/timeline?vertical=default&q=foof&src=typd&composed_count=0&include_available_features=1&include_entities=1&include_new_items_bar=true&interval=30000&latent_count=0
# replace 'foof' with your query string.  Not sure how to decode yet but it seems to work.