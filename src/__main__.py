from livereload import Server
from build import build, build_all, ignore
from sys import exit


def serve() -> None:
    server = Server()
    server.watch("**/*", func=build, ignore=ignore)
    server.serve(root="..")


if __name__ == "__main__":
    build_all()
    # noinspection PyBroadException
    try:
        serve()
    except KeyboardInterrupt:
        exit()
    except Exception:
        serve()
