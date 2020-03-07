import tweepy
import time
from datetime import datetime
import random
import sys
import psycopg2
import os

# consumer_key = API key
consumer_key = ""
# consumer_key = API secret
consumer_secret = ""
# key = access_token
key = ""
#secret = access_token_secret
secret = ""

API_KEY_FILE = "api_key"
API_KEY_SECRET_FILE = "api_secret"
ACCESS_TOKEN_FILE = "access_token"
ACCESS_TOKEN_SECRET_FILE = "access_token_secret"

LAST_SEEN_FILE = "last_tweet_seen.txt"
ACTIVITY_FILE = "tweeter_action.txt"
INTERVAL_IN_SECONDS = 1800

# PERCENTAGE OF TWEETS TO BE RETWEETED FROM THE TARGET, USE ENTIRE NUMBERS
RANDOM_FACTOR = 25

#CONTAINS THE USER_ID WHOSE TWEETS WILL BE RETWEETED
TARGET_USER_ID = 139797989

def read_last():
    return int(read_file_and_return(LAST_SEEN_FILE))

def read_file_and_return(file_name):
    file_read = open(file_name, 'r')
    value = file_read.read().strip()
    file_read.close()
    return value

def write_last(last_seen_id):
    file_write = open(LAST_SEEN_FILE, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def find_favorite(favorites, id):
    for f in favorites:
        if f.id == id:
            return True
    return False

def write_action_log(tweet, action):
    file_append = open(ACTIVITY_FILE , 'a')
    line = str(datetime.now()) + "|" + tweet.id_str + "|" + tweet.user.name + "|" + action + "|" + "\n"
    file_append.write(line)
    file_append.close()
    return

def write_action_log_on_db(tweet, action, connection):
    cursor = connection.cursor()
    insert_log_query = f'''INSERT INTO ACTION_LOG ( TweeterID, WhenProcessed, Author, Action)
            VALUES ('{tweet.id_str}', now(),'{tweet.user.name}','{action}' ) '''
    cursor.execute(insert_log_query)
    connection.commit()
    cursor.close()
    return


def reply(tweet_number_last):
    favorites = api.favorites('SergioPL81')
    tweets = api.mentions_timeline(since_id=tweet_number_last)
    print(f"number of new mentions {len(tweets)}")

    for tweet in reversed(tweets):
        print(tweet.id_str)
        api.retweet(tweet.id)
        if("bot" in tweet.text.lower()):
            api.update_status("Hola @" + tweet.user.screen_name + " soy el bot de Sergio!")
        if (find_favorite(favorites, tweet.id) == False):
            api.create_favorite(tweet.id)
        if(tweet.id > tweet_number_last):
            tweet_number_last = tweet.id
        print(tweet.text)

    write_last(str(tweet_number_last))


def show_number_of_mentions():
    tweet_number_last = read_last()
    print(f"former last tweet number: {tweet_number_last}")


def show_number_of_retweets_of_me():
    tweets = api.retweets_of_me()
    print(f"number of retweets of me {len(tweets)}")


def show_last_20_tweets_texts():
    tweets = api.home_timeline()
    for tweet in tweets:
        print(tweet.user.name + " : " + tweet.text)


def show_last_n_tweets_from_user_deprecated(user_name, n):
    tweets = api.home_timeline(count = n)
    i = 0
    for tweet in tweets:
        i += 1
        if(tweet.user.name == user_name):
            print(tweet.user.name + " : " + tweet.text)

    print("Number of tweets read: " + str(i))


def show_last_tweets_from_user(user_id, since_id):
    max_id = 1
    tweets = api.user_timeline(id=user_id, since_id = since_id)
    for tweet in tweets:
        if(random.randrange(99) < RANDOM_FACTOR):
            print(tweet.id_str + ": " + tweet.text)
        else:
            print("skiped tweet: " + tweet.id_str)
        if(tweet.id > max_id):
            max_id = tweet.id

    return max_id


def create_table_if_needed(connection):
    cursor = connection.cursor()
    create_table_query = '''CREATE TABLE IF NOT EXISTS ACTION_LOG
          (TweeterID TEXT PRIMARY KEY     NOT NULL,
            WhenProcessed TIMESTAMP,
            Author TEXT,
            Action TEXT ); '''

    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()


def retweet_randomly_from_user(user_id):
    tweet_number_min = read_last()
    tweets = api.user_timeline(id=user_id, since_id = tweet_number_min)

    try:
        # Connection using Docker containers
        print(os.environ['PGUSER'])
        print(os.environ['PGHOST'])
        print(os.environ['PGPASSWORD'])
        print(os.environ['PGPORT'])
        print(os.environ['PGDATABASE'])
        connection = psycopg2.connect(user = os.environ['PGUSER'],
                                  password = os.environ['PGPASSWORD'],
                                  host = os.environ['PGHOST'],
                                  port =  os.environ['PGPORT'],
                                  database = os.environ['PGDATABASE'])

		# Conection using local postgres server
		#connection = psycopg2.connect(user = 'postgres',
        #                password = 'postgres',
        #                host = 'localhost',								  
        #                port =  5432,
        #                database = 'postgres')

        create_table_if_needed(connection)

        i = 0
        action = ''
        for tweet in tweets:
            i = i + 1
            if(random.randrange(100) <= RANDOM_FACTOR):
                action = 'retweet+like'
                api.retweet(tweet.id)
                api.create_favorite(tweet.id)
            else:
                action = 'ignore'

            #write_action_log(tweet, action)
            write_action_log_on_db(tweet, action, connection)

            if(tweet.id > tweet_number_min):
                tweet_number_min = tweet.id

        write_last(tweet_number_min)
        print("Number of tweets read this time: " + str(i))

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(connection):
            connection.close()


consumer_key = read_file_and_return(API_KEY_FILE)
consumer_secret = read_file_and_return(API_KEY_SECRET_FILE)
key = read_file_and_return(ACCESS_TOKEN_FILE)
secret = read_file_and_return(ACCESS_TOKEN_SECRET_FILE)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

while True:
    retweet_randomly_from_user(TARGET_USER_ID)
    time.sleep(INTERVAL_IN_SECONDS)
    print(f"waiting {INTERVAL_IN_SECONDS} seconds" )

