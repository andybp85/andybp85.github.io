from glob import glob
from os import path, remove

from . import build

class TestIgnore:
    def test_env(self):
        assert build.ignore('env/file.html')

    def test_py(self):
        assert build.ignore('file.py')

    def test_txt(self):
        assert build.ignore('file.txt')

    def test_readme(self):
        assert build.ignore('README.md')

    def test_fixtures(self):
        assert build.ignore('fixtures/file.sass')

    def test_sass(self):
        assert not build.ignore('file.sass')

    def test_css(self):
        assert not build.ignore('file.css')

    def test_md(self):
        assert not build.ignore('file.mb')

    def test_html(self):
        assert not build.ignore('file.html')

class TestStyles:
    def test_DoesNothingForEmptyList(self):
        out = [o for o in build.styles([])]
        assert len(out) == 0

    def test_parsesOneSassFile(self):
        css = [o for o in build.styles(["fixtures/sass/01.sass"])]
        assert css == ["body{color:black}\n"]

    def test_parsesTwoSassFile(self):
        css = [o for o in build.styles(["fixtures/sass/01.sass", "fixtures/sass/02.sass"])]
        assert css[0] == "body{color:black}\n"
        assert css[1] == "div{font-size:1em}\n"

class TestBuildPage:
    def test_parseAndAppendMarkdownToMainInTemplate(self):
        path, contents = build.page("fixtures/test.md", "fixtures/test_template.html")
        assert path == "fixtures/index.html"
        assert contents == ("<html>\n"
                            " <head>\n"
                            " </head>\n"
                            " <body>\n"
                            "  <main>\n"
                            "   <p>\n"
                            "    test\n"
                            "   </p>\n"
                            "  </main>\n"
                            " </body>\n"
                            "</html>\n")

    def test_EmptyMarkdownFile(self):
        path, contents = build.page("fixtures/page/page.md", "fixtures/test_template.html")
        assert path == "fixtures/page/index.html"
        assert contents == ("<html>\n"
                                   " <head>\n"
                                   " </head>\n"
                                   " <body>\n"
                                   "  <main>\n"
                                   "  </main>\n"
                                   " </body>\n"
                                   "</html>\n")

class TestBuild:
    kwargs = {
        "sassFilePaths": glob("fixtures/sass/*.sass"),
        "templatePath": "fixtures/test_template.html",
        "stylesPath": "fixtures/styles.css"
    }

    def test_buildStyles(self):
        build.build(["fixtures/01.sass"], **self.kwargs)
        with open(self.kwargs["stylesPath"]) as styles:
            assert styles.read() == "body{color:black}\ndiv{font-size:1em}\n"
        remove(self.kwargs["stylesPath"])

    def test_buildPage(self):
        build.build(["fixtures/page/page.md"], **self.kwargs)
        assert path.exists("fixtures/page/index.html") == True
        assert path.exists("fixtures/index.html") == False
        assert path.exists(self.kwargs["stylesPath"]) == False
        remove("fixtures/page/index.html")

    def test_buildMiniSite(self):
        build.build([
            "fixtures/test.md",
            "fixtures/page/page.md",
            "fixtures/sass/01.sass",
            "fixtures/sass/02.sass"
        ], **self.kwargs)
        assert path.exists("fixtures/page/index.html") == True
        assert path.exists("fixtures/index.html") == True
        assert path.exists(self.kwargs["stylesPath"]) == True
        remove("fixtures/index.html")
        remove("fixtures/page/index.html")
        remove(self.kwargs["stylesPath"])
