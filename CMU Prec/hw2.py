#################################################
# 15-112-n18 hw2
# Your Name:
# Your Andrew ID:
# Your Section:
#################################################

import math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

#################################################
# hw2 problems
#################################################

def isPrime(n):
    if (n < 2):
        return False
    for factor in range(2,n):
        if (n % factor == 0):
            return False
    return True
#Cited from class notes

def rotateNumber(x):
    index=x
    counter=0
    while(index!=0):
        index//=10
        counter+=1
    d1=x%10
    d2=x//10
    return d1*(10**(counter-1))+d2

def isCircularPrime(x):
    if(x==0):
        return False
    index=x
    counter=0
    while(index!=0):
        index//=10
        counter+=1
    for i in range(0,counter):
        if(not isPrime(x)):
            return False
        x=rotateNumber(x)
    return True

def nthCircularPrime(n):
    found = 0
    guess = 0
    while (found <= n):
        guess += 1
        if (isCircularPrime(guess)):
            found += 1
    return guess

def longestDigitRun(n):
    n=abs(n)
    longestRun=1
    longestRunDigit=n%10
    currentRun=1
    index=n
    counter=0
    while(index!=0):
        index//=10
        counter+=1
    if (counter==1):
        return 1
    for j in range(0,counter):
        temp1=n%10
        n=n//10
        temp2=n%10
        if (temp1==temp2):
            currentRun+=1
        elif(currentRun>longestRun):              
            longestRun=currentRun
            longestRunDigit=temp1
            currentRun=1
        elif(currentRun==longestRun and temp1<longestRunDigit):
            longestRunDigit=temp1
            currentRun=1
        else:
            currentRun=1;
    return longestRunDigit

#################################################
# hw2 Test Functions
################################################


def testRotateNumber():
    print('Testing rotateNumber()... ', end='')
    assert(rotateNumber(1234) == 4123)
    assert(rotateNumber(4123) == 3412)
    assert(rotateNumber(3412) == 2341)
    assert(rotateNumber(2341) == 1234)
    assert(rotateNumber(5) == 5)
    assert(rotateNumber(111) == 111)
    print('Passed!')

def testIsCircularPrime():
    print('Testing isCircularPrime()... ', end='')
    assert(isCircularPrime(2) == True)
    assert(isCircularPrime(11) == True)
    assert(isCircularPrime(13) == True)
    assert(isCircularPrime(79) == True)
    assert(isCircularPrime(197) == True)
    assert(isCircularPrime(1193) == True)
    assert(isCircularPrime(42) == False)
    print('Passed!')

def testNthCircularPrime():
    print('Testing nthCircularPrime()... ', end='')
    assert(nthCircularPrime(0) == 2)
    assert(nthCircularPrime(4) == 11)
    assert(nthCircularPrime(5) == 13)
    assert(nthCircularPrime(11) == 79)
    assert(nthCircularPrime(15) == 197)
    assert(nthCircularPrime(25) == 1193)
    print('Passed!')

def testLongestDigitRun():
    print('Testing longestDigitRun()... ', end='')
    assert(longestDigitRun(117773732) == 7)
    assert(longestDigitRun(-677886) == 7)
    assert(longestDigitRun(5544) == 4)
    assert(longestDigitRun(1) == 1)
    assert(longestDigitRun(0) == 0)
    assert(longestDigitRun(22222) == 2)
    assert(longestDigitRun(111222111) == 1)
    print('Passed.')

#################################################
# hw2 Main
################################################

def testAll():
    testRotateNumber()
    testIsCircularPrime()
    testNthCircularPrime()
    testLongestDigitRun()

def main():
    testAll()

if __name__ == '__main__':
    main()
