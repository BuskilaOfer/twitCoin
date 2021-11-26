from datetime import datetime

import tweepy  # using version 4.1.0
import pytz


#
# date_string = "2012-12-12 10:10:10"
# print (datetime.from(date_string))

class TwitterBitcoinScanner:
    def __init__(self):
        # Twitter OAuth Authentication
        consumer_key = "dqyaBG6BbC1gETauyEDyoyaib"
        consumer_secret = "pKvBnWNT7Wxr7Z3WwQzhtJ1BlF1cKNw7LEN0597jYsSEE1cCTu"

        access_token = "1269644061079674888-NzGrf0MAEVl6fGDSTtpUTYJMNBezvb"
        access_token_secret = "ubqTldQLx7atDcXUwUlWJ8lLqx1wWkrkCKud97n6PswpN"

        # Configure tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.twitter_api = tweepy.API(auth)

    def get_100_latest_bitcoin_tweets(self):
        query_string = "$BTC OR bitcoin" + " -filter:retweets"
        tweets = self.twitter_api.search_tweets(q=query_string, result_type="recent", count=100, tweet_mode='extended')
        res = []
        for tweet in tweets:
            dt = datetime.strptime(tweet._json['created_at'], "%a %b %d %H:%M:%S +%f %Y")
            # epoch_utc_dt = dt.astimezone(pytz.utc).timestamp()
            date = dt.astimezone(pytz.utc)
            res.append((tweet._json['id'],
                        date,
                        # tweet_sentiment_score = favorite_count + 2*retweet_count
                        int(tweet._json['favorite_count'] + 2 * int(tweet._json['retweet_count']))
                        ))
        return res

# tw = TwitterBitcoinScanner()
# print(tw.get_100_latest_bitcoin_tweets())
