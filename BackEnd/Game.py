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
        
    def makeMove(self,move):
        
        self.board[move.startRow][move.startColumn] = "__"
        self.board[move.endRow][move.endColumn] = move.pieceMovedFrom
        self.moveLog.append(move)
        
        self.whiteTurn = not self.whiteTurn
        
        
    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startColumn] = move.pieceMovedFrom
            self.board[move.endRow][move.endColumn] = move.pieceMovedTo
            self.whiteTurn = not self.whiteTurn
            
    def getValidMoves(self):
        return self.getAllPossibleMoves()
        
    
    def getPawnMoves(self,row,column,moves):
        
        if self.whiteTurn:
            print("White turn!")
            if self.board[row - 1][column]=="__":
                moves.append(Movement((row,column), (row - 1,column), self.board))
                if row == 6 and self.board[row - 2][column]=="__":
                    moves.append(Movement((row,column),(row - 2,column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves.append(Movement((row,column),(row - 1,column - 1), self.board))
            if column + 1 <= 7:
                  if self.board[row - 1][column + 1][0] == "b":
                    moves.append(Movement((row,column),(row - 1,column + 1), self.board))
    
        else:
            print("Black turn!")
            if self.board[row + 1][column]=="__":
                moves.append(Movement((row,column), (row + 1,column), self.board))
                if row == 1 and self.board[row + 2][column]=="__":
                    moves.append(Movement((row,column),(row + 2,column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    moves.append(Movement((row,column),(row + 1,column - 1), self.board))
            if column + 1 <= 7:
                  if self.board[row + 1][column + 1][0] == "w":
                    moves.append(Movement((row,column),(row + 1,column + 1), self.board)) 
                    
     
        return moves 

    def getRookMoves(self,row,column,moves):
        pass
    
    def getKnightMoves(self,row,column,moves):
        pass
    
    def getBishopMoves(self,row,column,moves):
        pass
    
    def getQueenMoves(self,row,column,moves):
        pass
    
    def getKingMoves(self,row,column,moves):
        pass
    
    def getAllPossibleMoves(self):
        print("generating all moves!")
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