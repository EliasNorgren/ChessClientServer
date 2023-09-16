from chessGUI import ChessGUI
from serverAPI import ServerAPI
import sys


class Client:

    def __init__(self) -> None:

        white = True if sys.argv[1] == "white" else False
        self.api = ServerAPI("localhost", "6060", "10")
        self.api.handleReceivedFEN = self.handleFEN
        self.api.startConnection()

        self.gui = ChessGUI(renderAsWhite=white)
        self.gui.sendToServer = self.sendToServer
        self.gui.startGUI()

    def sendToServer(self, message):
        print("move " + message)
        self.api.sendMessage("move " + message)

    def handleFEN(self, fen):
        self.gui.renderFEN(fen)


def main():
    Client()


if __name__ == "__main__":
    main()
