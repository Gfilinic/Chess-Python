import pygame as p
import Game

p.init()
p.display.set_caption('Chess')
Icon = p.image.load('BackEnd\Models\icon.png')
p.display.set_icon(Icon)
WIDTH=HEIGHT=512
DIMENSIONS=8
SqSize= HEIGHT // DIMENSIONS    
Max_FPS=10
Models={}
selectedSquare=()
playerClicks=[]

def loadModels():
    chessPieces=['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in chessPieces:
        Models[piece]=p.transform.scale(p.image.load("BackEnd\Models\\"+piece+".png"),(SqSize,SqSize)) 

def highlightMoves(screen, boardState, validMoves, sqSelected):
    if sqSelected != ():
        row, column = sqSelected
        if boardState.board[row][column][0] == ("w" if  boardState.whiteTurn else "b"):
            s = p.Surface((SqSize,SqSize))
            s.set_alpha(100)
            s.fill(p.Color('yellow'))
            screen.blit(s, (column * SqSize, row * SqSize))
            s.fill(p.Color('brown'))
            for move in validMoves:
                if move.startRow == row and move.startColumn == column:
                    screen.blit(s, (move.endColumn * SqSize, move.endRow * SqSize))

def drawSquares(screen):
    colors=[p.Color("light gray"),p.Color("#999999")]
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color=colors[((row+column)%2)]
            p.draw.rect(screen,color,p.Rect(column*SqSize,row*SqSize,SqSize,SqSize)) 

def drawPieces(screen,board):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            piece=board[row][column]
            if piece != '__':
                screen.blit(Models[piece],p.Rect(column*SqSize,row*SqSize,SqSize,SqSize))    

def drawBoard(screen,boardState, validMoves, sqSelected):
    drawSquares(screen)
    highlightMoves(screen, boardState, validMoves, sqSelected)
    drawPieces(screen,boardState.board)

def setUpScreen():
    screen=p.display.set_mode((WIDTH,HEIGHT))
    screen.fill(p.Color("white"))
    return screen

def checkTheMouseClickAndMakeAMove(boardState):
    global selectedSquare,playerClicks
    location=p.mouse.get_pos()
    selectedColumn=location[0]//SqSize
    selectedRow=location[1]//SqSize
    
    if selectedSquare==(selectedRow,selectedColumn):
        selectedSquare=()
        playerClicks=[]
    else:
        selectedSquare=(selectedRow,selectedColumn)
        if len(playerClicks)==0:
            if boardState.board[selectedRow][selectedColumn]!="__":
                playerClicks.append(selectedSquare)
        else:
            playerClicks.append(selectedSquare)
            

    if len(playerClicks)==2:
        move = Game.Movement(playerClicks[0],playerClicks[1],boardState.board)
        validMoves = boardState.getValidMoves()
        for i in range(len(validMoves)):
            if move == validMoves[i]:
                move = validMoves[i]
        
        if move in validMoves:
            boardState.makeMove(move)
            print(move.getChessNotation())
            selectedSquare=()
            playerClicks=[]
        else:
            playerClicks=[selectedSquare]
         
def checkEventsAndUpdatetheBoard(active,screen,boardState,clock):
    global flagMove
    
    for e in p.event.get():
        if e.type==p.QUIT:
            active=False
            return active
        elif e.type == p.MOUSEBUTTONDOWN:
            checkTheMouseClickAndMakeAMove(boardState)
        elif e.type == p.KEYDOWN:
            if e.key == p.K_z:
                boardState.undoMove()
    validMoves = boardState.getValidMoves()
    drawBoard(screen,boardState, validMoves, selectedSquare )
    clock.tick(Max_FPS)
    p.display.flip()
    

def main():
    screen=setUpScreen()
    clock=p.time.Clock()
    boardState=Game.BoardState()
    loadModels()
    active=True
    while active:
        checkEventsAndUpdatetheBoard(active,screen,boardState,clock)
       
    
if __name__=="__main__":
    main()
