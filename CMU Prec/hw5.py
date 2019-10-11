#################################################
# 15-112-n18 hw5
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
# hw5 problems
#################################################
import copy

def lookAndSay(a):
    result=[]
    for item in a:
        if((a.count(item),item) not in result):   #ignore repeating result
            result+=[(a.count(item),item)]
    return result

def inverseLookAndSay(a):
    result=[]
    for turple in a:
        result += [turple[1]]*turple[0]
    return result

#helperfunction to check if the word can be formed by letters in hand
def possibleToForm(word,hand):
    for c in word:
        if not word.count(c)<=hand.count(c):
            return False
    return True

#helperfunction to determine the score of a word
def wordScore(word,letterScores):
    score=0
    for c in word:
        characterNum=ord(c)-97
        score+=letterScores[characterNum]
    return score

def bestScrabbleScore(dictionary, letterScores, hand):
    bestScore=0
    bestScrabbleWord=[]
    for str in dictionary:
        if possibleToForm(str,hand):
            score=wordScore(str,letterScores)
            if(score>=bestScore):
                bestScore=score
                bestScrabbleWord+=[str]
    if bestScore==0:
        return None
    #if there's only one best word, only a string will be returned
    if len(bestScrabbleWord)==1:
        return(bestScrabbleWord[0],bestScore)
    else:
        return(bestScrabbleWord,bestScore)


#################################################
# hw5 problems
# Note:
#   There are fewer test cases than usual below.
#   You'll want to add your own!
#################################################

def _verifyLookAndSayIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    lookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

#add more test cases here!
def testLookAndSay():
    print("Testing lookAndSay()...", end="")
    assert(_verifyLookAndSayIsNondestructive() == True)
    assert(lookAndSay([]) == [])
    assert(lookAndSay([1,1,1]) ==  [(3,1)])
    assert(lookAndSay([-1,2,7]) ==  [(1,-1),(1,2),(1,7)])
    assert(lookAndSay([3,3,8,-10,-10,-10]) ==  [(2,3),(1,8),(3,-10)])
    print("Passed!")

def _verifyInverseLookAndSayIsNondestructive():
    a = [(1,2), (2,3)]
    b = copy.copy(a)
    inverseLookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

#add more test cases here!
def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(_verifyInverseLookAndSayIsNondestructive()== True)
    assert(inverseLookAndSay([]) == [])
    assert(inverseLookAndSay([(3,1)]) == [1,1,1])
    assert(inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
    print("Passed!")

#there are lots of test cases here :)
def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) == ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) == (["a", "c"], 1))
    
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) == ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) == None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) == (["xyz", "zxy"], 10))
    print(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) == (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) == ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) == ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) == None)
    print("Passed!")

#################################################
# hw5 Main
################################################

def testAll():
    testLookAndSay()
    testInverseLookAndSay()
    testBestScrabbleScore()

def main():
    testAll()

if __name__ == '__main__':
    main()
