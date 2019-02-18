from db_connect import db_connect
import reddit_config as c
from VoteCounter import ThreadVoteCounter

cur = db_connect()
r = c.getReddit()

cur.execute('''SELECT DISTINCT thread_id FROM thread_votes''')

results = cur.fetchall()

for result in results:
    thread = result[0]
    vc = ThreadVoteCounter(r, cur, thread)
    vc.process_thread()
    vc.write_votes()


