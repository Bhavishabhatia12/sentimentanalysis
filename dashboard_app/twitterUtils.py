import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from dashboard_app.utils import ConfigReader
from dashboard_app.models import Tweet
import re



class TwitterHandle():
    def __init__(self):
        self.cf = ConfigReader()
        API_key = self.cf.get('TWITTER', 'api_key')
        API_secret = self.cf.get('TWITTER', 'api_secret')
        access_token = self.cf.get('TWITTER', 'access_token')
        access_token_secret = self.cf.get('TWITTER', 'access_token_secret')
        try:
            self.auth = OAuthHandler(API_key,
                                     API_secret)
            self.auth.set_access_token(access_token,
                                       access_token_secret)
            self.api = tweepy.API(self.auth)
            print('Authenticated')
        except:
            print("Sorry! Error in authentication!")

    def cleaning_process(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
                               , " ", tweet).split())

    def get_sentiment(self, tweet):
        analysis = TextBlob(self.cleaning_process(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=1000):
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except Exception as e:
            fetched_tweets = Tweet.objects.filter(message__contains=query)
            for tweet in fetched_tweets:
                parsed_tweet= {'tweet_id': tweet.tweet_id, 'posting_date': tweet.posting_date,
                               'twitter_handle': tweet.twitter_handle, 'message': tweet.message,
                               'sentiment': self.get_sentiment(tweet.message)}
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            return tweets



