import boto3
import credentials

s3 = boto3.resource(
    service_name = 's3',
    region_name='eu-central-1',
    aws_access_key_id = credentials.KEY_ID,
    aws_secret_access_key=credentials.KEY
)

for bucket in s3.buckets.all():
    print(bucket.name)