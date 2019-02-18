import db_connect
import praw
import reddit_config as c

from post_templates import continuous_vote_display

cur = db_connect.db_connect()

r = c.getReddit()

### Get most recent water thread
cur.execute('''
  SELECT post_id
  FROM water_thread_id
  ORDER BY time_stamp DESC
  LIMIT 1
  ''')
thread_id = cur.fetchone()[0]
s = r.submission(thread_id)


tally_sql = """
SELECT comment_vote
FROM thread_votes
WHERE thread_id = '%s'
AND comment_vote = %i
"""

### GET YES
cur.execute(tally_sql%(thread_id, 1))
YES = len(cur.fetchall())

### GET NO
cur.execute(tally_sql%(thread_id, -1))
NO = len(cur.fetchall())

def make_bars(yes, no):
        print('making bars with YES: %i and NO: %i'%(YES, NO))
        yes_pct = round(yes*100/(yes+no))
        no_pct = round(100 - yes_pct)

        yes_bar = "`YES`: `"+"|"*(int(yes_pct/2))+"` (%d)"%(yes)
        no_bar = "`NO`: `"+"|"*(int(no_pct/2))+"` (%d)"%(no)

        return yes_bar, no_bar

def check_for_existing_comment():
    cur.execute("""SELECT comment_id
                   FROM live_vote_comment_id
                   WHERE thread_id = '%s'"""%(thread_id))
    result = cur.fetchone()
    if result:
            print('existing comment found')
            result = result[0]
    print(result)
    return result

print(thread_id)

def update_comment():
    yes, no = make_bars(YES, NO)
    continuous_score_body = continuous_vote_display%(yes, no)
    print(continuous_score_body)

    comment_id = check_for_existing_comment()
    print(comment_id)
    if comment_id:
        update = r.comment(comment_id)
        print(update)
        update.edit(continuous_score_body)
    else:
        update = s.reply(continuous_score_body)
        comment_id = update.id
        print('creating record of live vote comment')
        cur.execute('INSERT INTO live_vote_comment_id VALUES(%s, %s)',
                     (thread_id, comment_id)
                   )

    update.mod.distinguish(sticky=True)


if __name__ == '__main__':
  print('running continuous tally comment')
  update_comment()
