from unittest.mock import call, patch
from pathlib import Path
import pytest

from . import build


@pytest.fixture
def build_args():
    return {"pages_path": "test/src/pages",
            "out_path": "test",
            "template_path": "test/src/template.html"}


@pytest.fixture
def home():
    return "<p>test</p>"


@pytest.fixture
def nav():
    def _nav(page):
        match page:
            case "index":
                return '<nav><a href="/page">Page</a><a href="/blog">Blog</a></nav>'
            case "page":
                return '<nav><a class="current" href="/page">Page</a><a href="/blog">Blog</a></nav>'
            case "blog":
                return '<nav><a href="/page">Page</a><a class="current" href="/blog">Blog</a></nav>'

    return _nav


@pytest.fixture
def page():
    return '<h2 id="page-id">page</h2>'


@pytest.fixture(autouse=True)
def pages_path():
    return "test/src/pages"


@pytest.fixture
def template():
    return "<html><head></head><body><header>", "</header><main>", "</main></body></html>"


@pytest.fixture
def styles_path():
    return Path("test/styles.css")


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


class TestMakeCss:
    def test_empty(self):
        """it should do nothing for an empty input list"""
        out = [o for o in build.make_css([])]
        assert len(out) == 0

    def test_one_file(self):
        """it should parse one sass file"""
        css = [o for o in build.make_css(["test/src/pages/01.sass"])]
        assert css == ["body{color:black}\n"]

    def test_two_files(self):
        """it should parse two sass files in the correct order"""
        css = [o for o in build.make_css(["test/src/pages/01.sass", "test/src/pages/02.sass"])]
        assert css[0] == "body{color:black}\n"
        assert css[1] == "div{font-size:1em}\n"


@pytest.mark.usefixtures
class TestMakeNav:
    def test_index(self, pages_path):
        page_nav = [str(a) for a in build.make_nav('test', pages_path)]
        assert page_nav == ['<a href="/page">Page</a>', '<a href="/blog">Blog</a>']

    def test_page(self, pages_path):
        page_nav = [str(a) for a in build.make_nav('page', pages_path)]
        assert page_nav == ['<a class="current" href="/page">Page</a>', '<a href="/blog">Blog</a>']


@pytest.mark.usefixtures("home", "page", "nav", "template")
class TestMakePage:
    def test_index(self, home, nav, pages_path, template):
        """it should parse and append markdown to main in template for home page"""
        contents = build.make_page(pages_path + "/home.md", pages_path,
                                   "test/src/template.html")
        assert str(contents) == template[0] + nav("index") + template[1] + home + template[2]

    def test_page(self, page, pages_path, template):
        """it should build properly with an empty markdown file and update the nav"""
        contents = build.make_page(pages_path + "/page/page.md", pages_path,
                                   "test/src/template.html")
        assert str(contents) == (
                template[0]
                + '<nav><a class="current" href="/page">Page</a><a href="/blog">Blog</a></nav>'
                + template[1] + page + template[2])


@pytest.mark.usefixtures
class TestMakePagePath:
    def test_make_home_path(self, pages_path):
        file_path = build.make_page_path(pages_path + "/home.md", pages_path)
        assert file_path == ""

    def test_make_page_path(self, pages_path):
        file_path = build.make_page_path(pages_path + "/page/page.md", pages_path)
        assert file_path == "page"


@pytest.mark.build
@pytest.mark.usefixtures("build_args", "home", "page", "nav", "styles_path", "template")
@patch("src.build._write")
class TestBuild:
    def test_build_styles(self, mock_write, build_args, styles_path):
        """it should properly build the styles.css file from only numbered sass files"""
        build.build(["test/01.sass"], **build_args)
        mock_write.assert_called_once_with("body{color:black}\n\ndiv{font-size:1em}\n", styles_path)

    def test_build_index(self, mock_write, home, build_args, nav, pages_path, template):
        """it should build the specified index file, but no others"""
        build.build([pages_path + "/home.md"], **build_args)
        mock_write.assert_called_once_with(
            template[0] + nav("index") + template[1] + home + template[2],
            Path('test/index.html'))

    def test_change_template(self, mock_write, home, page, build_args, nav, template):
        """it should build the entire html site if the template is changed"""
        build.build([build_args["template_path"]], **build_args)
        print(mock_write.call_args_list)
        mock_write.assert_has_calls(
            [call(template[0] + nav("index") + template[1] + home + template[2],
                  Path('test/index.html')),
             call(template[0] + nav("page") + template[1] + page + template[2],
                  Path('test/page/index.html')),
             call(template[0] + nav("blog") + template[1] + template[2],
                  Path('test/blog/index.html'))])

    # TODO: handle delete
    @pytest.mark.skip
    def test_delete_md_file_and_folder(self, build_args):
        """if called with no arguments (livereload implementation detail), it should delete a
        corresponding index (and folder if empty) if a markdown file gets deleted """
        page_path = Path("test/old/index.html")
        page_path.parent.mkdir(exist_ok=True, parents=True)
        page_path.write_text('test')
        build.build([build_args["template_path"]], **build_args)

    @pytest.mark.skip
    def test_delete_md_file_but_leave_folder(self):
        None
