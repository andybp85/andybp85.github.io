from livereload import Server
from src.build import build, ignore
from sys import exit

def serve():
    server = Server()
    server.watch("**/*", func=build, ignore=ignore)
    server.serve()

if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        exit()
    except Exception:
        serve()
