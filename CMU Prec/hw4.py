#################################################
# 15-112-n18 hw4
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################

import math
import string

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)


#################################################
# hw3 problems
#################################################

#helper function to find out the longest common substring strating from the begining of each string
def helperLongestSubstring(s1,s2):
    commonSubstring=""
    #find the shorter string 
    if(len(s1)>len(s2)):
        shorter=s2
    else:
        shorter=s1
    for i in range(len(shorter)):
        if s1[i]==s2[i]:
            commonSubstring+=s1[i]
        else:
            return commonSubstring
    return commonSubstring

def longestCommonSubstring(s1, s2):
    longestSubstring=""
    for i in range(len(s1)):
        for j in range(len(s2)):
            #cut the first letter in each string each time, and call the helper function
            substringInCommon=helperLongestSubstring(s1[i:],s2[j:]);
            if len(substringInCommon)>len(longestSubstring):
                longestSubstring=substringInCommon
            if len(substringInCommon)==len(longestSubstring):
                if(substringInCommon<longestSubstring):
                    longestSubstring=substringInCommon
            
    return longestSubstring

def bestStudentAndAvg(gradebook):
    highestAvg=-10**42
    for line in gradebook.splitlines():
        totalgrade=0
        counter=0
        avggrade=0
        #ignore lines starts with #'s
        if not line.startswith("#"):
            for items in line.split(","):
                #check the item if it is consist of digit or it is a negative number which starts with "-"
                if(items.isdigit() or items.startswith("-")):
                    totalgrade+=int(items)
                    counter+=1
            if(counter==0): avgrade=0;
            else: avggrade=int(totalgrade/counter)
            if avggrade>highestAvg:
                highestAvg=avggrade
                name=line[:line.find(",")]
    return name +":"+str(highestAvg)

def encodeColumnShuffleCipher(message, key):
    lenK=len(key)
    result=""
    #fill the empty space with "-"
    if(len(message)%lenK!=0):
        message+="-"*(lenK-len(message)%lenK)
    lenM=len(message)
    for n in key:
        for i in range(lenM):
            if(i%lenK==int(n)):
                result+=message[i]
    return key+result

#These two are bonus questions. 
def decodeColumnShuffleCipher(message):
    return 42

def mostFrequentLetters(s):
    return 42

#################################################
# hw3 Test Functions
################################################

def testLongestCommonSubstring():
    print("Testing longestCommonSubstring()...", end="")
    assert(longestCommonSubstring("abcdef", "abqrcdest") == "cde")
    assert(longestCommonSubstring("abcdef", "ghi") == "")
    assert(longestCommonSubstring("", "abqrcdest") == "")
    assert(longestCommonSubstring("abcdef", "") == "")
    assert(longestCommonSubstring("abcABC", "zzabZZAB") == "AB")
    print("Passed!")

def testBestStudentAndAvg():
    print("Testing bestStudentAndAvg()...", end="")
    gradebook = """
# ignore  blank lines and lines starting  with  #'s
wilma,91,93
fred,80,85,90,95,100
betty,88
"""
    assert(bestStudentAndAvg(gradebook) ==  "wilma:92")
    gradebook   =   """
#   ignore  blank   lines   and lines   starting    with    #'s
wilma,93,95

fred,80,85,90,95,100
betty,88
"""
    assert(bestStudentAndAvg(gradebook) ==  "wilma:94")
    gradebook = "fred,0"
    assert(bestStudentAndAvg(gradebook) ==  "fred:0")
    gradebook = "fred,-1\nwilma,-2"
    assert(bestStudentAndAvg(gradebook) ==  "fred:-1")
    gradebook = "fred,100"
    assert(bestStudentAndAvg(gradebook) ==  "fred:100")
    gradebook = "fred,100,110"
    assert(bestStudentAndAvg(gradebook) ==  "fred:105")
    gradebook = "fred,49\nwilma" + ",50"*50
    assert(bestStudentAndAvg(gradebook) ==  "wilma:50")
    print("Passed!")


def testEncodeColumnShuffleCipher():
    print("Testing encodeColumnShuffleCipher()...", end="")

    msg = "ILOVECMUSOMUCH"
    result = "021IVMOCOCSU-LEUMH"
    assert(encodeColumnShuffleCipher(msg, "021") == result)
    
    msg = "WEATTACKATDAWN"
    result = "0213WTAWACD-EATNTKA-"
    assert(encodeColumnShuffleCipher(msg, "0213") == result)
    
    msg = "SUDDENLYAWHITERABBITWITHPINKEYESRANCLOSEBYHER"
    result = "210DNAIRBWHNYRCSYRUEYHEBTTIESNOBESDLWTAIIPKEALEH"
    assert(encodeColumnShuffleCipher(msg,"210") == result)

    print("Passed!")
    
def testDecodeColumnShuffleCipher():
    print("Testing decodeColumnShuffleCipher()...", end="")
    msg = "0213WTAWACD-EATNTKA-"
    result = "WEATTACKATDAWN"
    assert(decodeColumnShuffleCipher(msg) == result)

    msg = "210DNAIRBWHNYRCSYR-UEYHEBTTIESNOBE-SDLWTAIIPKEALEH-"
    result = "SUDDENLYAWHITERABBITWITHPINKEYESRANCLOSEBYHER"
    assert(decodeColumnShuffleCipher(msg) == result)

    print("Passed!")

def testMostFrequentLetters():
    print("Testing mostFrequentLetters()...", end="")

    s = "We attack at Dawn"
    result = "atwcdekn"
    assert(mostFrequentLetters(s) == result)

    s = "Note that digits, punctuation, and whitespace are not letters!"
    result = "teanioscdhpruglw"
    assert(mostFrequentLetters(s) == result)

    s = ""
    result = ""
    assert(mostFrequentLetters(s) == result)

    print("Passed!")


#################################################
# hw3 Main
################################################

def testAll():
    testLongestCommonSubstring()
    testBestStudentAndAvg()
    testEncodeColumnShuffleCipher()

    #Comment these in if you want to test the bonus functions
    # testDecodeColumnShuffleCipher()
    # testMostFrequentLetters()


def main():
    testAll()

if __name__ == '__main__':
    main()
