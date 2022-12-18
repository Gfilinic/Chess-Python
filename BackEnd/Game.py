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
        self.moveFunctions = {'P':self.getPawnMoves,'R':self.getRookMoves, 'N':self.getKnightMoves, 
                              'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteTurn = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.turnNumber = 1
        self.checkMate = False
        self.staleMate = False
            
    def makeMove(self,move):
        
        self.board[move.startRow][move.startColumn] = "__"
        self.board[move.endRow][move.endColumn] = move.pieceMovedFrom
        self.moveLog.append(move)
        self.turnNumber+=1
        self.whiteTurn = not self.whiteTurn
        if move.pieceMovedFrom == "wK":
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMovedFrom== "bK":
            self.blackKingLocation = (move.endRow, move.endColumn)
           
    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMovedFrom
            self.board[move.endRow][move.endColumn] = move.pieceMovedTo
            self.whiteTurn = not self.whiteTurn
            self.turnNumber -=1
            if move.pieceMovedFrom == "wK":
                self.whiteKingLocation = (move.startRow, move.startColumn)
            if move.pieceMovedFrom == "bK":
                self.blackKingLocation = (move.startRow, move.startColumn)
            
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteTurn:
            enemyColour = "b"
            allyColour = "w"
            kingStartRow = self.whiteKingLocation[0]
            kingStartColumn = self.whiteKingLocation[1]
        else:
            enemyColour = "w"
            allyColour = "b"
            kingStartRow = self.blackKingLocation[0]
            kingStartColumn = self.blackKingLocation[1]
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1))
        for i in range(len(directions)):
            d = directions[i]
            possiblePin = ()
            for j in range(1,8):
                endRow = kingStartRow + d[0] * j
                endColumn = kingStartColumn +d[1] * j
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece[0] == allyColour and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endColumn, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColour:
                        pieceType = endPiece[1]
                        if (0 <= i <= 3 and pieceType == 'R') or \
                           (4 <= i <= 7 and pieceType == 'B') or \
                           (j == 1 and pieceType == 'p' and ((enemyColour == "w" and 6 <= i <= 7 ) or (enemyColour == "b" and 4 <= i <= 5))) or \
                           (pieceType == "Q" ) or (j == 1 and pieceType == "K"):
                               if possiblePin == ():
                                   inCheck = True
                                   checks.append((endRow, endColumn, d[0], d[1]))
                                   break
                               else:
                                   pins.append(possiblePin)
                else:
                    break
        knightMoves = ((-2, 1), (2, 1), (-2, -1), (2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        for move in knightMoves:
            endRow = kingStartRow + move[0]
            endColumn = kingStartColumn + move[1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] == enemyColour and endPiece[1] == "N":
                    inCheck = True
                    checks.append((endRow, endColumn, move[0], move[1]))
        return inCheck, checks, pins

    def getValidMoves(self):
        moves = []
        self.inCheck, self.checks, self.pins = self.checkForPinsAndChecks()
        if self.whiteTurn:
            kingRow = self.whiteKingLocation[0]
            kingColumn = self.whiteKingLocation[1]
        else: 
            kingRow = self.blackKingLocation[0]
            kingColumn = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkColumn = check[1]
                pieceChecking = self.board[checkRow][checkColumn]
                validMoveSquares = []
                if pieceChecking[1] == "N":
                    validMoveSquares = [(checkRow, checkColumn)]
                else: 
                    for i in range(1,8):
                        validMoveSquare = (kingRow + check[2] * i, kingColumn + check[3] * i)
                        validMoveSquares.append(validMoveSquare)
                        if validMoveSquare[0] == checkRow and validMoveSquare[1] == checkColumn:
                            break
                        
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMovedFrom[1] != "K":
                        if not (moves[i].endRow ,moves[i].endColumn) in validMoveSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingColumn, moves)
        else:
            moves = self.getAllPossibleMoves()
        
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
                print("Check Mate!")
            else:
                self.staleMate = True
                print("Stale Mate!")
        else:
            self.checkMate = False
            self.staleMate = False
        return moves
                                    
    def getPawnMoves(self,row,column,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        
        if self.whiteTurn:
            if self.board[row - 1][column]=="__":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Movement((row,column), (row - 1,column), self.board))
                    if row == 6 and self.board[row - 2][column]=="__":
                        moves.append(Movement((row,column),(row - 2,column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Movement((row,column),(row - 1,column - 1), self.board))
            if column + 1 <= 7:
                  if self.board[row - 1][column + 1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Movement((row,column),(row - 1,column + 1), self.board))
    
        else:
            if self.board[row + 1][column]=="__":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Movement((row,column), (row + 1,column), self.board))
                    if row == 1 and self.board[row + 2][column]=="__":
                        moves.append(Movement((row,column),(row + 2,column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Movement((row,column),(row + 1,column - 1), self.board))
            if column + 1 <= 7:
                  if self.board[row + 1][column + 1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Movement((row,column),(row + 1,column + 1), self.board)) 

        return moves 

    def getRookMoves(self,row,column,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][column][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        
        possibleDirections = ((0,1),(1,0),(0,-1),(-1,0))
        enemyColor = "b" if self.whiteTurn else "w"
        for d in possibleDirections:
            for i in range(1,8):
                endRow = row + d[0] * i
                endColumn = column +d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    if not piecePinned or pinDirection == d or pinDirection (-d[0], -d[1]):
                        endPiece = self.board[endRow][endColumn]
                        if endPiece == "__":
                            moves.append(Movement((row,column),(endRow,endColumn),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Movement((row,column),(endRow,endColumn),self.board))
                            break
                        else:
                            break
                else:
                    break
    
    def getKnightMoves(self,row,column,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        possibleKnightMoves = ((2, 1), (2, -1), (1, 2), (1, -2), (-1, 2),(-1, -2),(-2, 1),(-2, -1))
        enemyColor = "b" if self.whiteTurn else "w"
        for move in possibleKnightMoves:
            endRow = row + move[0] 
            endColumn = column + move[1] 
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endColumn]
                    if endPiece[0] == enemyColor or endPiece == "__":
                        moves.append(Movement((row,column),(endRow,endColumn),self.board))
    
    def getBishopMoves(self,row,column,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == column:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        possibleDirections = ((1,1),(1,-1),(-1,1),(-1,-1))
        enemyColor = "b" if self.whiteTurn else "w"
        for d in possibleDirections:
            for i in range(1,8):
                endRow = row + d[0] * i
                endColumn = column +d[1] * i
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endColumn]
                        if endPiece == "__":
                            moves.append(Movement((row,column),(endRow,endColumn),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Movement((row,column),(endRow,endColumn),self.board))
                            break
                        else:
                            break
                else:
                    break
    
    def getQueenMoves(self, row, column, moves):
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)
    
    def getKingMoves(self,row,column,moves): 
        possibleKingMoves=((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
       
        enemyColor = "b" if self.whiteTurn else "w"
        for i in range (8):
            endRow = row + possibleKingMoves[i][0]
            endColumn = column + possibleKingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                endPiece = self.board[endRow][endColumn]
                if endPiece[0] == enemyColor or endPiece == "__":
                    if enemyColor == "b":
                        self.whiteKingLocation = (endRow, endColumn)
                    else: 
                        self.blackKingLocation = (endRow, endColumn)
                    inCheck, checks, pins = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Movement((row,column),(endRow,endColumn),self.board))
                    if enemyColor == "b":
                        self.whiteKingLocation = (row, column)
                    else: 
                        self.blackKingLocation = (row, column)
                 
    def getAllPossibleMoves(self):
        moves=[]
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                pieceColor = self.board[row][column][0]
                if (pieceColor=='w' and self.whiteTurn) or (pieceColor=='b' and not self.whiteTurn):
                    piece=self.board[row][column][1]
                    self.moveFunctions[piece](row,column,moves)
        return moves                
        
class Movement():
    
    numberToRows={"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0 }
    rowsToNumber={v: k for k,v in numberToRows.items()}
    lettersToColumns={"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7}
    columsToLetters={v: k for k,v in lettersToColumns.items()}  

    def __init__(self,startSquare,endSquare,board):
        self.startRow=startSquare[0]
        self.startColumn=startSquare[1]
        self.endRow=endSquare[0]
        self.endColumn=endSquare[1]
        self.pieceMovedFrom=board[self.startRow][self.startColumn]
        self.pieceMovedTo=board[self.endRow][self.endColumn]
        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn
        
         
    def __eq__(self,other):
        if isinstance(other,Movement):
            return self.moveID == other.moveID
        return False    

    
    def getChessNotation(self):
        return self.getNumberLetters(self.startRow,self.startColumn) + "->" + self.getNumberLetters(self.endRow,self.endColumn)
    
    def getNumberLetters(self,row,column):
        return self.columsToLetters[column] + self.rowsToNumber[row]