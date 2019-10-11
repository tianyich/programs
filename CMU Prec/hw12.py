#################################################
# 15-112-n18 hw12
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################
import copy
import time
def solveSudoku(board):
    emptyCell=findEmptyCell(board)
    return backTracking(board,emptyCell,0)
    
def findEmptyCell(board): #find the rows and cols all the empty cells and add them into a list
    result=[]
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]==0:
                result.append([row,col])
    return result

def backTracking(board,emptyCell,index):
    solvedBoard=copy.deepcopy(board)
    if isFilledBoard(solvedBoard):
        return solvedBoard
    else:
        row=emptyCell[index][0]
        col=emptyCell[index][1]
        for num in range(1,10):
            if(isLegalCell(board,row,col,num)):
                solvedBoard[row][col]=num
                solution=backTracking(solvedBoard,emptyCell,index+1) 
                if solution!=None:
                    return solution
                solvedBoard[row][col]=0
        return None
            
def isLegalCell(board,row,col,num): 
    if not isLegalBlock(board,num,row,col):
        return False
    if not isLegalCol(board,num,col):
        return False
    if not isLegalRow(board,num,row):
        return False
    return True

def isFilledBoard(board): #check if the board is filled
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]==0:
                return False
    return True
#####copied and modified from hw6#####
def isLegalRow(board,num,row): #check each row 
    for i in range(len(board)):
        if board[row][i]==num:
            return False
    return True
    
def isLegalCol(board,num,col):#check each col
    for i in range(len(board)):
        if board[i][col]==num:
            return False
    return True

def isLegalBlock(board,num,row,col):#check each block
    for i in range(3):
        for j in range(3):
            if board[i+row//3*3][j+col//3*3]==num:
                return False
    return True

######Test Case######
def testSolveSudoku():
    print('Testing solveSudoku()...', end='')
    board = [
              [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
              [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
              [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
              [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
              [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
              [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
              [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
              [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
              [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
            ]
    solved = solveSudoku(board)
    solution = [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
               ]
    assert(solved == solution)
    print('Passed!')
    