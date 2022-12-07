from Board import *

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

    
    def getChessNotation(self):
        return self.getNumberLetters(self.startRow,self.startColumn) + "->" + self.getNumberLetters(self.endRow,self.endColumn)
    
    def getNumberLetters(self,row,column):
        return self.columsToLetters[column] + self.rowsToNumber[row]

