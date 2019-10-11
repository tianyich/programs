#################################################
# 15-112-n18 hw9
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
# Collaborated with:ziruiwan
# Solve both isKingsTour and playSudoku.
# Only isKingsTour is autograded. 
# playSudoku is manually graded by TAs. 
#################################################
from tkinter import *
import math
import copy
import random

def drawCells(canvas,data,row,col,color): #draw a cell on certain row and col
    canvas.create_rectangle(data.margin+col*data.cellSize,data.margin*2+row*data.cellSize,
                            data.margin+(col+1)*data.cellSize,data.margin*2+(row+1)*data.cellSize,
                            fill=color,width=5)
                            
def createBoard(data): #create the board filled with blue
    data.board=[]
    for row in range(data.row):
        newRow=[]
        for col in range(data.col):
            newRow.append("blue")
        data.board.append(newRow)
        
def drawBoards(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="yellow") #yellow background
    for row in range(data.row):
        for col in range(data.col):
            drawCells(canvas,data,row,col,data.board[row][col])  #draw the board cell by cell
    
def pieces(data): #pieces are stored here!
    iPiece = [
            [  True,  True,  True,  True ]
        ]
    
    jPiece = [
            [  True, False, False ],
            [  True,  True,  True ]
        ]
    
    lPiece = [
            [ False, False,  True ],
            [  True,  True,  True ]
        ]
    
    oPiece = [
            [  True,  True ],
            [  True,  True ]
        ]
    
    sPiece = [
            [ False,  True,  True ],
            [  True,  True, False ]
        ]
    
    tPiece = [
            [ False,  True, False ],
            [  True,  True,  True ]
        ]
    
    zPiece = [
            [  True,  True, False ],
            [ False,  True,  True ]
        ]
    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]

def createFallingPiece(data): #create a new falling piece in the center of the top row
    pieceIndex=random.randint(0,6)
    data.fallingPiece=data.tetrisPieces[pieceIndex]
    data.pieceColor=data.tetrisPieceColors[pieceIndex]
    data.colPiece=data.col//2-len(data.fallingPiece[0])//2
    data.rowPiece=0
    data.isFallingPieceExist=True
    
def drawFallingPiece(canvas,data):  #draw the falling piece cell by cell
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                drawCells(canvas,data,data.rowPiece+row,data.colPiece+col,data.pieceColor)
    
def movePiece(data,row,col): #move the piece due to the parameter
    data.rowPiece+=row
    data.colPiece+=col
    if not isFallingPieceLegal(data): 
        data.rowPiece-=row
        data.colPiece-=col

def isFallingPieceLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                if data.rowPiece+row>=data.row: #check if it reaches the bottom
                   data.isFallingPieceExist=False                    
                   return False
                if data.colPiece<0 or data.colPiece+len(data.fallingPiece[row])>data.col: #check left and right bound
                    return False
                if data.board[data.rowPiece+row][data.colPiece+col]!="blue": #check collision with other pieces
                    data.isFallingPieceExist=False
                    return False
    return True

def rotatePiece(data):
    fallingPiece=data.fallingPiece
    rotatedPiece=[]
    for col in range (len(fallingPiece[0])):
        newRow=[]
        for row in range(len(fallingPiece)):
            newRow.insert(0,fallingPiece[row][col])
        rotatedPiece.append(newRow)
        data.fallingPiece=rotatedPiece
    if not isFallingPieceLegal(data):
        data.fallingPiece=fallingPiece
    else: #move the rotated piece so that the center stays the same
        dCol=len(fallingPiece[0])//2-len(rotatedPiece[0])//2
        dRow=len(fallingPiece)//2-len(rotatedPiece)//2
        movePiece(data,dRow,dCol)
            
def isGameOver(data): #check if game is over
    for col in data.board[0]:
        if col!="blue":  
            data.gameOver=True
    
def drawPiece(data): #draw the piece to the board when it falls to the bottom or on the other piece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col]==True:
                data.board[data.rowPiece+row][data.colPiece+col]=data.pieceColor
    data.isFallingPieceExist=False  #boolean to check if there's a piece falling
                    
def removeLine(canvas,data): #remove the line when it is filled
    for row in data.board:
        if row.count("blue")==0:
            data.board.remove(row)
            data.board.insert(0,["blue"]*data.col) #add a new line at the top of the board
            data.score+=1

def showScore(canvas,data): #show score
    canvas.create_text(data.width/2,data.margin,text="Your Score is %d" %data.score,font="Helvetica 26")
       
def drawEndScreen(canvas,data):
    canvas.create_text(data.width/2,data.height/2,
                    text="Game Over!!!",font="Times 28")
######copied from class notes#######
####################################
# customize these functions
####################################

def init(data):
    data.row=15
    data.col=10
    createBoard(data)
    data.margin=30
    data.cellSize=(data.width-data.margin*2)//data.col
    data.rowPiece=0
    data.colPiece=0
    data.isFallingPieceExist=False
    data.fallingPiece=[]
    pieces(data)
    createFallingPiece(data)
    data.gameOver=False
    data.score=0

def mousePressed(event, data):
    createFallingPiece(data)

def keyPressed(event, data):    
    if(event.keysym=="Up"):
        rotatePiece(data)
    if(event.keysym=="Left"):
        movePiece(data,0,-1)
    if(event.keysym=="Right"):
        movePiece(data,0,1)
    if(event.keysym=="Down"):
        movePiece(data,1,0)
    

def timerFired(data):
    movePiece(data,1,0)
    
def redrawAll(canvas, data):
    drawBoards(canvas,data)
    if not data.gameOver:
        if(data.isFallingPieceExist==False):
                isGameOver(data)
                drawPiece(data)
                createFallingPiece(data)
                # if there's no falling piece, create a new one
        else:
            drawFallingPiece(canvas,data)
        removeLine(canvas,data)
        showScore(canvas,data)
    else:
        canvas.delete(ALL) 
        drawEndScreen(canvas,data)
        #clear the screen and draw the end screen shows "Game over"
####################################
# use the run function as-is
####################################

def run(width=400, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()

##########################################
def testFn():
    class Struct(object): pass
    data1 = Struct()
    data1.rows = 15
    data1.cols = 10
    data1.board = createBoard(data)
    data1.fallingPiece = pieces[0]
    rotateFallingPiece(data1) 
    assert(data1.fallingPiece == [[True],[True],[True],[True]])
    data1.fallingPiece=pieces[4]
    rotateFallingPiece(data1) 
    assert(data1.fallingPiece == [[True,False],[True,True],[False,True]])
    
    data2 = Struct()
    data2.rows = 15
    data2.cols = 10
    data2.board = createBoard(data)
    tempBoard=copy.deepcopy(data2.board)
    data2.board.replace(data2.row,["yellow"]*data2.cols)
    removeLine(canvas,data)
    assert(data2.board==tempBoard)
    
    data3 = Struct()
    data3.rows = 15
    data3.cols = 10
    data3.board = createBoard(data)
    createFallingPiece(data)
    row=data3.rowPiece
    col=data3.colPiece
    movePiece(data,1,1)
    assert(data3.rowPiece==row+1)
    assert(data3.colPiece==col-1)
    