import boto3
import credentials
import commands

BUCKET_NAME = 'developer-task'
BUCKET_PREFIX = 'x-wing'
REGION = 'eu-central-1'


def mainLoop(bucket, files):
    while True:
        cmd = input()
        if len(cmd) < 3:
            print('Unrecognized command')
            continue
        task = cmd[0:3]
        body = cmd[3:]
        args = (bucket, body, files, BUCKET_PREFIX)

        cmds = {'lst': commands.listFiles,
                'upl': commands.uploadFile,
                'dwn': commands.downloadFile,
                'del': commands.deleteFile,
                'hlp': commands.printHelp}

        if task == 'cls':
            break

        if task not in cmds:
            print('Unknown command!')
            continue

        cmds[task](*args)

    print('Bye!')


def run():
    s3 = boto3.resource(
        service_name='s3',
        region_name=REGION,
        aws_access_key_id=credentials.KEY_ID,
        aws_secret_access_key=credentials.KEY
    )
    x_wing_bucket = s3.Bucket(name='developer-task')
    files = [str(file.key) for file in x_wing_bucket.objects.filter(Prefix='x-wing')]

    commands.printHelp(x_wing_bucket, None, None, BUCKET_PREFIX)

    mainLoop(x_wing_bucket, files)


run()
