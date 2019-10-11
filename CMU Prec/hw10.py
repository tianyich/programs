#################################################
# 15-112-n18 hw9
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################
"""
def slow1(lst): # N is the length of the list lst
    assert(len(lst) >= 2)                           O(1)
    a = lst.pop()                                   O(1)
    b = lst.pop(0)                                  O(N)
    lst.insert(0, a)                                O(N)
    lst.append(b)                                   O(1)
    
    
The function swaps the first and the last element of the list
The bigO of the whole function is O(N)
Better:

def betterSlow1(lst):
    assert(len(lst)>=2)                O(1)
    a=lst.pop()                        O(1)
    b=lst[0]                           O(1)
    lst[0]=a                           O(1)
    lst.append(b)                      O(1)
The bigO of the whole function is O(1)


def slow2(lst): # N is the length of the list lst
    counter = 0                         O(1)
    for i in range(len(lst)):           O(n)
        if lst[i] not in lst[:i]:       O(N)
            counter += 1                O(1)
    return counter                      O(1)
    
This function returns the number of different elements in the list 
The bigO of the whole function is O(N**2)
Better

def betterSlow2(lst):
    s=set(lst)                          O(N)
    return len(s)                       O(1)

The bigO of the whole function is O(N)

import string
def slow3(s): # N is the length of the string s
    maxLetter = ""                                              O(1)
    maxCount = 0                                                O(1)
    for c in s:                                                 O(N)
        for letter in string.ascii_lowercase:                   O(1)
            if c == letter:                                     O(1)
                if s.count(c) > maxCount or                     O(N)
                   s.count(c) == maxCount and c < maxLetter:    O(N)
                    maxCount = s.count(c)                       O(N)
                    maxLetter = c                               O(1)
    return maxLetter                                            O(1)
This function returns the most frequent character in a string, if there's a 
tie, it will return the alphabetically smaller one
The bigO of the function is O(N**2)

Better:
import string
def betterSlow3(s):                             O(1)
    d=dict()                                    O(1)
    maxCount=0                                  O(1)
    maxLetter=None                              O(1)
    for letter in string.ascii_lowercase:       O(1)
        d[letter]=0                             O(1)
    for c in s:                                 O(N)
        d[c]+=1                                 O(1)
        if d[c]>maxCount:                       O(1)
            maxCount=d[c]                       O(1)
            maxLetter=c                         O(1)
    return maxLetter                            O(1)
The bigO of this function is O(N)
"""

def invertDictionary(d):
    invertedDict={}
    for k in d:
        invertedDict[d[k]]=set() #create a empty list for each value in d
    for k in d:
        invertedDict[d[k]].add(k) #add the key of the value to the list in the inverted dictionary
    return invertedDict

def largestSumOfPairs(a):
    if(len(a)<=1):
        return None
    largest=a[0]
    secondlargest=a[0]
    for i in range(len(a)):
        if a[i]>=largest:
            secondlargest=largest
            largest=a[i]
        elif a[i]>secondlargest:  #a[i]<largest
            secondlargest=a[i]
        else:
            continue
    return largest +secondlargest
        
######Test Cases######
assert(invertDictionary({1:2, 2:3, 3:4, 5:3}) ==
        {2:{1},3:{2,5},4:{3}})
assert(invertDictionary({1:0, 2:0, 3:0, 5:0}) ==
       {0:{1,2,3,5}})
assert(largestSumOfPairs([1,2,4,4,7])==11)
assert(largestSumOfPairs([-6,-1,-9,-9])==-7)
assert(largestSumOfPairs([])==None)
assert(largestSumOfPairs([12345678, 12345679, 12345680, 12345681, 12345682])==24691363)
       
