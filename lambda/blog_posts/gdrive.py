import json
import os
import re
import subprocess
from dateutil.parser import isoparse
from functools import reduce
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GDrive:

    def __init__(self, key):
        self._parse = _compose(_slug, self._body, _tags, _meta)
        self._service = build(
            "drive",
            "v3",
            credentials=service_account.Credentials.from_service_account_info(key),
            cache_discovery=False
        )

    def get_posts(self):
        results = self._service.files().list(
            pageSize=10,
            fields="files(id, name, description, modifiedTime)",
            q="'" + os.environ['GD_POSTS_FOLDER'] + "' in parents"
        ).execute()

        return (_modified(post) for post in results.get("files", []) if post['name'][0] != "_")

    def parse(self, posts):
        print(posts)
        return _process([self._parse(post) for post in posts])

    def _body(self, post: dict):
        body = self._service.files().export_media(
            fileId=post['id'],
            mimeType="text/html"
        ).execute()

        post['body'] = body.decode("UTF-8") if isinstance(body, bytes) else ""
        return post


def _compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def _map_bodies(p: tuple):
    p[0]['body'] = p[1]
    return p[0]


def _meta(post: dict):
    description = post.pop('description', '')
    post.update({m[0]: m[1] for m in [meta.split(": ") for meta in description.split("\n")]})
    return post


def _modified(post: dict):
    modified = post.pop('modifiedTime')
    post['modifiedTime'] = round(isoparse(modified).timestamp())
    return post


def _process(posts: list):
    processed = subprocess.run(
        ["./parser", json.dumps([post['body'] for post in posts])],
        capture_output=True
    )
    bodies = json.loads(json.loads(processed.stdout))  # racket returns an escaped string
    return map(
        _map_bodies,
        zip(posts, bodies)
    )


def _slug(post: dict):
    post['slug'] = re.sub('[^-A-Za-z0-9]+', '', post['name'].replace(' ', '-')).lower()
    return post


def _tags(post: dict):
    tags = post.pop('tags')
    post['tags'] = tags.split(", ")
    return post
