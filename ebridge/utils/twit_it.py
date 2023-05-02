# twit_it.py
import os
import tweepy
import logging
logger = logging.getLogger(__name__)

# Twitter Oauth keys
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
oauth_token = os.getenv('OAUTH_TOKEN')
oauth_token_secret = os.getenv('OAUTH_TOKEN_SECRET')

# Initialize the api
client = tweepy.Client(
    bearer_token=None,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=oauth_token,
    access_token_secret=oauth_token_secret
)


def send_tweet(status):
    """ Just sends text to Twitter """
    res = client.create_tweet(text=status)
    # TODO Add try/except for failed tweets
    logger.info(res)
    if res:
        logger.info(f'tweet sent!')
        return True
    else:
        logger.info(f'doh: {res}')
        return False
