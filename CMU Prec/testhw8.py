#################################################
# 15-112-n18 hw8
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################

import math
import string
import copy
from tkinter import *
#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# hw8 problems
#################################################
def getIndex(board,k):
    n=len(board)
    result=[]
    for i in range(n):
        for j in range(n):
            if board[i][j]==k:
                result.append(i)
                result.append(j)
    return result

#check all the conditions of moving
def isPossibleMove(board,i,j):
    n=len(board)
    result=False
    if j<n-1 and board[i][j]+1==board[i][j+1]:
        result = True
    if j>0 and board[i][j]+1==board[i][j-1]:
        result = True
    if i<n-1 and board[i][j]+1==board[i+1][j]:
        result = True
    if i>0 and board[i][j]+1==board[i-1][j]:
        result = True
    if j<n-1 and i<n-1 and board[i][j]+1==board[i+1][j+1]:
        result = True
    if j<n-1 and i>0 and board[i][j]+1==board[i-1][j+1]:
        result = True
    if j>0 and i>0 and board[i][j]+1==board[i-1][j-1]:
        result = True
    if j>0 and i<n-1 and board[i][j]+1==board[i+1][j-1]:
        result = True
    return result
    

def isKingsTour(board):
    n=len(board)
    # return False if one of the row is empty
    if board==[]:
        return False
    for row in range(n):
        if board[row]==[]:
            return False
        for col in  range(n):
            if not (isinstance(board[row][col],int) and board[row][col]>=0):
                return False
    for k in range(1,n+1,1):
        i=getIndex(board,k)[0]
        j=getIndex(board,k)[1]
        if not isPossibleMove(board,i,j):
            return False
    return True

##################################################
# playSudoku
##################################################
def startBoard():
    return [
  [ 1, 2, 3, 4, 5, 6, 7, 8, 9],
  [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
  [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
  [ 9, 5, 2, 3, 8, 1, 4, 6, 7],
  [ 6, 4, 1, 2, 9, 7, 8, 3, 5],
  [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
  [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
  [ 8, 6, 4, 9, 1, 5, 3, 7, 2],
  [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
]

#default values
def init(data):
    data.board=startBoard()
    data.originalBoard=copy.deepcopy(data.board)
    data.cellNum=len(data.board)
    data.margin=20
    data.select=(-1,-1)
    data.fill="white"
    data.isGameOver=False
    data.cellWidth=(data.width-data.margin*2)/data.cellNum
    data.cellHeight=(data.height-data.margin*2)/data.cellNum

#get the cell of given coordinate
def getCell(x,y,data):
    row = int((y - data.margin)//data.cellHeight)
    col = int((x - data.margin)//data.cellWidth)
    return(row,col)

#get the range of coordinate of given cell
def getCellCoordinate(row,col,data):
    x0=data.margin+col*data.cellWidth
    y0=data.margin+row*data.cellHeight
    x1=data.margin+(col+1)*data.cellWidth
    y1=data.margin+(row+1)*data.cellHeight
    return (x0,y0,x1,y1)

#select the cell which was clicked by the mouse
def mousePressed(event,data):
    data.select=getCell(event.x, event.y, data)

def drawSudokuBoard(canvas,data):
    for row in range(data.cellNum):
        for col in range(data.cellNum):
            (x0, y0, x1, y1) = getCellCoordinate(row, col, data)
            if (data.select == (row, col)):
                fill = "grey" #use grey to highlight selected cell
            elif (isPossibleToChange(data,row,col)):
                fill = "light grey" #use light grey to highlight cells can be changed by players
            else: 
                fill=data.fill

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill) 
    drawThickerLine(canvas,data)
    drawText(canvas,data)

def drawThickerLine(canvas,data):
    for i in range(data.cellNum+1)   :    
        if(i%(data.cellNum**0.5)==0): #draw the thicker lines
            canvas.create_line(i*data.cellWidth+data.margin,data.margin,
                            i*data.cellWidth+data.margin,data.height-data.margin,width=5)
            canvas.create_line(data.margin,i*data.cellHeight+data.margin,
                            data.width-data.margin,i*data.cellHeight+data.margin,width=5)
            
def drawText(canvas,data):
    for row in range(data.cellNum):
        for col in range(data.cellNum):
            if(data.board[row][col]!=0):
                canvas.create_text((col+0.5)*data.cellWidth+data.margin,
                            (row+0.5)*data.cellHeight+data.margin, 
                            text=str(data.board[row][col]),font="Helvetica")     
######Copied and modified from hw6######
def areLegalValues(values):
    lenVal=len(values)
    if values==[]:
        return False
    if not int(lenVal**0.5)==lenVal**0.5:
        return False
    for i in range (lenVal):
        if not isinstance(values[i],int):
            return False
        if not 0<values[i]<=lenVal :
            return False
        if values.count(values[i])>1:
            return False
    return True

def isLegalRow(board,row):
    #directly copy the list on the selected row
    rowVal=board[row]
    return areLegalValues(rowVal)
    
def isLegalCol(board,col):
    colVal=[]
    #add all the 'col'th element in each row to the list
    for i in range(len(board)):
        colVal.append(board[i][col])
    return areLegalValues(colVal)

def isLegalBlock(board,block):
    blockLen=int(len(board)**0.5)   #length of each block
    blockVal=[]
    for i in range(blockLen):
        for j in range(blockLen):
            blockVal.append(board[i+block//blockLen*blockLen][j+block%blockLen*blockLen])
    return areLegalValues(blockVal)

def isLegalSudoku(board):
    #three for-loops goes through each row,cols and blocks
    for row in range(len(board)):
        if not isLegalRow(board,row):
            return False
    for col in range(len(board[0])):
        if not isLegalCol(board,col):
            return False
    for block in range(len(board)):
        if not isLegalBlock(board,block):
            return False
    return True
############
     
#check if the cell is able to be changed by the player
def isPossibleToChange(data,row,col):
    if data.originalBoard[row][col]==0:
        return True
    else:
        return False

#the end message
def drawEndScreen(canvas,data):
    canvas.create_text(data.width/2,data.height/2,
    text="""
    Congratulations!!!
    You Win The Game!!!
    """,fill="dark blue",font="Helvetica 28 bold")
    
def keyPressed(event, data):
    pressedKey=event.keysym
    row=data.select[0]
    col=data.select[1]
    if isPossibleToChange(data,row,col):
        if event.keysym=="BackSpace":
            data.board[row][col]=""
        elif event.keysym.isdigit() and 0<int(event.keysym):
            data.board[row][col]=int(event.keysym)

#check if the game is over
def isGameOver(data):
    return isLegalSudoku(data.board)

def timerFired(data):
    pass
    
def redrawAll(canvas,data):
    if not isGameOver(data):
        drawSudokuBoard(canvas,data)
    else:
        drawEndScreen(canvas,data)
        
    
    

#copied from class notes
def run(width=700, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        #disable mouse after game is over
        if not isGameOver(data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        #disable keyboard after game is over
        if not isGameOver(data):
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
    data.timerDelay = 100 # milliseconds
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