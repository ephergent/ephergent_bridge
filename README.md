# ephergent_bridge

A bridge for sharing Ghost posts to Mastodon and Twitter

## The Setup

You will need a key from the Mastodon instance you live in.

You will also need to set up an integration in your Ghost blog to post a webhook to where you are hosting the Ivory Bridge.

```
Example:  https://YOUR_HOST/?APP_KEY=YOUR_SECRET_FOR_THE_GHOST_INTEGRATION
```

### API Key authentication setup:

- Copy `env-example` to `.env`
- Read the `.env` file as it point to where to get the keys
- Edit it for your setup
- Source it `source .env`

### Python setup:

- Clone the repo: `git clone https://github.com/ephergent/ephergent_bridge.git`
- Change into the directory: `cd ephergent_bridge`
- Create a virtual environment: `virtualenv -p pytho3 venv`
- Source it: `source venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`

### Run it:

- Run the Flask app: `python run.py`
