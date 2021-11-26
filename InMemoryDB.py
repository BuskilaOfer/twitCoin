import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


class InMemoryDB:
    def __init__(self, database_uri):
        self.conn = create_connection(database_uri)
        self.create_db_if_not_exists()

    def create_db_if_not_exists(self):
        sql_create_last_minute_tweets_table = """ CREATE TABLE IF NOT EXISTS last_minute_tweets (
                                            id integer PRIMARY KEY,
                                            tweet_time date NOT NULL,
                                            tweet_sentiment_score integer NOT NULL
                                        ); """


        sql_create_last_two_hours_tweets_table = """ CREATE TABLE IF NOT EXISTS last_two_hours_tweets (
                                            timestamp date PRIMARY KEY,
                                            bitcoin_price integer NOT NULL,
                                            last_minute_tweets integer NOT NULL,
                                            batch_sentiment_score integer NOT NULL 
                                        ); """

        if self.conn is not None:
            self.execute_sql_query(sql_create_last_minute_tweets_table)
            self.execute_sql_query(sql_create_last_two_hours_tweets_table)
        else:
            print("Error! cannot create the database ")

    def execute_sql_query(self, create_table_sql, param=None):
        try:
            c = self.conn.cursor()
            if param is not None:
                c.execute(create_table_sql, param)
                rows = c.fetchall()
            else:
                c.execute(create_table_sql)
                rows = c.fetchall()
            self.conn.commit()
            return rows
        except Error as e:
            print(e)

    def add_or_update_tweet(self, tweet):
        add_tweet_sql = ''' INSERT OR REPLACE INTO last_minute_tweets(id,tweet_time,tweet_sentiment_score)
                  VALUES(?,?,?) '''
        self.execute_sql_query(add_tweet_sql, tweet)

    def get_all_tables (self ):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM last_minute_tweets")
        rows = cur.fetchall()
        return rows

    def get_num_and_some_of_last_minute_tweets(self, timestamp_in_utc):
        timestamp_in_utc = (timestamp_in_utc,)
        print (timestamp_in_utc)
        add_tweet_sql = ''' 
            SELECT count(*),sum(tweet_sentiment_score)
            FROM last_minute_tweets
            WHERE (( JULIANDAY('now','utc') - JULIANDAY(tweet_time,'utc') ) * 24 * 60 * 60  > 60)                   
          '''
        # execute("SELECT * FROM tasks WHERE priority=?", (priority,))
        res = self.execute_sql_query(add_tweet_sql, timestamp_in_utc)
        print(res)
        num_of_tweets = res[0][0]
        sum_of_sentiment_score = res[0][1]
        return num_of_tweets, sum_of_sentiment_score

    def clear_last_minute(self, last_time_stamp):
        remove_tweet_sql = '''DELETE FROM last_minute_tweets WHERE epoch_utm_time < ?  '''
        return self.execute_sql_query(remove_tweet_sql,(last_time_stamp,))

    def get_row_left_in_last_minute_tweets(self):
        remove_tweet_sql = '''SELECT count (*) FROM last_minute_tweets'''
        return self.execute_sql_query(remove_tweet_sql)

    def add_last_minute_summery(self, summery):
        add_tweet_sql = ''' INSERT OR REPLACE INTO last_two_hours_tweets(timestamp,bitcoin_price,batch_sentiment_score)
                  VALUES(?,?,?,?) '''
        return self.execute_sql_query(add_tweet_sql, summery)


#
# if __name__ == '__main__':

    # imb = InMemoryDB('sqlite.db')
    # imb.get_num_and_some_of_last_minute_tweets()
    # imb.clear_last_minute()
#     from datetime import datetime
#
#
#     dtt = datetime(2021, 11, 20, 17, 42, 56)
#     tweet = (123, dtt, 0, 0)
#     imb.add_tweet(tweet)
#
#     rows = imb.get_all_tables()
#     for row in rows:
#         print(row)