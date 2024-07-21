from bs4 import BeautifulSoup
from os import path, remove, rmdir
from pytest import fail

from . import build

pages_path = "test/src/pages"


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

    def test_test(self):
        """it should ignore anything in test/"""
        assert build.ignore('test/file.sass')

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

    def test_one_file(self):
        """it should parse one sass file"""
        css = [o for o in build.styles(["test/src/pages/01.sass"])]
        assert css == ["body{color:black}\n"]

    def test_two_files(self):
        """it should parse two sass files in the correct order"""
        css = [o for o in build.styles(["test/src/pages/01.sass", "test/src/pages/02.sass"])]
        assert css[0] == "body{color:black}\n"
        assert css[1] == "div{font-size:1em}\n"


class TestNav:
    def test_index(self):
        nav = [str(a) for a in build.nav(pages_path, 'test')]
        assert nav == ['<a href="page">Page</a>', '<a href="blog">Blog</a>']

    def test_page(self):
        nav = [str(a) for a in build.nav(pages_path, 'page')]
        assert nav == ['<a class="current" href="page">Page</a>', '<a href="blog">Blog</a>']


class TestPage:
    def test_index(self):
        """it should parse and append markdown to main in template for home page"""
        contents = build.page(pages_path + "/home.md", "test/src/template.html", pages_path)
        assert str(contents) == BeautifulSoup(
            "<html><head></head><body><header><nav>"
            "<a href=\"page\">Page</a><a href=\"blog\">Blog</a>"
            "</nav></header><main><p>test</p></main></body></html>",
            features="html.parser").prettify()

    def test_page(self):
        """it should build properly with an empty markdown file and update the nav"""
        contents = build.page(pages_path + "/page/page.md", "test/src/template.html", pages_path)
        assert str(contents) == BeautifulSoup(
            "<html><head></head><body><header><nav>"
            "<a class=\"current\" href=\"page\">Page</a><a href=\"blog\">Blog</a>"
            "</nav></header><main></main></body></html>",
            features="html.parser").prettify()


class TestMakePagePath:
    def test_make_home_path(self):
        file_path = build.make_page_path(pages_path + "/home.md", pages_path)
        assert file_path == ""

    def test_make_page_path(self):
        file_path = build.make_page_path(pages_path + "/page/page.md", pages_path)
        assert file_path == "page"


class TestBuild:
    buildArgs = {
        "pages_path": "test/src/pages",
        "out_path": "test",
        "template_path": "test/src/template.html"
    }
    stylesPath = "test/styles.css"

    def test_build_styles(self):
        """it should properly build the styles.css file"""
        build.build(["test/01.sass"], **self.buildArgs)
        try:
            with open(self.stylesPath) as styles:
                assert styles.read() == "body{color:black}\ndiv{font-size:1em}\n"
        except Exception as e:
            fail(str(e))
        finally:
            remove(self.stylesPath)

    def test_build_index(self):
        """it should build the specified index file, but no others"""
        build.build([pages_path + "/home.md"], **self.buildArgs)
        try:
            assert path.exists("test/index.html") is True
            assert path.exists("test/page/index.html") is False
            assert path.exists("index.html") is False
            assert path.exists(self.stylesPath) is False
        except Exception as e:
            fail(str(e))
        finally:
            remove("test/index.html")

    def test_build_mini_site(self):
        """it should build a mini site consisting of a home page,
           a styles.css, and a page in test/"""
        build.build([
            pages_path + "/home.md",
            pages_path + "/page/page.md",
            pages_path + "/blog/blog.md",
            pages_path + "/01.sass",
            pages_path + "/blog/blog.sass"
        ], **self.buildArgs)
        try:
            assert path.exists("test/index.html") is True
            assert path.exists("test/page/index.html") is True
            assert path.exists(self.stylesPath) is True
        except Exception as e:
            fail(str(e))
        finally:
            remove(self.stylesPath)
            remove("test/index.html")
            remove("test/page/index.html")
            remove("test/blog/index.html")
            rmdir("test/page/")
            rmdir("test/blog/")
