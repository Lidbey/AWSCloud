import boto3
import re
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

files = [str(file.key) for file in x_wing_bucket.objects.filter(Prefix='x-wing')]


def listFiles(bucket, body):
    if body == '':
        print(files)
        return
    if len(body) < 2:
        print('No regex provided')
        return
    regex = body[1:]
    r = re.compile(regex)
    print(list(filter(r.match, files)))


def uploadFile(bucket, body):
    paths = body.split('\'')[1::2]

    if len(paths) < 1:
        print('No file provided')
        return

    file_path = paths[0]
    file_name = BUCKET_PREFIX + '/' + (os.path.basename(file_path) if len(paths) < 2 else paths[1])
    try:
        response = bucket.upload_file(file_path, file_name)
        print(f'File uploaded. Response {response}')
        if file_name not in files:
            files.append(file_name)
    except Exception as e:
        print(f'Failed to upload with error {e}')


def downloadFile(bucket, body):
    paths = body.split('\'')[1::2]

    if len(paths) < 2:
        print('Paths not provided')
        return

    remote_path = paths[0] if paths[0].startswith(BUCKET_PREFIX+'/') else BUCKET_PREFIX + '/' + paths[0]
    local_path = paths[1]

    try:
        response = bucket.download_file(remote_path, local_path)
        print(f'File downloaded. Response {response}')
    except Exception as e:
        print(f'Failed to download with error {e}')

def deleteFile(bucket, body):
    if body == '':
        print('No regex provided')
        return
    if len(body) < 2:
        print('No regex provided')
        return
    regex = body[1:]
    r = re.compile(regex)
    l = list(filter(r.match, files))
    l_dict = [{'Key': name} for name in l]
    try:
        bucket.delete_objects(
            Delete={
                'Objects': l_dict
            }
        )
        print(f'Deleted files: {l}')
        for item in l:
            files.remove(item)
    except Exception as e:
        print(f'Failed to delete files {e}')


print(f"""
Welcome to AWS CLI for buckets. 
You're connected to bucket {BUCKET_NAME}. Your searching path is {BUCKET_PREFIX}
Available commands:
    lst [regex]- lists all files matching regex 
    upl '[local_file_path]' '[remote_name]' - uploads file to the bucket
    dwn '[remote_file_path]' '[local_file_path]' - downloads file from the bucket
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
