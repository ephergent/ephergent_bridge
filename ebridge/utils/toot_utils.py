# toot_utils.py
import os
from mastodon import Mastodon
import logging

logger = logging.getLogger(__name__)

# Get you access token and instance from .env
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
MASTODON_INSTANCE = os.getenv('MASTODON_INSTANCE')

# Initialize
mastodon = Mastodon(
    access_token=ACCESS_TOKEN,
    api_base_url=MASTODON_INSTANCE
)


def send_toot(status, media_id=None):
    """ Just sends text to Mastodon,
    will attach media if media_id attached
    """
    res = mastodon.status_post(status, media_ids=media_id)
    logger.info(res)
    if res:
        logger.info(f'toot sent!')
        return res['id']
    else:
        logger.info(f'doh: {res}')
        return False


def send_media(media_file, mime_type=None, description=None):
    """ Upload ONE image to server, return the media ID """
    res = mastodon.media_post(
        media_file=media_file, mime_type=mime_type, description=description
    )
    logger.info(res)
    if res:
        logger.info(f'Image uploaded to server!')
        return res['id']
    else:
        logger.info(f'doh, image upload failed: {res}')
        return False


def make_hashtag(text):
    """ helper for hashtags """
    # remove underscore and dashes
    s = text.replace("-", " ").replace("_", " ")
    # split out words
    s = s.split()
    # if only one word, send back with
    # hashtag and capitalize
    if len(text) == 0:
        return f'#{text.capitalize()}'
    # Send back hashtag after camelcase
    return '#' + ''.join(i.capitalize() for i in s)
