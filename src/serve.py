from livereload import Server
import sass
import os
import glob

def parseSassFiles(fileList):
    if not any(file.endswith(".sass") for file in fileList): return
    sass.compile(dirname=('src/sass', 'src/sass'), output_style='compressed')
    with open('styles.css', "w") as styles:
        for file in glob.glob("src/sass/*.css"):
            with open(file) as style:
                styles.write(style.read())
            os.remove(file)

def build(fileList):
    parseSassFiles(fileList)

def ignore(filepath):
    return filepath.startswith("env/") \
        or filepath == "serve.py" \
        or filepath.endswith(".txt")

def serve():
    try:
        server = Server()
        server.watch('**/*', ignore=ignore, func=build)
        server.serve()
    except Exception:
        serve()

serve()
