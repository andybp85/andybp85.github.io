from pathlib import Path
from string import Template
from unittest.mock import ANY, call

import pytest

from . import build

'''
Fixtures
'''


@pytest.fixture
def build_args(subnav_template_path, template_path):
    return {'out_path': 'test',
            'pages_path': 'test/pages',
            'sass_partials': 'test/sass-partials',
            'subnav_template_path': subnav_template_path,
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
def page():
    return '<h2 id="page-id">page</h2>'


@pytest.fixture(autouse=True)
def pages_path():
    return 'test/pages'


@pytest.fixture
def page_styles():
    def _page_styles(page):
        match page:
            case 'index':
                return '<link href="/home.css" rel="stylesheet"/>'
            case 'blog':
                return '<link href="/blog/blog.css" rel="stylesheet"/>'
            case 'post':
                return '<link href="/blog/post/post.css" rel="stylesheet"/>'

    return _page_styles


@pytest.fixture
def styles_path():
    return Path('test/styles.css')


@pytest.fixture
def subnav():
    def _subnav(page):
        match page:
            case 'blog':
                return '<nav><a href="/blog/post">Post</a></nav>'
            case 'post':
                return '<nav><a class="current" href="/blog/post">Post</a></nav>'

        # case 'blog':
        #     return ('<nav><a --data-date="2024-07-31" --data-categories="testone testtwo" '
        #             'href="/blog/post">Post</a></nav>')
        # case 'post':
        #     return ('<nav><a --data-categories="testone testtwo" --data-date="2024-07-31" '
        #             'class="current" href="/blog/post">Post</a></nav>')

    return _subnav


@pytest.fixture
def subnav_template_path():
    return 'test/subnav_template.html'


@pytest.fixture
def template():
    return Template(('<html><head>$head</head><body>'
                     '<header>$header</header>$side_nav'
                     '<main>$main</main></body></html>\n'))


@pytest.fixture
def template_path():
    return 'test/template.html'


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


@pytest.mark.usefixtures('build_args')
class TestMakeCss:
    def test_file(self, build_args):
        """it should parse a sass file"""
        sass_file = 'test/pages/01.sass'
        assert build._make_css(sass_file, build_args['sass_partials']) == 'body{color:#000}\n'

    def test_empty_file(self, build_args):
        """it should parse an empty sass file"""
        assert build._make_css('test/empty.sass', build_args['sass_partials']) == ''

    def test_file_with_import(self, build_args):
        """it should parse a sass file"""
        sass_file = 'test/pages/blog/post/post.sass'
        assert build._make_css(sass_file,
                               build_args['sass_partials']) == 'div{color:green}div{color:blue}\n'


@pytest.mark.navs
@pytest.mark.usefixtures
class TestMakeNav:
    def test_index(self, pages_path):
        """it should make the home nav with nothing marked current"""
        page_nav = [str(a) for a in build._make_nav('', pages_path)]
        assert page_nav == ['<a href="/page">Page</a>', '<a href="/blog">Blog</a>']

    def test_page(self, pages_path):
        """it should make a page nav with the page marked current"""
        page_nav = [str(a) for a in build._make_nav('page', pages_path)]
        assert page_nav == ['<a class="current" href="/page">Page</a>', '<a href="/blog">Blog</a>']

    def test_page_with_subpages(self, pages_path):
        """it should make a subnav with no page marked current"""
        sub_nav = [str(a) for a in build._make_nav('blog', pages_path, 'blog')]
        assert sub_nav == ['<a href="/blog/post">Post</a>']

    def test_subpage(self, pages_path):
        """it should make a subnav showing which subpage we're on"""
        sub_nav = [str(a) for a in build._make_nav('post', pages_path, 'blog')]
        assert sub_nav == ['<a class="current" href="/blog/post">Post</a>']


@pytest.mark.page
@pytest.mark.usefixtures('home', 'nav', 'page', 'page_styles', 'template', 'subnav_template_path',
                         'template_path')
class TestMakePage:
    def test_index(self, home, nav, pages_path, subnav_template_path, template, template_path):
        """it should parse and append markdown to main in template for home page"""
        contents = build._make_page(pages_path + '/home.md', pages_path, '', subnav_template_path,
                                    template_path)
        assert contents == template.substitute(head='', header=nav('index'), main=home, side_nav='')

    def test_page(self, nav, page, pages_path, template, subnav_template_path, template_path):
        """it should build properly with an empty markdown file and update the nav"""
        contents = build._make_page(pages_path + '/page/page.md', pages_path, '',
                                    subnav_template_path, template_path)
        assert contents == template.substitute(head='', header=nav('page'), main=page, side_nav='')

    def test_add_stylesheet(self, home, nav, page, pages_path, page_styles, subnav,
                            subnav_template_path, template, template_path):
        index_contents = build._make_page(pages_path + '/home.md', pages_path, 'home.css',
                                          subnav_template_path, template_path)
        assert index_contents == template.substitute(head=page_styles('index'),
                                                     header=nav('index'), main=home, side_nav='')
        blog_contents = build._make_page(pages_path + '/blog/blog.md', pages_path, 'blog/blog.css',
                                         subnav_template_path, template_path)
        assert blog_contents == template.substitute(head=page_styles('blog'), header=nav('blog'),
                                                    main='', side_nav=subnav('blog'))


'''
Main
'''


@pytest.mark.build
@pytest.mark.usefixtures('build_args', 'home', 'page', 'page_styles', 'nav', 'styles_path',
                         'subnav', 'template')
class TestBuild:
    def test_build_styles(self, build_args, mocker, page_styles, styles_path):
        """it should properly build and sort the styles.css file from only numbered sass files"""
        mock_write = mocker.patch('src.build._write')

        build.build(['pages/01.sass'], **build_args)

        mock_write.assert_called_once_with(
            'body{color:#000}\ndiv{color:green}div{font-size:1em}\n',
            styles_path)

    def test_build_home_styles(self, build_args, home, mocker, nav, pages_path, page_styles,
                               template):
        """it should properly compile home.sass and append it to the home page"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([pages_path + '/home.sass'], **build_args)

        mock_mkdir.assert_called_once_with(Path('test'), ANY)
        mock_write.assert_has_calls([
            call('div{color:red}\n', Path('test/home.css')),
            call(template.substitute(
                head=page_styles('index'),
                header=nav('index'), main=home, side_nav=''), Path('test/index.html'))])

    def test_build_blog_styles(self, build_args, home, mocker, nav, pages_path, page_styles,
                               subnav, template):
        """it should properly compile and add blog.sass, and make the blog with side nav"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([pages_path + '/blog/blog.sass'], **build_args)

        mock_mkdir.assert_called_once_with(Path('test/blog'), ANY)
        mock_write.assert_has_calls([
            call('div{color:green}div{color:blue}\n', Path('test/blog/blog.css')),
            call(template.substitute(
                head=page_styles('blog'),
                header=nav('blog'), main='', side_nav=subnav('blog')),
                Path('test/blog/index.html'))])

    def test_sass_partials(self, build_args, mocker, nav, page_styles, subnav, template):
        """it should build all sass files and Markdown pages that contain the partial"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([build_args['sass_partials'] + '/_test.sass'], **build_args)

        mock_mkdir.assert_called_once_with(Path('test/blog'), ANY)
        mock_write.assert_has_calls([
            call('body{color:#000}\ndiv{color:green}div{font-size:1em}\n',
                 Path('test/styles.css')),
            call('div{color:green}div{color:blue}\n',
                 Path('test/blog/blog.css')),
            call(template.substitute(
                head=page_styles('blog'),
                header=nav('blog'), main='', side_nav=subnav('blog')),
                Path('test/blog/index.html'))])

    def test_build_index(self, home, build_args, mocker, nav, pages_path, page_styles, template):
        """it should build the specified index file and attach styles"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([pages_path + '/home.md'], **build_args)

        mock_mkdir.assert_called_once_with(Path('test'), ANY)
        mock_write.assert_called_once_with(
            template.substitute(head=page_styles('index'), header=nav('index'), main=home,
                                side_nav=''),
            Path('test/index.html'))

    def test_change_template(self, build_args, home, mocker, nav, page, pages_path, page_styles,
                             subnav, template):
        """it should build the entire html site if the template is changed"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([build_args['template_path']], **build_args)

        mock_mkdir.assert_has_calls([
            call(Path('test'), ANY),
            call(Path('test/page'), ANY),
            call(Path('test/blog'), ANY)])
        mock_write.assert_has_calls(
            [call(template.substitute(head=page_styles('index'), header=nav('index'), main=home,
                                      side_nav=''),
                  Path('test/index.html')),
             call(template.substitute(head='', header=nav('page'), main=page, side_nav=''),
                  Path('test/page/index.html')),
             call(template.substitute(head=page_styles('blog'), header=nav('blog'), main='',
                                      side_nav=subnav('blog')),
                  Path('test/blog/index.html'))])

    def test_build_subpage(self, build_args, home, mocker, nav, pages_path, page_styles, subnav,
                           template):
        """it should build a subpage with a side nav, the correct top nav, and a stylesheet"""
        mock_mkdir = mocker.patch('os.mkdir')
        mock_write = mocker.patch('src.build._write')

        build.build([pages_path + '/blog/post/post.md'], **build_args)

        mock_mkdir.assert_called_once_with(Path('test/blog/post/'), ANY)
        mock_write.assert_called_once_with(template.substitute(
            head=page_styles('post'), header=nav('blog'), main='<p>test post</p>',
            side_nav=subnav('post')),
            Path('test/blog/post/index.html'))

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


@pytest.mark.usefixtures('build_args')
class TestBuildAll:
    def test_build_all(self, build_args, mocker):
        """it should call build.build with all Markdown and Sass files"""
        mock_build = mocker.patch('src.build.build')

        build.build_all(**build_args)

        mock_build.assert_called_once_with(
            ['test/pages/01.sass', 'test/pages/home.md', 'test/pages/02.sass',
             'test/pages/home.sass', 'test/pages/page/page.md',
             'test/pages/blog/blog.md', 'test/pages/blog/blog.sass',
             'test/pages/blog/post/post.md', 'test/pages/blog/post/post.sass'],
            **build_args)


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
        assert not build.ignore('sass-partials/test.sass')
        assert not build.ignore('page/page.sass')

    def test_css(self):
        """it should not ignore css files"""
        assert not build.ignore('file.css')

    def test_md(self):
        """it should not ignore markdown files"""
        assert not build.ignore('file.mb')

    def test_html(self):
        """it should not ignore html files"""
        assert not build.ignore('file.html')
