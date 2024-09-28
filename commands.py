import re
import os

def listFiles(bucket, body, files, bucket_prefix):
    if body == '' or body == ' *':
        print(files)
        return
    if len(body) < 2:
        print('No regex provided')
        return
    regex = body[1:]
    r = re.compile(regex)
    print(list(filter(r.match, files)))


def uploadFile(bucket, body, files, bucket_prefix):
    paths = body.split('\'')[1::2]

    if len(paths) < 1:
        print('No file provided')
        return

    file_path = paths[0]
    file_name = bucket_prefix + '/' + (os.path.basename(file_path) if len(paths) < 2 else paths[1])
    try:
        response = bucket.upload_file(file_path, file_name)
        print(f'File uploaded. Response {response}')
        if file_name not in files:
            files.append(file_name)
    except Exception as e:
        print(f'Failed to upload with error {e}')


def downloadFile(bucket, body, files, bucket_prefix):
    paths = body.split('\'')[1::2]

    if len(paths) < 2:
        print('Paths not provided')
        return

    remote_path = paths[0] if paths[0].startswith(bucket_prefix + '/') else bucket_prefix + '/' + paths[0]
    local_path = paths[1]

    if not remote_path in files:
        print('File does not exist')
        return

    try:
        response = bucket.download_file(remote_path, local_path)
        print(f'File downloaded. Response {response}')
    except Exception as e:
        print(f'Failed to download with error {e}')


def deleteFile(bucket, body, files, bucket_prefix):
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


def printHelp(bucket, body, files, bucket_prefix):
    print(f"""
    Welcome to AWS CLI for buckets. 
    You're connected to bucket {bucket.name}. Your searching path is {bucket_prefix}
    Available commands:
        lst [regex]- lists all files matching regex 
        upl '[local_file_path]' '[remote_name]' - uploads file to the bucket
        dwn '[remote_file_path]' '[local_file_path]' - downloads file from the bucket
        del [regex] - deletes file matching regex
        hlp - prints this text
        cls - quits the application
    """)