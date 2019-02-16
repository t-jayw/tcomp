# Make a thread in the subreddit to get input on water/don't water 
import os
import praw
import sys

import reddit_config as c
import post_templates as posts
#import gpio_out as g

REDDIT_USERNAME = 'takecareofmyplant'
REDDIT_PASSWORD = 'hunter2'

# Set-up
r = c.getReddit()
sr = c.getSubReddit(r)

post_body = posts.body
post_title = posts.title

# Post Thread
post = sr.submit(post_title, selftext=post_body)
post.mod.sticky()

# Logging

#path_prefix = c.pathPrefix()
#
#with open(path_prefix+'daily_thread.txt', 'w') as f:
#    f.write(s.id)
#    f.close()
#
#with open(path_prefix+'topup.txt', 'r+') as f:
#    x = f.read()
#    if x == '1':
#      g.on_off(10)
#      True
#
## Reset continuous comment files
#with open(path_prefix+'/continuous_tally/cont_comment_log.txt', 'w') as f:
#    f.write('')
#    f.close()
#    
#with open(path_prefix+'/continuous_tally/cont_comment_id.txt', 'w') as f:
#    f.write('')
#    f.close()



