import os
import praw

user_agent = os.environ['reddit_user_agent']
password = os.environ['reddit_password']
client_id = os.environ['reddit_client_id']
reddit_secret = os.environ['reddit_secret']
# PRAW
user_name = 'takecareofmyplant'
subreddit = 'takecareofmyplant'

def getReddit():
    r = praw.Reddit(client_id=client_id, client_secret=reddit_secret,
                    user_agent=user_agent, username=user_name, 
                    password=password)
    return r

def getSubReddit(Reddit, test=False):
    sub = test_sub if test else subreddit
    sr = Reddit.subreddit(sub)
    return sr





