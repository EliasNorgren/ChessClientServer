import chess


class chessEngine:
    def __init__(self) -> None:
        self.board = chess.Board()

    def performMove(self, move: str):
        move = chess.Move.from_uci(move)
        self.board.push(move)

    def moveIsLegal(self, move: str):
        move = chess.Move.from_uci(move)
        return move in self.board.legal_moves

    def gameIsCheckMate(self):
        return self.board.is_checkmate()

    def whitesTurn(self):
        return self.board.turn

    def getFen(self):
        return self.board.fen()
