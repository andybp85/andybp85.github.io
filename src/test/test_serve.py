from builder import serve


def test__snapshot_maps_watched_files_to_mtimes(tmp_path):
    (tmp_path / 'posts').mkdir()
    post = tmp_path / 'posts' / 'a-post.md'
    post.write_text('hi')
    template = tmp_path / 'post_template.html'
    template.write_text('t')
    (tmp_path / 'ignored.css').write_text('not watched')
    assert set(serve._snapshot(tmp_path)) == {str(post), str(template)}
