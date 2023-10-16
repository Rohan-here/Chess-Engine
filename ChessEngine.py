

class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves,
                              'N': self.getKnightMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        print(self.whiteToMove)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    def getRookMoves(self, r, c, moves):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy_piece = "w"
        if self.whiteToMove:
            enemy_piece = "b"
        for d in directions:
            for i in range(1, 8):
                new_r = r + d[0] * i
                new_c = c + d[1] * i
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                    if self.board[new_r][new_c] == "--":
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                    elif self.board[new_r][new_c][0] == enemy_piece:
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getBishopMoves(self, r, c, moves):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        enemy_piece = "w"
        if self.whiteToMove:
            enemy_piece = "b"
        for d in directions:
            for i in range(1, 8):
                new_r = r + d[0] * i
                new_c = c + d[1] * i
                if 0 <= new_r <= 7 and 0 <= new_c <= 7:
                    if self.board[new_r][new_c] == "--":
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                    elif self.board[new_r][new_c][0] == enemy_piece:
                        moves.append(Move((r, c), (new_r, new_c), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        directions = [(1, 1), (1, 0), (1, -1), (0, -1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

        if self.whiteToMove:
            enemy_piece = 'b'
        else:
            enemy_piece = 'w'
        for d in directions:
            new_r = r + d[0]
            new_c = c + d[1]
            if 0 <= new_r <= 7 and 0 <= new_c <= 7 and (self.board[new_r][new_c] == "--" or enemy_piece ==
                                                        self.board[new_r][new_c][0]):
                moves.append(Move((r, c), (new_r, new_c), self.board))

    def getKnightMoves(self, r, c, moves):
        directions = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        enemy_piece = 'w'
        if self.whiteToMove:
            enemy_piece = 'b'
        for d in directions:
            new_r = r + d[0]
            new_c = c + d[1]
            if 0 <= new_r <= 7 and 0 <= new_c <= 7 and (self.board[new_r][new_c] == "--" or enemy_piece ==
                                                        self.board[new_r][new_c][0]):
                moves.append(Move((r, c), (new_r, new_c), self.board))


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"h": 7, "g": 6, "f": 5, "e": 4, "d": 3, "c": 2, "b": 1, "a": 0}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
