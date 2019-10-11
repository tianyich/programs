#################################################
# 15-112-n18 hw11
# Your Name:Eric Chen
# Your Andrew ID:tianyich
# Your Section:B
#################################################
def alternatingSum(lst):
    if lst==[]:
        return 0
    elif(len(lst)>1):
        result=lst[0]-lst[1]
        return result+alternatingSum(lst[2:])
    else:#situation when these's one element left
        return lst[0]


def binarySearchValues(L,v):
    if(L==[]):
        return []
    start=0
    end=len(L)
    return helperBinarySearch(L,start,end,v)
  
#helper function that takes the start index and end index of the lst
def helperBinarySearch(L,start,end,v):
    mid=(start+end)//2
    if (end-start)>=1:
        if v==L[mid]:
            return [(mid,L[mid])]
        elif v < L[mid]:
            #change the end index to mid to search left part
            return [(mid,L[mid])]+helperBinarySearch(L,start,mid,v)
        else:
            #change the start index to mid+1(since it's inclusive) to search right part
            return [(mid,L[mid])]+helperBinarySearch(L,mid+1,end,v)
    else:
        return []
        
def generateLetterString(s):
    if(len(s))!=2:
        return ""
    if (s[0]==s[1]):#base case
        return s[0]
    elif ord(s[0])<ord(s[1]):#forward
        newStr=chr(ord(s[0])+1)+s[1]
        return s[0]+generateLetterString(newStr)
    elif ord(s[0])>ord(s[1]):#backward
        newStr=chr(ord(s[0])-1)+s[1]
        return s[0]+generateLetterString(newStr)
    
#####Test Cases#####
assert(alternatingSum([1,2,3,4,5])==3)
assert(alternatingSum([1,-2,3,-4,5])==15)
assert(alternatingSum([])==0)
L = ['a', 'c', 'f', 'g', 'm', 'q']
assert(binarySearchValues(L, 'c') == [(3,'g'), (1,'c')])
assert(binarySearchValues(L, "b") == [(3, 'g'), (1, 'c'), (0, 'a')])
assert(binarySearchValues([],"a")==[])
assert(generateLetterString('ko')=='klmno')
assert(generateLetterString('me')=='mlkjihgfe')
assert(generateLetterString('aa')=='a')