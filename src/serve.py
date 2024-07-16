from bs4 import BeautifulSoup
from glob import glob
from livereload import Server
from markdown import markdown
from os import remove
from pathlib import Path
from sass import compile as compileSass
from sys import exit

def parseSassFiles(fileList):
    if not any(file.endswith(".sass") for file in fileList): return
    compileSass(dirname=("src/sass", "src/sass"), output_style="compressed")
    with open("styles.css", "w+") as styles:
        for file in glob("src/sass/*.css"):
            with open(file) as style:
                styles.write(style.read())
            remove(file)

def buildPages(fileList):
    for mdFileName in filter(lambda f: f.endswith(".md"), fileList):
        path = str(Path(mdFileName).parent)
        with open(mdFileName, "r") as mdFile, \
          open("src/template.html", "r") as template, \
          open(path + "/index.html", "w+") as index:
            page = BeautifulSoup(template, features="html.parser")
            contents = BeautifulSoup(markdown(mdFile.read()),
                                              features="html.parser")
            page.find("main").append(contents)
            index.write(page.prettify())

def build(fileList):
    parseSassFiles(fileList)
    buildPages(fileList)

def serve():
    try:
        server = Server()
        server.watch("**/*",
                     func=build,
                     ignore=lambda f: f.startswith("env/") \
                        or f == "serve.py" \
                        or f.endswith(".txt"))
        server.serve()
    except KeyboardInterrupt:
        exit()
    except Exception:
        serve()

serve()
