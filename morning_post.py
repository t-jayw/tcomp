# Make a thread in the subreddit to get input on water/don't water 
import os
import praw
import sys

import reddit_config as c
import post_templates as posts

from datetime import datetime, timedelta
from db_connect import db_connect

REDDIT_USERNAME = 'takecareofmyplant'
REDDIT_PASSWORD = 'hunter2'

# Set-up
r = c.getReddit()
sr = c.getSubReddit(r)
cur = db_connect()

# Vote history
history_sql = """
with past_seven as (
    SELECT 
        post_id
        , date_trunc('day', time_stamp) as post_date
    FROM water_thread_id 
    ORDER BY time_stamp DESC 
    LIMIT 7
    ),
past_seven_votes as (
    SELECT 
    thread_id
    , sum(comment_vote) as tally 
    FROM thread_votes 
    WHERE thread_id in (SELECT post_id FROM past_seven)
    GROUP BY thread_id 
    )

SELECT 
    substring(post_date::varchar from 0 for 11) as date, 
    thread_id, 
    CASE WHEN tally >= 0 THEN 'water' 
         ELSE 'no water' 
         END as vote_result
FROM past_seven_votes
JOIN past_seven ON thread_id = post_id
ORDER BY post_date DESC
"""
url_string = 'https://www.reddit.com/r/takecareofmyplant/comments/%s'
post_string = '[%s](%s): %s'

cur.execute(history_sql)
res = cur.fetchall()
history = []

for row in res:
  date = row[0]
  thread_id = url_string%row[1]
  outcome = row[2]
  outcome = '💧' if outcome == 'water' else '🚫'

  history.append(post_string%(date, thread_id, outcome))

print(len(history))

post_body = posts.body%(history[0], history[1], history[2], history[3],
                      history[4], history[5])
post_title = posts.title

# Post Thread
post = sr.submit(post_title, selftext=post_body)
post.mod.sticky()

# Write newly created post's ID to table
try:
  time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  post_id = str(post)

  data = (post_id, time_stamp)

  cur.execute("insert into water_thread_id values (%s, %s)", data)
except:
  print('this did not work')




