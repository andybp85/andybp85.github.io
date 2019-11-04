import boto3
import os
from typing import List, Dict


class Dynamo:

    def __init__(self):
        dynamo = boto3.resource(
            "dynamodb",
            aws_access_key_id=os.environ['DYNAMO_ACCESS_KEY'],
            aws_secret_access_key=os.environ['DYNAMO_SECRET_ACCESS_KEY'],
            region_name=os.environ['AWS_REGION']
        )
        self.table = dynamo.Table("blog_posts")

    def put(self, records: List[Dict]):
        with self.table.batch_writer() as batch:
            for record in records:
                batch.put_item(Item=record)

    def scan(self, **kwargs):
        return self.table.scan(**kwargs)

    def query(self, *args):
        return self.table.scan(*args)
