import reddit_config as c
from db_connect import db_connect
import post_templates as post

### Script to update the water thread

r = c.getReddit()
cur = db_connect()

### Get data
print('fetching data for wrapup thread')

LAST_THREAD_SQL = '''
SELECT post_id
FROM water_thread_id
ORDER BY time_stamp DESC
LIMIT 1
'''

VOTE_SQL = '''
SELECT 
  SUM( CASE WHEN comment_vote > 0 THEN 1 END ) as yes,
  SUM( CASE WHEN comment_vote < 0 THEN 1 END ) as no
FROM thread_votes
WHERE thread_id = (
  SELECT post_id 
  FROM water_thread_id
  ORDER BY time_stamp DESC
  LIMIT 1
  )
'''

cur.execute(LAST_THREAD_SQL)
thread_id = cur.fetchone()[0]

cur.execute(VOTE_SQL)
results = cur.fetchone()

YES = results[0]
NO = results[1]

### Do reddit tingz
print('editing the submission')

s = r.submission(thread_id)

self_text = s.selftext
wrapup = post.body_edit.format(posts.now_formatted, YES, NO)

wrapup = self_text + "\n **** \n" + wrapup

s.edit(wrapup)

print('wrapup thread posted')

