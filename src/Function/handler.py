import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Get the S3 client
    s3 = boto3.client('s3')

    # Fetch the S3 bucket name from an environment variable
    bucket_name = 'estudos'
    if not bucket_name:
        raise ValueError('S3 bucket name not provided')

    # Fetch the prefix (optional) from an environment variable
    prefix = os.getenv('S3_PREFIX', '')

    try:
        # List the objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        # Iterate through the objects and print the details
        for obj in response['Contents']:
            key = obj['Key']
            size = obj['Size']
            content_type = s3.head_object(Bucket=bucket_name, Key=key)['ContentType']

            print(f"File name: {key}")
            print(f"File type: {content_type}")
            print(f"File size: {size} bytes")
            print("---")

        return {
            'statusCode': 200,
            'body': 'Files processed successfully'
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            print(f"Error: S3 bucket '{bucket_name}' does not exist.")
        else:
            print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': 'Error processing files'
        }
