import tkinter as tk
from PIL import Image, ImageTk
# (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K")


class ChessGUI:

    CHESSBOARD_WIDTH = 8
    CHESSBOARD_HEIGHT = 8
    SQUARE_SIZE = 60  # Size of each square in pixels (adjust as needed)

    def startChessGUI(self, root, renderAsWhite, roomNumber):
        # Create the main application window
        self.renderAsWhite = renderAsWhite
        self.roomNumber = roomNumber
        # self.root = tk.Tk()
        self.window = tk.Toplevel(root)
        self.window.title("Chess Client")
        self.window.protocol("WM_DELETE_WINDOW",
                             self.closeConnectionAndDestroyWindo)
        self.selectedTile = None
        self.chessboard_canvas = tk.Canvas(self.window, width=self.SQUARE_SIZE *
                                           self.CHESSBOARD_WIDTH, height=self.SQUARE_SIZE * self.CHESSBOARD_HEIGHT)
        self.chessboard_canvas.bind("<Button-1>", self.canvasClick)

        # chessboard_canvas.create_rectangle(100, 100, 200, 200, fill="green")

        self.chessboard_canvas.pack()

        self.resetBoard()

        self.loadImages()
        self.initBoard()

        # self.root.mainloop()

    def closeConnectionAndDestroyWindo(self):
        self.closeChessWindow(self.roomNumber)
        self.window.destroy()

    def canvasClick(self, event):
        # print(f"Click: x:{event.x} y:{event.y}")
        x, y = self.getCanvasCordsFromClick(event.x, event.y)
        # print(f"Canvas coord x:{x} y:{y}")
        chessCord = self.getChessPosFromCanvasPos(x, y)
        # print(f"Chess coord {chessCord}")
        if not self.selectedTile:
            self.selectedTile = chessCord
            self.chessboard_canvas.create_rectangle(
                x*self.SQUARE_SIZE, y*self.SQUARE_SIZE, x*self.SQUARE_SIZE+self.SQUARE_SIZE, y*self.SQUARE_SIZE+self.SQUARE_SIZE, outline="#5781a1", width=3, tags="highlight")
        else:
            if chessCord == self.selectedTile:
                self.chessboard_canvas.delete("highlight")
                self.selectedTile = None
            else:
                self.sendToServer(self.selectedTile+chessCord, self.roomNumber)
                self.chessboard_canvas.delete("highlight")
                self.selectedTile = None

    def renderPieceAtPosition(self, piece, row, col):
        self.chessboard_canvas.create_image(
            col * self.SQUARE_SIZE,  row * self.SQUARE_SIZE, image=piece, anchor="nw", tags="pieces")

    def loadImages(self):
        # Load chess piece images
        self.piece_images = {
            'P': tk.PhotoImage(file="client/images/wp.png"),
            'R': tk.PhotoImage(file="client/images/wr.png"),
            'N': tk.PhotoImage(file="client/images/wn.png"),
            'B': tk.PhotoImage(file="client/images/wb.png"),
            'Q': tk.PhotoImage(file="client/images/wq.png"),
            'K': tk.PhotoImage(file="client/images/wk.png"),
            'p': tk.PhotoImage(file="client/images/bp.png"),
            'r': tk.PhotoImage(file="client/images/br.png"),
            'n': tk.PhotoImage(file="client/images/bn.png"),
            'b': tk.PhotoImage(file="client/images/bb.png"),
            'q': tk.PhotoImage(file="client/images/bq.png"),
            'k': tk.PhotoImage(file="client/images/bk.png"),
        }

    def initBoard(self):
        if self.renderAsWhite:
            for i in range(8):
                self.renderPieceAtPosition(
                    self.piece_images['P'], row=6, col=i)
                self.renderPieceAtPosition(
                    self.piece_images['p'], row=1, col=i)

            self.renderPieceAtPosition(self.piece_images['R'], row=7, col=0)
            self.renderPieceAtPosition(self.piece_images['N'], row=7, col=1)
            self.renderPieceAtPosition(self.piece_images['B'], row=7, col=2)
            self.renderPieceAtPosition(self.piece_images['Q'], row=7, col=3)
            self.renderPieceAtPosition(self.piece_images['K'], row=7, col=4)
            self.renderPieceAtPosition(self.piece_images['B'], row=7, col=5)
            self.renderPieceAtPosition(self.piece_images['N'], row=7, col=6)
            self.renderPieceAtPosition(self.piece_images['R'], row=7, col=7)

            self.renderPieceAtPosition(self.piece_images['r'], row=0, col=0)
            self.renderPieceAtPosition(self.piece_images['n'], row=0, col=1)
            self.renderPieceAtPosition(self.piece_images['b'], row=0, col=2)
            self.renderPieceAtPosition(self.piece_images['q'], row=0, col=3)
            self.renderPieceAtPosition(self.piece_images['k'], row=0, col=4)
            self.renderPieceAtPosition(self.piece_images['b'], row=0, col=5)
            self.renderPieceAtPosition(self.piece_images['n'], row=0, col=6)
            self.renderPieceAtPosition(self.piece_images['r'], row=0, col=7)
        else:
            for i in range(8):
                self.renderPieceAtPosition(
                    self.piece_images['p'], row=6, col=i)
                self.renderPieceAtPosition(
                    self.piece_images['P'], row=1, col=i)

            self.renderPieceAtPosition(self.piece_images['r'], row=7, col=0)
            self.renderPieceAtPosition(self.piece_images['n'], row=7, col=1)
            self.renderPieceAtPosition(self.piece_images['b'], row=7, col=2)
            self.renderPieceAtPosition(self.piece_images['k'], row=7, col=3)
            self.renderPieceAtPosition(self.piece_images['q'], row=7, col=4)
            self.renderPieceAtPosition(self.piece_images['b'], row=7, col=5)
            self.renderPieceAtPosition(self.piece_images['n'], row=7, col=6)
            self.renderPieceAtPosition(self.piece_images['r'], row=7, col=7)

            self.renderPieceAtPosition(self.piece_images['R'], row=0, col=0)
            self.renderPieceAtPosition(self.piece_images['N'], row=0, col=1)
            self.renderPieceAtPosition(self.piece_images['B'], row=0, col=2)
            self.renderPieceAtPosition(self.piece_images['K'], row=0, col=3)
            self.renderPieceAtPosition(self.piece_images['Q'], row=0, col=4)
            self.renderPieceAtPosition(self.piece_images['B'], row=0, col=5)
            self.renderPieceAtPosition(self.piece_images['N'], row=0, col=6)
            self.renderPieceAtPosition(self.piece_images['R'], row=0, col=7)

    def resetBoard(self):
        white = True
        for row in range(self.CHESSBOARD_HEIGHT):
            for col in range(self.CHESSBOARD_WIDTH):
                color = "#779954" if white else "#e9edcc"
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                self.chessboard_canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=color)
                white = not white
            white = not white

    def getCanvasCordsFromClick(self, x, y):
        x = x // self.SQUARE_SIZE
        y = y // self.SQUARE_SIZE
        return x, y

    def getChessPosFromCanvasPos(self, x, y):
        if self.renderAsWhite:
            rank = 8 - y
            file = chr(97+x)
        else:
            rank = y + 1
            file = chr(104-x)
        return file + str(rank)

    def renderPieceIndependentOfBoardRotation(self, piece, x, y):
        if self.renderAsWhite:
            self.renderPieceAtPosition(self.piece_images[piece], y, x)
        else:
            self.renderPieceAtPosition(
                self.piece_images[piece], 7-int(y), 7-int(x))

    def renderFEN(self, fen):
        print("HANDLING: " + fen)

        self.chessboard_canvas.delete("pieces")
        fenRows = fen.split("/")
        rowIndex = 0
        for row in fenRows:
            colIndex = 0
            for col in row:
                if col.isdigit():
                    colIndex += int(col)
                else:
                    self.renderPieceIndependentOfBoardRotation(
                        col, colIndex, rowIndex)
                    colIndex += 1
            rowIndex += 1
