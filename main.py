import boto3
import credentials
import os

BUCKET_NAME = 'developer-task'
BUCKET_PREFIX = 'x-wing'
REGION = 'eu-central-1'

s3 = boto3.resource(
    service_name='s3',
    region_name=REGION,
    aws_access_key_id=credentials.KEY_ID,
    aws_secret_access_key=credentials.KEY
)

x_wing_bucket = s3.Bucket(name='developer-task')

files = [bucket.key for bucket in x_wing_bucket.objects.filter(Prefix='x-wing')]


def listFiles(bucket, body):
    if body == '':
        print(files)
        return


def uploadFile(bucket, body):
    paths = body.split('\'')[1::2]


def downloadFile(bucket, body):
    paths = body.split('\'')[1::2]


def deleteFile(bucket, body):
    if body == '':
        print('No regex provided')
        return


print(f"""
Welcome to AWS CLI for buckets. 
You're connected to bucket {BUCKET_NAME}. Your searching path is {BUCKET_PREFIX}
Available commands:
    lst [regex]- lists all files matching regex 
    upl '[local_file_path]' '[remote_name]' - uploads file named file_path to the bucket
    dwn '[remote_file_path]' '[local_file_path]' - downloads file named file_path to PATH
    del [regex] - deletes file matching regex
    cls - quits the application
""")

while True:
    command = input()
    if len(command) < 3:
        print('Unrecognized command')
        continue
    task = command[0:3]
    body = command[3:]
    if task == 'cls':
        break
    elif task == 'lst':
        listFiles(x_wing_bucket, body)
    elif task == 'upl':
        uploadFile(x_wing_bucket, body)
    elif task == 'dwn':
        downloadFile(x_wing_bucket, body)
    elif task == 'del':
        deleteFile(x_wing_bucket, body)

print('Bye!')
