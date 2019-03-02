import psycopg2
import reddit_config as c
from db_connect import db_connect

r = c.getReddit()
cur = db_connect()

last_7_query = """
WITH last_7 as (
	SELECT post_id 
	FROM water_thread_id 
	ORDER by time_stamp 
	DESC limit 7),
vote_totals_last_7 as (
	SELECT comment_author, count(1) as votes
	FROM thread_votes
	WHERE thread_id IN (SELECT * FROM last_7)
	GROUP BY 1)
SELECT comment_author 
FROM vote_totals_last_7 
WHERE votes = 7
"""

cur.execute(last_7_query)
ogs = [x[0] for x in cur.fetchall()]

r = c.getReddit()
sr = c.getSubReddit(r)

for flair in sr.flair():
  if flair['flair_text'] == 'Outstanding Gardener':
    if flair['user'].name in ogs:
      continue
    else:
      sr.flair.delete(flair['user'])
      print('deleting flair from %s'%flair['user'].name)
  else:
    continue

for user in ogs:
  print('setting OG flair for %s'%user)
  sr.flair.set(user, text = 'Outstanding Gardener')


		
		
