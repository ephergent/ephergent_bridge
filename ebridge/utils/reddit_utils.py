# reddit_utils.py

import os
import praw
import logging

logger = logging.getLogger(__name__)

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_SUBREDDIT = os.getenv('REDDIT_SUBREDDIT')

# Instantiate the API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT,
    username=REDDIT_USERNAME
)


def post_link(title=None, url=None):
    res = reddit.subreddit(
        REDDIT_SUBREDDIT).submit(
        title,
        url
    )
    logger.info(res)
    if res:
        logger.info(f'Successfully sent post to Reddit!')
        return res
    else:
        logger.info(f'doh, post submission failed: {res}')
        return False
