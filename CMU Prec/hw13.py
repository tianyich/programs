#################################################
# 15-112-n18 hw13
# Your Name:
# Your Andrew ID:
# Your Section:

#################################################
import os

def findLargestFile(path):
    fileList=backtrack(path)
    if fileList==[]:
        return ""
    largestFile=fileList[0]
    for file in fileList:
        if(os.path.getsize(file)>os.path.getsize(largestFile)):
            largestFile=file
    print(largestFile)
    return largestFile

def backtrack(path):
    if os.path.isdir(path)==False:
        return [path]
    else:
        fileList=[]
        for file in os.listdir(path):
            fileList+=backtrack(os.path.join(path,file))
    return fileList
        
def friendsOfFriends(d):
    result=dict()
    for person in d:
        result[person]=set()
    for person in d:
        for friends in d[person]:
            for friendsOfFriends in d[friends]:
                if not (friendsOfFriends in d[person]) and friendsOfFriends!=person:
                    result[person].add(friendsOfFriends)
    return result
    
        

######################################################################
# ignore_rest: The autograder will ignore all code below here
######################################################################

#Don't forget to write test cases!
def testFindLargestFile():
    print("Testing findLargestFile()...", end="")
    assert(findLargestFile("sampleFiles"+os.sep+"folderA") ==
                       "sampleFiles"+os.sep+"folderA"+ \
                       os.sep+"folderC"+os.sep+"giftwrap.txt")
    assert(findLargestFile("sampleFiles"+os.sep+"folderB") ==
                       "sampleFiles"+os.sep+"folderB"+  \
                       os.sep+"folderH"+os.sep+"driving.txt")
    assert(findLargestFile("sampleFiles"+os.sep+"folderB"+ \
                       os.sep+"folderF") == "")
    #Write more test cases here!
    print("Passed!")

def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    d = { }
    d["spongebob"] = set(["sandy", "patrick", "mr.krabs", "squidward"])
    d["mr.krabs"] = set(["pearl", "spongebob", "squidward"])
    d["pearl"] = set(["mr.krabs"])
    d["sandy"] = set(["spongebob", "patrick"])
    d["patrick"] = set(["spongebob", "sandy"])
    d["squidward"] = set()
    assert(friendsOfFriends(d) == {
     'spongebob': {'pearl'}, 
     'mr.krabs': {'patrick', 'sandy'}, 
     'pearl': {'spongebob', 'squidward'}, 
     'sandy': {'mr.krabs', 'squidward'}, 
     'patrick': {'mr.krabs', 'squidward'}, 
     'squidward': set(), 
    }
    )
    #Write more test cases here!
    print("Passed!")


testFindLargestFile()
testFriendsOfFriends()

from tkinter import *
import math
import random
#########################################
# customize these functions for HFractal
#########################################

def init(data):
    data.level=0

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.keysym== "Up":
        data.level+=1
    if data.level!=0 and event.keysym=="Down":
        data.level-=1

def timerFired(data):
    pass

def drawHFractal(canvas,x,y,size,level):
    #x,y is the center of the H
    xl=x-size
    xr=x+size
    yt=y-size
    yb=y+size
    if level<=0:
        canvas.create_line(xl,yt,xl,yb)
        canvas.create_line(xl,y,xr,y)
        canvas.create_line(xr,yt,xr,yb)
    else:
        drawHFractal(canvas,xl,yt,size/2,level-1)
        drawHFractal(canvas,xr,yt,size/2,level-1)
        drawHFractal(canvas,xl,yb,size/2,level-1)
        drawHFractal(canvas,xr,yb,size/2,level-1)
        canvas.create_line(xl,yt,xl,yb)
        canvas.create_line(xl,y,xr,y)
        canvas.create_line(xr,yt,xr,yb)
def redrawAll(canvas, data):
    canvas.create_text(data.width//2,25,
                        text="Level %d HFractal" % (data.level),font="Arial 10")
    drawHFractal(canvas,data.width//2,data.height//2+50,50,data.level)
    

####################################
# use the run function as-is
####################################
def runHFractal(width=300, height=300):
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

runHFractal(300, 400)


##############################################
# customize these functions for dotsGalore 2.0
##############################################
def createDots(data):
    dir =[[-1,-1],[-1,0],[-1,1],
          [-1,0],        [1,0],
          [-1,1],[1,0],[1,1]]
    color=["red","green","blue","yellow"]
    d=random.randint(0,7)
    c=random.randint(0,3)
    size=random.randint(5,50)
    x=random.randint(0,data.width)
    y=random.randint(0,data.height)
    data.dots.append((x,y))
    data.dotsDir.append(dir[d])
    data.dotsColor.append(color[c])
    data.dotsSize.append(size)
    #create a dot with random location,size,color and moving direction
    
def drawDots(canvas,data):
#draw all the dots in the list
    for i in range(len(data.dots)):
        (x,y) =data.dots[i]
        size=data.dotsSize[i]
        color=data.dotsColor[i]
        canvas.create_oval(x-size,y-size,x+size,y+size,fill=color)
        
def moveDots(data):
#make the dots move by adding the direction to its current location
    for i in range(len(data.dots)):
        (x,y)=data.dots[i]
        (dx,dy)=data.dotsDir[i]
        size=data.dotsSize[i]
        data.dots[i]=(x+dx,y+dy)
        if (x+dx)<0-size:
            data.dots[i]=(data.width+size,y)
        if (x+dx)>(data.width+size):
            data.dots[i]=(0-size,y)
        if (y+dy)<0-size:
            data.dots[i]=(x,data.height+size)
        if (y+dy)>(data.height+size):
            data.dots[i]=(x,0-size)
            
def checkCollision(data):
#if two balls collides, they will move to the opposite direction
    for i in range(len(data.dots)):
        (x0,y0)=data.dots[i]
        (dx0,dy0)=data.dotsDir[i]
        size0=data.dotsSize[i]
        for j in range(len(data.dots)):
            if i!=j:#make sure it's not calculating distance with itself
                (x1,y1)=data.dots[j]
                (dx1,dy1)=data.dotsDir[j]
                size1=data.dotsSize[j]
                distance=((x0+dx0-x1-dx1)**2+(y0+dy0-y1-dy1)**2)**0.5
                if distance<=(size0+size1):
                    data.dotsDir[i]=(-dx0,-dy0)
                    data.dotsDir[j]=(-dx1,-dy1)


def reverseDir(data):
    for i in range(len(data.dots)):
        (dx,dy)=data.dotsDir[i]
        data.dotsDir[i]=(-dx,-dy)
        
def increaseSize(data):
    for i in range(len(data.dotsSize)):
        data.dotsSize[i]+=5
        
def init(data):
    # load data.xyz as appropriate
    data.dots=[]
    data.dotsDir=[]
    data.dotsSize=[]
    data.dotsColor=[]
    data.isPaused=False
    data.counter=0
    

def mousePressed(event, data):
    if not data.isPaused:
        for i in range(len(data.dots)-1,-1,-1):
        #go through the list inversely to make sure the ball at the top is the only one to be removed
            (x,y)=data.dots[i]
            size=data.dotsSize[i]
            distance=((x-event.x)**2+(y-event.y)**2)**0.5
            if distance<=size:
                data.dots.pop(i)
                data.dotsDir.pop(i)
                data.dotsColor.pop(i)
                data.dotsSize.pop(i)
                break
        

def keyPressed(event, data):
#Pause and Reverse function
    if event.keysym=="p" and data.isPaused==False:
        data.isPaused=True
    elif event.keysym=="p" and data.isPaused==True:
        data.isPaused=False
    if not data.isPaused and event.keysym=="r":
        reverseDir(data)

def timerFired(data):
    if not data.isPaused:
        data.counter+=1
        moveDots(data)
        checkCollision(data)
        #create a new dot every 2s
        if data.counter%20==0:
            createDots(data)
        #increase the size of dots by 5 every 10s
        if data.counter%100==0:
            increaseSize(data)
        
            
        
def redrawAll(canvas, data):
    drawDots(canvas,data)



####################################
# use the run function as-is
####################################

def runDotsGalore(width=300, height=300):
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

runDotsGalore(600, 600)