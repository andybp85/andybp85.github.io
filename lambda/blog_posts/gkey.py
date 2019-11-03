import boto3
import base64
import json
import os


class GKey:

    kms = boto3.Session(
        aws_access_key_id=os.environ['S3_ACCESS_KEY'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
        region_name=os.environ['S3_REGION']
    ).client('kms')

    s3 = boto3.Session(
        aws_access_key_id=os.environ['S3_ACCESS_KEY'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY'],
        region_name=os.environ['S3_REGION']
    ).client('s3')

    def get(self):
        response = self.s3.get_object(
            Bucket=os.environ['S3_BUCKET'],
            Key=os.environ['S3_KEY']
        )

        decoded_ciphertext = base64.b64decode(response['Body'].read())
        plaintext = self.kms.decrypt(CiphertextBlob=bytes(decoded_ciphertext))

        return json.loads(plaintext['Plaintext'])
