#################################################
# 15-112-n18 hw7
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
# hw7 problems
#################################################

def drawStar(canvas, centerX, centerY, diameter, numPoints, color):
    dA=2*math.pi/numPoints
    outerRadius=diameter/2 
    innerRadius=diameter/2*3/8
    points=[]
    for i in range(numPoints):
        ix=centerX+innerRadius*math.cos(i*dA+math.pi/2-dA/2)
        iy=centerY-innerRadius*math.sin(i*dA+math.pi/2-dA/2)
        points+=(ix,iy)
        #angle is modified to make sure the star is pointing up
        ox=centerX+outerRadius*math.cos(i*dA+math.pi/2)
        oy=centerY-outerRadius*math.sin(i*dA+math.pi/2)
        points+=(ox,oy)
    canvas.create_polygon(points,fill=color)
        
def drawSudokuBoard(canvas, board, margin, canvasSize):
    n=len(board)
    squareSize=(canvasSize-margin*2)/n
    for i in range(n+1): #draw thinner lines
        canvas.create_line(i*squareSize+margin,margin,
                            i*squareSize+margin,canvasSize-margin)
        canvas.create_line(margin,i*squareSize+margin,
                            canvasSize-margin,i*squareSize+margin)
        if(i%(n**0.5)==0): #draw the thicker lines
            canvas.create_line(i*squareSize+margin,margin,
                            i*squareSize+margin,canvasSize-margin,width=5)
            canvas.create_line(margin,i*squareSize+margin,
                            canvasSize-margin,i*squareSize+margin,width=5)
    for j in range(n):
        for k in range(n):
            canvas.create_text((k+0.5)*squareSize+margin,
                                (j+0.5)*squareSize+margin,text=str(board[j][k]),font="Helvetica 26 bold")

#copied from class notes
def runDrawing(width=500, height=500):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    board1=[[1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,16]
    ]
    board2=[[1,2,3,4,5,6,7,8,9],
            [5,0,8,1,3,9,6,2,4],
            [4,9,6,8,7,2,1,5,3],
            [9,5,2,3,8,1,4,6,7],
            [6,4,1,2,9,7,8,3,5],
            [3,8,7,5,6,4,0,9,1],
            [7,1,9,6,2,3,5,4,8],
            [8,6,4,9,1,5,3,7,2],
            [2,3,5,7,4,8,9,1,6]
            ]
    #drawSudokuBoard(canvas,board2,15,300)
    #drawSudokuBoard(canvas,board1,20,500)
    #drawStar(canvas, 300, 200, 300, 9, "red") 
    #drawStar(canvas,250,250,300,6,"green1")
    root.mainloop()
    print("bye!")


runDrawing()