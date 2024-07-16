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
    for sassFile in glob("src/sass/*.sass"):
        with open(sassFile, "r") as style:
            yield compileSass(string=style.read(), output_style="compressed")


def buildPages(fileList):
    for mdFileName in filter(lambda f: f.endswith(".md"), fileList):
        path = str(Path(mdFileName).parent)
        with open(mdFileName, "r") as mdFile, open("src/template.html", "r") as template:
            page = BeautifulSoup(template, features="html.parser")
            contents = BeautifulSoup(markdown(mdFile.read()), features="html.parser")
            page.find("main").append(contents)
            yield path + "/index.html", page.prettify()

def build(fileList):
    with open("styles.css", "w+") as styles:
        for style in parseSassFiles(fileList):
            styles.write()
    for path, contents in buildPages(fileList):
        with open(path, "w+") as file:
            file.write(contents)

def ignore(filePath):
    return filePath.startswith("env/") \
      or filePath == "serve.py" \
      or filePath.endswith(".txt")
