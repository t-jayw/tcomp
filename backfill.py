from db_connect import db_connect

cur = db_connect()

cur.execute('''SELECT DISTINCT thread_id FROM thread_votes''')

threads = cur.fetchall()

print(threads)
