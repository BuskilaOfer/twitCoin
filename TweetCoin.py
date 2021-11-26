from FinancialModelingPrep import FinancialModelingPrep as FMP
from InMemoryDB import InMemoryDB as IMD
from Scheduler import Scheduler
from TwitteBitcoinScanner import TwitterBitcoinScanner as TBS
from datetime import datetime
import pytz


class TweetCoin:
    def __init__(self):
        self.tbs = TBS()
        self.imdb = IMD('sqlite.db')
        self.scheduler = Scheduler()
        self.fmp = FMP()
        #https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets =>
        #The api allows us to make up-to 180 request per 15 minute
        api_max_rate_per_min = 180 / 15 # = 12
        #  make 1 request evey 5 sec = 12 req in 1 min = 180 req in 15 min
        self.request_rate_for_new_tweets = (60 / api_max_rate_per_min) + 1   # = 5 time frame for new request

    def scan_for_new_tweets(self):
        latest_tweets = self.tbs.get_100_latest_bitcoin_tweets()
        for tweet in latest_tweets:
            self.imdb.add_or_update_tweet(tweet)
        print("Add or Updated " + str(len(latest_tweets)) + " tweets")

    def store_last_minute_tweets(self):
        print("start store tweets")
        timestamp = datetime.now(tz=pytz.utc)
        print("get_num_and_some_of_last_minute_tweets")
        last_minute_tweets, batch_sentiment_score = self.imdb.get_num_and_some_of_last_minute_tweets(timestamp)
        print("clear_last_minute")
        self.imdb.clear_last_minute(timestamp)
        bitcoin_price = self.fmp.get_stock_price("BTCUSD")
        summery = (timestamp, bitcoin_price, last_minute_tweets, batch_sentiment_score)
        print(summery)
        print(self.imdb.add_last_minute_summery(summery))
        print("the db left " + str (self.imdb.get_row_left_in_last_minute_tweets()))

    def start(self):
        # read every 5 sec the latest tweets and store then in "in-memory-db'
        self.scheduler.set_handler_for_n_second(
            self.scan_for_new_tweets,
            self.request_rate_for_new_tweets,
            1
        )

        #  every 1 min sum all latest minute tweets, and store then in other db', this function has higher priority
        self.scheduler.set_handler_for_n_second(
            self.store_last_minute_tweets,
            60,
            2
        )
        self.scheduler.run()


if __name__ == '__main__':
    tw = TweetCoin()
    tw.start()