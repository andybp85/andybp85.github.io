from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from time import sleep

from builder.build import SRC_PATH, build_all

WATCH_GLOBS = ['*.html', 'posts/*.md']


def _snapshot(base_path: Path = SRC_PATH) -> dict[str, float]:
    return {str(p): p.stat().st_mtime for g in WATCH_GLOBS for p in Path(base_path).glob(g)}


def _watch() -> None:
    seen = _snapshot()
    while True:
        sleep(1)
        now = _snapshot()
        if now != seen:
            seen = now
            print('rebuilding blog...')
            build_all()


def main() -> None:
    build_all()
    Thread(target=_watch, daemon=True).start()
    server = ThreadingHTTPServer(
        ('', 5500), partial(SimpleHTTPRequestHandler, directory=str(SRC_PATH.parent)))
    print('serving at http://localhost:5500/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
