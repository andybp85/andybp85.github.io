import os
from google.oauth2 import service_account
from googleapiclient.discovery import build


def _meta(post: dict):
    description = post.pop('description', '')
    post.update({m[0]: m[1] for m in [meta.split(": ") for meta in description.split("\n")]})
    return post


class GDrive:

    def __init__(self, key):
        creds = service_account.Credentials.from_service_account_info(key)
        self.service = build(
            "drive",
            "v3",
            credentials=creds,
            cache_discovery=False
        )

    def get_posts(self):
        results = self.service.files().list(
            pageSize=10,
            fields="files(id, name, description, modifiedTime)",
            q="'" + os.environ['GD_POSTS_FOLDER'] + "' in parents"
        ).execute()

        return [_meta(self._body(post)) for post in results.get("files", []) if post['name'][0] != "_"]

    def _body(self, post: dict):
        body = self.service.files().export_media(
            fileId=post['id'],
            mimeType="text/html"
        ).execute()

        post['body'] = body.decode("UTF-8") if isinstance(body, bytes) else ""

        return post
