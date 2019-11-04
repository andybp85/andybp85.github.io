from gkey import GKey
from gdrive import GDrive
from dynamo import Dynamo


def load(event, context):

    db = Dynamo()
    db_posts = db.scan(Select='SPECIFIC_ATTRIBUTES', ProjectionExpression='id,modifiedTime')
    db_times = {p['id']: p['modifiedTime'] for p in db_posts['Items']}

    drive = GDrive(GKey().get())
    drive_posts = drive.get_posts()
    posts = []

    for post in drive_posts:
        if post['id'] not in db_times or post['modifiedTime'] > db_times[post['id']]:
            posts.append(post)

    db.put(drive.parse(posts))

    return


load(None, None)
