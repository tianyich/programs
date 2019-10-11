# Basic Animation Framework

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.cellWidth=data.width/10
    data.cellHeight=data.height/10
    data.location=[0,0]

def mousePressed(event, data):
    row=event.x//data.cellWidth
    col=event.y//data.cellHeight
    data.location=[row,col]
    
def keyPressed(event, data):
    if event.keysym=="Up" and data.location[1]>0:
        data.location[1]-=1
    if event.keysym=="Down" and data.location[1]<9:
        data.location[1]+=1
    if event.keysym=="Left" and data.location[0]>0:
        data.location[0]-=1
    if event.keysym=="Right" and data.location[0]<9:
        data.location[0]+=1
        
def isGameOver(data):
    if data.location==[9,9]:
        return True
    else:
        return False
def timerFired(data):
    pass

def redrawAll(canvas, data):
    if not isGameOver(data):
        canvas.create_oval(data.location[0]*data.cellWidth,data.location[1]*data.cellHeight,
                        (data.location[0]+1)*data.cellWidth,(data.location[1]+1)*data.cellHeight,
                            fill="blue")
        for row in range(10):
            for col in range(10):
                canvas.create_rectangle(col*data.cellWidth,row*data.cellHeight,
                                        (col+1)*data.cellWidth,(row+1)*data.cellHeight)
    else:
        canvas.create_text(data.width/2,data.height/2,text="You Won!!")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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

run(600,600)