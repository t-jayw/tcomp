import re

from psycopg2 import IntegrityError
from datetime import datetime
from db_connect import db_connect
import reddit_config as c


class ThreadVoteCounter():
  def __init__(self, praw_reddit, db_cursor, thread_id=None):
    self.Reddit = praw_reddit
    self.cur = db_cursor
    if not thread_id:
      self.thread_id = self.get_last_water_thread_id()
    else:
      self.thread_id = thread_id
    self.thread = self.Reddit.submission(id = self.thread_id)
    self.yes_regex = 'yes|aye|prost'
    self.no_regex = 'no|not on your nelly|nein'
    self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:00")

  def get_last_water_thread_id(self):
    cur = self.cur
    cur.execute('''SELECT post_id FROM water_thread_id
                ORDER BY time_stamp DESC
                LIMIT 1''')
    thread_id = cur.fetchall()
    print(thread_id)
    return thread_id[0][0]

  def count_comment_vote(self, Comment):
    text = Comment.body
    yes = re.search(self.yes_regex, text, re.IGNORECASE)
    no = re.search(self.no_regex, text, re.IGNORECASE)
    if yes and no:
      return 0
    elif yes:
      return 1
    elif no:
      return -1
    else:
      return 0

  def pull_comments(self):
    comments = self.thread.comments
    return comments

  def process_thread(self):
    '''Creates a list of tuples to be inserted to table'''
    comments = self.pull_comments()
    output = []
    for c in comments:
      output.append((self.thread_id, c.id, c.author.name,
                    c.body, self.count_comment_vote(c), self.timestamp))

    self.processed_comments = output

  def write_votes(self):
    '''Takes the list of comment tuples and inserts them into table.
    On comment_id conflict, it overwrites the record.
    On comment_author conflict, it skips--result is one vote per author
    '''

    SQL = """
      INSERT INTO thread_votes (thread_id, comment_id, comment_author,
                                comment_text, comment_vote, count_timestamp)
      VALUES(%s, %s, %s, %s, %s, %s)
      ON CONFLICT (comment_id)
      DO UPDATE SET (thread_id, comment_id, comment_author,
                     comment_text, comment_vote, count_timestamp)
      = (EXCLUDED.thread_id, EXCLUDED.comment_id, EXCLUDED.comment_author,
         EXCLUDED.comment_text, EXCLUDED.comment_vote, EXCLUDED.count_timestamp)
      """

    for c in self.processed_comments:
      print('writing: '+str(c))
      try:
        print(SQL%data)
        self.cur.execute(SQL, c)
      except IntegrityError:
        continue

if __name__=="__main__":
  r = c.getReddit()
  cur = db_connect()

  foo = ThreadVoteCounter(r, cur)
  foo.process_thread()
  foo.write_votes()
