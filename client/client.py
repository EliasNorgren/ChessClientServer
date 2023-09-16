from chessGUI import ChessGUI
from serverAPI import ServerAPI


class Client:

    def __init__(self) -> None:
        self.api = ServerAPI("localhost", "8080", "10")
        self.api.startConnection()

        self.gui = ChessGUI()
        self.gui.buttonClick = self.buttonClick
        self.gui.startGUI()

    def buttonClick(self, message):
        self.api.sendMessage(message)


def main():
    Client()


if __name__ == "__main__":
    main()
