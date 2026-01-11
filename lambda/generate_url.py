import json
import boto3
import uuid
import os

s3 = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]

def handler(event, context):
    object_key = f"uploads/{uuid.uuid4()}.jpg"

    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET_NAME, "Key": object_key},
        ExpiresIn=3600
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "upload_url": url,
            "file_key": object_key
        })
    }