from bs4 import BeautifulSoup
from glob import glob
from markdown import markdown
from pathlib import Path
from sass import compile as compileSass

def ignore(filePath):
    return filePath.startswith("env/") \
      or filePath.startswith("fixtures/") \
      or filePath.endswith(".py") \
      or filePath.endswith(".txt") \
      or filePath.endswith("README.md")

def styles(sassFilePaths):
    for sassFilePath in sassFilePaths:
        with open(sassFilePath, "r") as style:
            yield compileSass(string=style.read(), indented=True, output_style="compressed")

def page(mdFilePath, templatePath):
    path = str(Path(mdFilePath).parent)
    with open(mdFilePath, "r") as mdFile, open(templatePath, "r") as template:
        page = BeautifulSoup(template, features="html.parser")
        contents = BeautifulSoup(markdown(mdFile.read()), features="html.parser")
        page.find("main").append(contents)
        return path + "/index.html", page.prettify()

def build(fileList, sassFilePaths=glob("src/sass/*.sass"), templatePath="src/template.html", stylesPath="styles.css"):
    if any(file.endswith(".sass") for file in fileList):
        with open(stylesPath, "w+") as stylesFile:
            for style in styles(sassFilePaths):
                stylesFile.write(style)

    for mdFilePath in filter(lambda f: f.endswith(".md"), fileList):
        path, contents = page(mdFilePath, templatePath)
        with open(path, "w+") as file:
            file.write(contents)

