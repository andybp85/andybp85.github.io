import subprocess

from gkey import GKey
from posts import Posts


def load(event, context):

    posts = Posts(GKey().getKey())

    print(
        *posts.get(), sep='\n'
    )

    # subprocess.run("./application")
    return


load(None, None)