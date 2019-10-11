#################################################
# 15-112-n18 hw6
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################

import math
import string
import copy

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
# hw6 problems
#################################################
def areLegalValues(values):
    lenVal=len(values)
    if values==[]:
        return False
    if not int(lenVal**0.5)==lenVal**0.5:
        return False
    for i in range (lenVal):
        if not 0<=values[i]<=lenVal :
            return False
        if values[i]!=0 and values.count(values[i])>1:
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
#Test Case from hw page
assert(isLegalSudoku([
  [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
  [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
  [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
  [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
  [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
  [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
  [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
  [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
  [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
])==True)