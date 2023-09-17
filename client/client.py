from chessGUI import ChessGUI
from serverAPI import ServerAPI
import sys
from roomSelectorGUI import RoomSelectorGUI
import tkinter as tk


class Client:

    def __init__(self) -> None:

        # white = True if sys.argv[1] == "white" else False

        self.api = ServerAPI("localhost", "6060")
        self.api.handleReceivedFEN = self.handleFEN
        self.api.startConnection()
        print("Waiting for connection to server")
        if not self.api.connectedToServerEvent.wait(15):
            print("Timeout when connected to server")
            sys.exit(1)

        self.root = tk.Tk()
        self.roomNumberToGUI = {}
        self.roomSelectorgui = RoomSelectorGUI()
        self.roomSelectorgui.joinOrCreateServer = self.joinOrCreateRoom
        self.roomSelectorgui.startGUI(self.root)

        self.root.mainloop()

    def sendToServer(self, message):
        print("move " + message)
        self.api.sendMessage("move " + message)

    def handleFEN(self, fen, roomNumber):
        self.roomNumberToGUI[roomNumber].renderFEN(fen)

    def joinOrCreateRoom(self, textFromEntry):
        roomNumber = textFromEntry.split(" ")[0]
        playingAs = textFromEntry.split(" ")[1]

        self.api.sendMessage(f"create room {roomNumber} {playingAs}")
        self.api.waitForMessage()
        self.roomNumberToGUI[roomNumber] = ChessGUI()
        self.roomNumberToGUI[roomNumber].sendToServer = self.sendToServer
        renderAswhite = True if playingAs == "white" else False
        print(f"playingas={playingAs}, renderAsWhite={renderAswhite}")

        self.roomNumberToGUI[roomNumber].startChessGUI(
            self.root, renderAswhite)


def main():
    Client()


if __name__ == "__main__":
    main()
