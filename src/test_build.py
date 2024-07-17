from glob import glob
from os import path, remove

from . import build

class TestIgnore:
    def test_env(self):
        """it should ignore anything in env/"""
        assert build.ignore('env/file.html')

    def test_py(self):
        """it should ignore python files"""
        assert build.ignore('file.py')

    def test_txt(self):
        """it should ignore text files"""
        assert build.ignore('file.txt')

    def test_readme(self):
        """it should ignore readme files"""
        assert build.ignore('README.md')
        assert build.ignore('src/README.md')

    def test_fixtures(self):
        """it should ignore anything in fixtures/"""
        assert build.ignore('fixtures/file.sass')

    def test_sass(self):
        """it should not ignore sass files"""
        assert not build.ignore('file.sass')

    def test_css(self):
        """it should not ignore css files"""
        assert not build.ignore('file.css')

    def test_md(self):
        """it should not ignore markdown files"""
        assert not build.ignore('file.mb')

    def test_html(self):
        """it should not ignore html files"""
        assert not build.ignore('file.html')

class TestStyles:
    def test_empty(self):
        """it should do nothing for an empty input list"""
        out = [o for o in build.styles([])]
        assert len(out) == 0

    def test_oneFile(self):
        """it should parse one sass file"""
        css = [o for o in build.styles(["fixtures/sass/01.sass"])]
        assert css == ["body{color:black}\n"]

    def test_twoFiles(self):
        """it should parse two sass files"""
        css = [o for o in build.styles(["fixtures/sass/01.sass", "fixtures/sass/02.sass"])]
        assert css[0] == "body{color:black}\n"
        assert css[1] == "div{font-size:1em}\n"

class TestBuildPage:
    def test_index(self):
        """it should parse and append markdown to main in template for home page"""
        path, contents = build.page("test.md", "fixtures/test_template.html")
        assert path == "./index.html"
        assert contents == ("<html>\n"
                            " <head>\n"
                            " </head>\n"
                            " <body>\n"
                            "  <header>\n"
                            "   <nav>\n"
                            "    <a href=\"#\">\n"
                            "     Page\n"
                            "    </a>\n"
                            "    <a href=\"#\">\n"
                            "     Page Two\n"
                            "    </a>\n"
                            "   </nav>\n"
                            "  </header>\n"
                            "  <main>\n"
                            "   <p>\n"
                            "    test\n"
                            "   </p>\n"
                            "  </main>\n"
                            " </body>\n"
                            "</html>\n")

    def test_page(self):
        """it should build properly with an empty markdown file and update the nav"""
        path, contents = build.page("fixtures/Page.md", "fixtures/test_template.html")
        assert path == "fixtures/index.html"
        assert contents == ("<html>\n"
                            " <head>\n"
                            " </head>\n"
                            " <body>\n"
                            "  <header>\n"
                            "   <nav>\n"
                            "    <a class=\"current\" href=\"#\">\n"
                            "     Page\n"
                            "    </a>\n"
                            "    <a href=\"#\">\n"
                            "     Page Two\n"
                            "    </a>\n"
                            "   </nav>\n"
                            "  </header>\n"
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
        """it should properly build the stlyes.css file"""
        build.build(["fixtures/01.sass"], **self.kwargs)
        with open(self.kwargs["stylesPath"]) as styles:
            assert styles.read() == "body{color:black}\ndiv{font-size:1em}\n"
        remove(self.kwargs["stylesPath"])

    def test_buildPage(self):
        """it should build the specified index file, but no others"""
        build.build(["fixtures/Page.md"], **self.kwargs)
        assert path.exists("fixtures/index.html") == True
        assert path.exists("index.html") == False
        assert path.exists(self.kwargs["stylesPath"]) == False
        remove("fixtures/index.html")

    def test_buildMiniSite(self):
        """it should build a mini site consisting of a home page,
           a styles.css, and a page in fixtures/"""
        build.build([
            "test.md",
            "fixtures/Page.md",
            "fixtures/sass/01.sass",
            "fixtures/sass/02.sass"
        ], **self.kwargs)
        assert path.exists("fixtures/index.html") == True
        assert path.exists("index.html") == True
        assert path.exists(self.kwargs["stylesPath"]) == True
        remove("index.html")
        remove("fixtures/index.html")
        remove(self.kwargs["stylesPath"])
