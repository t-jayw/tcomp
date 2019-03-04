import os, requests, time
import boto3

from db_connect import db_connect

### Nest thangs
nest_device_id = os.environ['nest_device_id']
nest_api_auth = os.environ['nest_api_auth']

SCREENCAPURL = "https://www.dropcam.com/api/wwn.get_snapshot/%s?auth=%s"%(
                  nest_device_id, nest_api_auth)

r = requests.get(SCREENCAPURL)
img = r.content

timestamp = int(time.time())
file_name = str(timestamp) + "_nestScreenCapture.jpg"

with open(file_name, 'wb') as f:
  f.write(img)
  f.close()

### drop in s3
session = boto3.Session(aws_access_key_id=os.environ['s3_access_key_id'],
                      aws_secret_access_key=os.environ['s3_secret_access_key'])
s3_resource = session.resource('s3')
s3_bucket = s3_resource.Bucket(name='tcomp-nest-captures')
s3_bucket.upload_file(file_name, file_name, ExtraArgs={'ACL':'public-read'})
###

os.remove(file_name)

