I have don this project only to learn about Python and about container integration with Docker, if you have get here looking by
a real bot for tweeter this may not be the right project for you, making this solution to run is neither very easy nor very well explained.

This project contains a simple tweeter bot based on Python designed to be run from postgres. It will retweet and like the tweets from a UserId, 
it relies on the tweepy library: 

http://docs.tweepy.org/en/latest/api.html


In order to make this bot work, a developer tweeter account needs to be created and the developer keys and secrets need to be copied in 
the files "access_token", "access_token_secret", "api_key" and "api_key_secret" of your local repository, my keys are not shared in 
this repository for obvious reasons.

The UserID whose tweets will be retweeted is specified in the TARGET_USER_ID, notice that the UserID is not an obvious parameter in
Tweeter but it can be retrieved from a call to api.user_timeline by passing the user's name.

The program stores the last tweet number in the "last_tweet_seen.txt" file so that it only looks for tweets later than that number.

There is an option to retweet and reply only a part of the tweets randomly by using the RANDOM_FACTOR, a value of 100 or higher would retweet
all the tweets while a value of 0 would retweet none.

The retweets can be seen in tweeter but a telling what messages have been retweeted is available in a postgres database.

The program is prepared to run for ever, it checks new tweets each half an hour (1800 seconds). This quantity that can be in the variable INTERVAL_IN_SECONDS.


INSTRUCTIONS FOR DOCKER

- Start Docker, open the command prompt and from the repository folder, 
  execute the following command to start the container:
  
  docker-compose up
  
  After the Postgres and tweeter_bot containers are running, the ACTION_LOG should have records, you can run this query to verify that.
  
  
  docker exec -it my_postgres psql -U postgres -c "SELECT * FROM ACTION_LOG;”
  
  





