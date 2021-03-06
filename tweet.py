#!/usr/bin/env python
import tweepy
import os
import sys
import yaml
from gen_image import get_tweet


# Load twitter credentials for this bot from config file
BOTCRED_FILE = '%s/.twurlrc' % os.path.expanduser('~')
with open(BOTCRED_FILE, 'r') as credfile:
    full_config = yaml.load(credfile)
    api_key = api_key = full_config['profiles']['s_volde_trump'].keys()[0]
    bot_creds = full_config['profiles']['s_volde_trump'][api_key]

CONSUMER_KEY = bot_creds['consumer_key']
CONSUMER_SECRET = bot_creds['consumer_secret']
ACCESS_KEY = bot_creds['token']
ACCESS_SECRET = bot_creds['secret']

# Do actual authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

BOTDIR = sys.path[0]
img, alt_text = get_tweet()

"""
Steps:
    1. Updload media, return media id
    2. Annotate media id with alt text
    3. Update status and pass in media id
"""
media = api.media_upload('%s/%s' % (BOTDIR, img))
api.media_metadata_create(media.media_id, alt_text)
tweet = api.update_status(media_ids=[media.media_id])
