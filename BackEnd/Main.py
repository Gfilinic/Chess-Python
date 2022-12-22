import pygame as p
import Game

p.init()
p.display.set_caption('Chess')
Icon = p.image.load('BackEnd\Models\icon.png')
p.display.set_icon(Icon)
BOARD_WIDTH=BOARD_HEIGHT=512
MOVE_LOG_PANEL_WIDTH = 350
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSIONS=8
SqSize= BOARD_HEIGHT // DIMENSIONS    
Max_FPS=10
Models={}
selectedSquare=()
playerClicks=[]
boardState=Game.BoardState()

def loadModels():
    chessPieces=['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in chessPieces:
        Models[piece]=p.transform.scale(p.image.load("BackEnd\Models\\"+piece+".png"),(SqSize,SqSize)) 

def highlightMoves(screen, boardState, validMoves):
    if selectedSquare != ():
        row, column = selectedSquare
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
    global colors
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

def drawBoard(screen,boardState, validMoves):
    drawSquares(screen)
    highlightMoves(screen, boardState, validMoves)
    drawPieces(screen,boardState.board)
    drawMoveLog(screen,boardState)

def setUpScreen():
    screen=p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH,BOARD_HEIGHT))
    screen.fill(p.Color("white"))
    return screen

def drawMoveLog(screen,boardState):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    font = p.font.SysFont("Arial", 16, False, False)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = boardState.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = " || "+str(i//2 + 1) + "." + str(moveLog[i]) + " | "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
    padding = 5
    lineSpacing = 2
    textY = padding
    movesPerRow = 2
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color("White"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
      
            
        

def checkTheMouseClickAndMakeAMove(boardState, screen, clock):
    global selectedSquare,playerClicks
    location=p.mouse.get_pos()
    selectedColumn=location[0]//SqSize
    selectedRow=location[1]//SqSize
    
    if selectedSquare==(selectedRow,selectedColumn) or selectedColumn >= 8:
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
            animeteMove(boardState.moveLog[-1], screen, boardState.board, clock)
            print(move.getChessNotation())
            selectedSquare=()
            playerClicks=[]
        else:
            playerClicks=[selectedSquare]
            
def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('White'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject,textLocation.move(2, 2))

def checkForGameOver(boardState, screen):
    if boardState.checkMate:
        if boardState.whiteTurn:
            drawText(screen, "Black wins by checkmate")
            return True
        else:
            drawText(screen, "White wins by checkmate")
    elif boardState.staleMate:
        drawText(screen, "Stalemate!")


def checkEventsAndUpdatetheBoard(active,screen,clock):
    global boardState
    for e in p.event.get():
        if e.type==p.QUIT:
            active=False
            return active
        elif e.type == p.MOUSEBUTTONDOWN:
            checkTheMouseClickAndMakeAMove(boardState,screen,clock)
        elif e.type == p.KEYDOWN:
            if e.key == p.K_z:
                boardState.undoMove()
            elif e.key == p.K_r:
                boardState = Game.BoardState()
                selectedSquare = ()
                playerClicks=[]
                
    
    validMoves = boardState.getValidMoves()
    drawBoard(screen,boardState, validMoves )
    checkForGameOver(boardState, screen)
    clock.tick(Max_FPS)
    p.display.flip()
    

def animeteMove(move, screen, boardState, clock):
    global colors
    coords = []
    deltaRow = move.endRow - move.startRow
    deltaColumn = move.endColumn - move.startColumn
    framesPerSquare = 5
    frameCount = (abs(deltaRow) + abs(deltaColumn)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, column = ((move.startRow + deltaRow * frame/frameCount), move.startColumn + deltaColumn * frame/frameCount)
        drawSquares(screen)
        drawPieces(screen, boardState)
        color=colors[(move.endRow + move.endColumn) % 2]
        endSquare = p.Rect(move.endColumn * SqSize, move.endRow * SqSize, SqSize, SqSize)
        p.draw.rect(screen, color, endSquare)
        if move.pieceMovedTo != "__":
            screen.blit(Models[move.pieceMovedTo], endSquare)
        screen.blit(Models[move.pieceMovedFrom], p.Rect(column * SqSize, row * SqSize, SqSize, SqSize))
        p.display.flip()
        clock.tick(60)

def main():
    screen=setUpScreen()
    clock=p.time.Clock()
    loadModels()
    active=True
    while active:
        checkEventsAndUpdatetheBoard(active,screen,clock)
       
    
if __name__=="__main__":
    main()
