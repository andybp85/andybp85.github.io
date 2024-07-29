from pathlib import Path
from string import Template
from unittest.mock import call, patch

import pytest

from . import build

'''
Fixtures
'''


@pytest.fixture
def template_path():
    return 'test/src/template.html'


@pytest.fixture
def build_args(template_path):
    return {'out_path': 'test',
            'pages_path': 'test/src/pages',
            'template_path': template_path}


@pytest.fixture
def home():
    return '<p>test</p>'


@pytest.fixture
def nav():
    def _nav(page):
        match page:
            case 'index':
                return '<nav><a href="/page">Page</a><a href="/blog">Blog</a></nav>'
            case 'page':
                return '<nav><a class="current" href="/page">Page</a><a href="/blog">Blog</a></nav>'
            case 'blog':
                return '<nav><a href="/page">Page</a><a class="current" href="/blog">Blog</a></nav>'

    return _nav


@pytest.fixture
def page_styles():
    def _page_styles(page):
        match page:
            case 'index':
                return '<link href="/home.css" rel="stylesheet"/>'
            case 'blog':
                return '<link href="/blog/blog.css" rel="stylesheet"/>'

    return _page_styles


@pytest.fixture
def page():
    return '<h2 id="page-id">page</h2>'


@pytest.fixture(autouse=True)
def pages_path():
    return 'test/src/pages'


@pytest.fixture
def template():
    return Template(('<html><head>$head</head><body>'
                     '<header>$header</header>'
                     '<main>$main</main></body></html>'))


@pytest.fixture
def styles_path():
    return Path('test/styles.css')


'''
Utilities
'''


@pytest.mark.usefixtures
class TestPagePath:
    def test_home_path(self, pages_path):
        file_path = build._page_path(pages_path + '/home.md', pages_path)
        assert file_path == ''

    def test_page_path(self, pages_path):
        file_path = build._page_path(pages_path + '/page/page.md', pages_path)
        assert file_path == 'page'


'''
Makers
'''


class TestMakeCss:
    def test_file(self):
        """it should parse a sass file"""
        assert build._make_css('test/src/pages/01.sass') == 'body{color:black}\n'

    def test_empty_file(self):
        """it should parse an empty sass file"""
        assert build._make_css('test/src/empty.sass') == ''


@pytest.mark.usefixtures
class TestMakeNav:
    def test_index(self, pages_path):
        """it should make the home nav with nothing marked current"""
        page_nav = [str(a) for a in build._make_nav('test', pages_path)]
        assert page_nav == ['<a href="/page">Page</a>', '<a href="/blog">Blog</a>']

    def test_page(self, pages_path):
        """it should make a page nav with the page marked current"""
        page_nav = [str(a) for a in build._make_nav('page', pages_path)]
        assert page_nav == ['<a class="current" href="/page">Page</a>', '<a href="/blog">Blog</a>']


@pytest.mark.usefixtures('home', 'nav', 'page', 'page_styles', 'template', 'template_path')
class TestMakePage:
    def test_index(self, home, nav, pages_path, template, template_path):
        """it should parse and append markdown to main in template for home page"""
        contents = build._make_page(pages_path + '/home.md', pages_path, template_path)
        assert contents == template.substitute(head='', header=nav('index'), main=home)

    def test_page(self, nav, page, pages_path, template, template_path):
        """it should build properly with an empty markdown file and update the nav"""
        contents = build._make_page(pages_path + '/page/page.md', pages_path, template_path)
        assert contents == template.substitute(head='', header=nav('page'), main=page)

    def test_add_stylesheet(self, home, nav, page, pages_path, page_styles, template,
                            template_path):
        index_contents = build._make_page(pages_path + '/home.md', pages_path, template_path,
                                          'home.css')
        assert index_contents == template.substitute(head=page_styles('index'),
                                                     header=nav('index'), main=home)
        page_contents = build._make_page(pages_path + '/blog/blog.md', pages_path, template_path,
                                         'blog/blog.css')
        assert page_contents == template.substitute(head=page_styles('blog'), header=nav('blog'),
                                                    main='')


'''
Builders
'''


@pytest.mark.build
@pytest.mark.usefixtures('build_args', 'home', 'page', 'page_styles', 'nav', 'styles_path',
                         'template')
@patch('src.build._write')
class TestBuild:
    def test_build_styles(self, mock_write, build_args, page_styles, styles_path):
        """it should properly build and sort the styles.css file from only numbered sass files"""
        build.build(['pages/01.sass'], **build_args)
        mock_write.assert_called_once_with('body{color:black}\ndiv{font-size:1em}\n', styles_path)

    def test_build_index(self, mock_write, home, build_args, nav, pages_path, page_styles,
                         template):
        """it should build the specified index file, but no others"""
        build.build([pages_path + '/home.md'], **build_args)
        mock_write.assert_called_once_with(
            template.substitute(head=page_styles('index'), header=nav('index'), main=home),
            Path('test/index.html'))

    def test_change_template(self, mock_write, build_args, home, nav, page, page_styles, template):
        """it should build the entire html site if the template is changed"""
        build.build([build_args['template_path']], **build_args)
        mock_write.assert_has_calls(
            [call(template.substitute(head=page_styles('index'), header=nav('index'), main=home),
                  Path('test/index.html')),
             call(template.substitute(head='', header=nav('page'), main=page),
                  Path('test/page/index.html')),
             call(template.substitute(head=page_styles('blog'), header=nav('blog'), main=''),
                  Path('test/blog/index.html'))])

    # TODO: handle delete
    @pytest.mark.skip
    def test_delete_md_file_and_folder(self, build_args):
        """if called with no arguments (livereload implementation detail), it should delete a
        corresponding index (and folder if empty) if a markdown file gets deleted """
        page_path = Path('test/old/index.html')
        page_path.parent.mkdir(exist_ok=True, parents=True)
        page_path.write_text('test')
        build.build([build_args['template_path']], **build_args)

    @pytest.mark.skip
    def test_delete_md_file_but_leave_folder(self):
        print(None)

    def test_build_home_styles(self, mock_write, build_args, home, nav, pages_path, page_styles,
                               template):
        """it should properly compile home.sass and append it to the home page"""
        build.build([pages_path + '/home.sass'], **build_args)
        mock_write.assert_has_calls([
            call('div{color:red}\n', Path('test/home.css')),
            call(template.substitute(
                head=page_styles('index'),
                header=nav('index'), main=home), Path('test/index.html'))])


@pytest.mark.usefixtures('build_args')
@patch('src.build.build')
class TestBuildAll:
    def test_build_all(self, mock_build, build_args):
        """it should call build.build with all Markdown and Sass files"""
        build.build_all(**build_args)
        mock_build.assert_called_once_with(
            ['test/src/pages/01.sass', 'test/src/pages/home.md', 'test/src/pages/02.sass',
             'test/src/pages/home.sass', 'test/src/pages/page/page.md',
             'test/src/pages/blog/blog.md', 'test/src/pages/blog/blog.sass'], **build_args)


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
