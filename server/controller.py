from server import server
from chessEngine import chessEngine


def main():
    engine = chessEngine()
    srv = server(engine, 8080)


if __name__ == "__main__":
    main()
