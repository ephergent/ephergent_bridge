from flask import Blueprint, request, render_template, abort
from functools import wraps
import logging
import os
import requests
# Local imports
from ebridge.utils.toot_utils import send_toot, send_media, make_hashtag
from ebridge.utils.twit_it import send_tweet

logger = logging.getLogger(__name__)

home = Blueprint('home', __name__)
APP_KEY = os.getenv('APP_KEY')


# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('APP_KEY') and request.args.get('APP_KEY') == APP_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


# Basic site routes
@home.route('/', methods=['GET', 'POST'])
def index_get():
    """ Just a GET request """
    return render_template('index.html')


@home.route('/healthcheck')
def health_check():
    logging.debug("OK")
    return "OK"


@home.route('/webhook', methods=['POST'])
@require_appkey
def webhook():
    """ Takes data from the post, formats it into a toot and sends it to Mastodon """
    data = request.json
    logging.debug("Posted Data:")
    logging.debug(data)
    post_data = data['post']['current']
    logging.debug(post_data)
    # Parse the post data

    # Tag data
    tags = []
    for t in post_data['tags']:
        tag_dict = {'tag_name': t['name']}
        tags.append(tag_dict)

    parsed_post = {
        'post_id': post_data['id'],
        'post_uuid': post_data['uuid'],
        'title': post_data['title'],
        'url': post_data['url'],
        'excerpt': post_data['custom_excerpt'],
        'feature_image': post_data['feature_image'],
        'published': post_data['published_at'],
        'updated_at': post_data['updated_at'],
        'tags': tags,
        'visibility': post_data['visibility']
    }
    logging.debug(parsed_post)
    # Make tags into hashtags
    hashtags = ''
    for tag in parsed_post['tags']:
        t = make_hashtag(tag['tag_name'])
        hashtags += f'{t} '
    # print(f'Hashtags: \n {hashtags}')

    # Get featured image for the upload
    media_id = None
    if post_data['feature_image']:
        try:
            response = requests.get(post_data['feature_image'])
            if response.status_code == 200:
                image_data = response.content
                # Upload featured image to server
                media_id = send_media(
                    media_file=image_data,
                    mime_type=response.headers['content-type'],
                    description=post_data['title']
                )
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error: RequestException encountered while "
                  f"downloading image from {post_data['feature_image']} ({str(e)})")
            return None

    # send post to mastodon
    logging.debug("Sending post to Mastodon")
    toot = f"{parsed_post['title']}  {hashtags}  {parsed_post['url']}"
    # print(f'toot Length: {len(toot)}')
    logging.debug(toot)
    # Send it to Mastodon
    sent_toot = send_toot(status=toot, media_id=media_id)
    logging.debug(sent_toot)
    # Send it to Twitter
    tweet = f"""{parsed_post['title']}  
    
    {hashtags}
    
    {parsed_post['url']} 
    eb
    """
    sent_tweet = send_tweet(status=tweet)
    logging.debug(sent_tweet)
    return "Toot Sent"