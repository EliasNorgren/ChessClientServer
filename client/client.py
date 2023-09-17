from chessGUI import ChessGUI
from serverAPI import ServerAPI
import sys
from roomSelectorGUI import RoomSelectorGUI
import tkinter as tk


class Client:

    def __init__(self) -> None:

        # white = True if sys.argv[1] == "white" else False

        self.root = tk.Tk()
        self.roomNumberToGUI = {}
        self.roomNumberToAPI = {}
        self.roomSelectorgui = RoomSelectorGUI()
        self.roomSelectorgui.joinOrCreateServer = self.joinOrCreateRoom
        self.roomSelectorgui.startGUI(self.root)

        self.root.mainloop()

    def sendToServer(self, message, roomNumber):
        print("move " + message)
        self.roomNumberToAPI[roomNumber].sendMessage("move " + message)

    def handleFEN(self, fen, roomNumber):
        self.roomNumberToGUI[roomNumber].renderFEN(fen)

    def joinOrCreateRoom(self, textFromEntry):
        roomNumber = textFromEntry.split(" ")[0]
        playingAs = textFromEntry.split(" ")[1]

        self.roomNumberToAPI[roomNumber] = ServerAPI("localhost", "6060")
        self.roomNumberToAPI[roomNumber].handleReceivedFEN = self.handleFEN
        self.roomNumberToAPI[roomNumber].startConnection()
        print("Waiting for connection to server")
        if not self.roomNumberToAPI[roomNumber].connectedToServerEvent.wait(15):
            print("Timeout when connected to server")
            sys.exit(1)

        self.roomNumberToAPI[roomNumber].sendMessage(
            f"create room {roomNumber} {playingAs}")
        self.roomNumberToAPI[roomNumber].waitForMessage()
        self.roomNumberToGUI[roomNumber] = ChessGUI()
        self.roomNumberToGUI[roomNumber].sendToServer = self.sendToServer
        self.roomNumberToGUI[roomNumber].closeChessWindow = self.closeAPIConnection
        renderAswhite = True if playingAs == "white" else False
        print(f"playingas={playingAs}, renderAsWhite={renderAswhite}")

        self.roomNumberToGUI[roomNumber].startChessGUI(
            self.root, renderAswhite, roomNumber)

    def closeAPIConnection(self, roomNumber):
        print(f"Closing in client: {roomNumber}")
        self.roomNumberToAPI[roomNumber].closeConnection()


def main():
    Client()


if __name__ == "__main__":
    main()
