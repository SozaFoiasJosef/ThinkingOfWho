import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ThinkingOfWho.settings')
django.setup()

import boto3
from django.conf import settings

s3 = boto3.client(
    's3',
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='auto',
)

# Upload a small test object
s3.put_object(
    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
    Key='test-upload.txt',
    Body=b'hello from django'
)

print("Upload successful!")

# Verify it exists
resp = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='test-upload.txt')
print("Files in bucket:", resp.get('Contents', []))