class BoardState():
    def __init__(self):
        self.board=[
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['__','__','__','__','__','__','__','__'],
            ['__','__','__','__','__','__','__','__'],
            ['__','__','__','__','__','__','__','__'],
            ['__','__','__','__','__','__','__','__'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]
        self.whiteTurn = True
        self.moveLog = []
        
    def makeMove(self,move):
        from Game import Movement
        self.board[move.startRow][move.startColumn] = "__"
        self.board[move.endRow][move.endColumn] = move.pieceMovedFrom
        self.moveLog.append(move)
        self.whiteTurn= not self.whiteTurn