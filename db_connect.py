import psycopg2
from psycopg2.extras import DictCursor
import os
import sys
import re

def db_connect():
  db_name = os.environ['aws_db_name']
  db_user = os.environ['aws_db_user']
  db_host = os.environ['aws_db_host']
  db_password =  os.environ['aws_db_password']

  conn_string = "dbname='" + str(db_name) + "' user='" + str(db_user) + "' host='" + str(db_host) + "' password='" + str(db_password) + "'"
  print(conn_string)
  try:
    conn = psycopg2.connect(str(conn_string))
    conn.autocommit = True
  except:
    print("Unable to connect to the database")

  cur = conn.cursor(cursor_factory=DictCursor)
  return cur

secret_endpoint = os.environ['secret_endpoint']


if __name__=="__main__":
    foo = db_connect()
