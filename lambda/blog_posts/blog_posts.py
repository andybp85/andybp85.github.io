import subprocess

from gkey import GKey


def load(event, context):

    print(GKey().getKey())

    subprocess.run("./application")
    return


load(None, None)