import subprocess


def load(event, context):
    print('test')
    subprocess.run("./application")
    return


# load_blog_posts(None, None)