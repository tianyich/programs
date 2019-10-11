import tkinter
import math

class Node(object):
    def __init__(self,x,y,value):
        self.x = x
        self.y = y    
        self.value = value
        self.radius = 30

    def drawNode(self,canvas):
        x = self.x
        y = self.y
        r = self.radius
        canvas.create_oval(x-r,y-r,x+r,y+r,fill="yellow")
        canvas.create_text(x,y,text=self.value,font="24")
    
    def swapRadius(self,other):
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        r = math.sqrt((x1-x2)**2+(y1-y2)**2)/2
        xc = (x1+x2)/2
        yc = (y1+y2)/2
        return (r,xc,yc)

class customButton(object):
        def __init__(self,x,y,width,height,color,margin,marginColor,name):
                self.x=x
                self.y=y
                self.width=width
                self.height=height
                self.color= color 
                self.margin=margin
                self.marginColor=marginColor
                self.name=name

        def isClickedIn(self,cx,cy):
                if self.x<cx<self.x+self.width and self.y<cy<self.y+self.height:
                        return True
                return False

        def draw(self,canvas):
                canvas.create_rectangle(self.x-self.margin,self.y-self.margin,
                                                                self.x+self.width+self.margin,self.y+self.height+self.margin,
                                                                fill=self.marginColor)
                canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill=self.color)
                canvas.create_text(self.x+self.width/2,self.y+self.height/2,text=self.name,font="Aria 25 bold")


def swapping(Node1,Node2,r,xc,yc):
    dtheta = 2*math.pi/10
    theta1 =  math.atan2(Node1.x-xc,Node1.y-yc)
    theta2 =  math.atan2(Node2.x-xc,Node2.y-yc)
    Node1.x = r*math.cos(theta1) +xc
    Node1.y = r*math.sin(theta1) +yc
    Node2.x = r*math.cos(theta2) +xc
    Node2.y = r*math.sin(theta2) +yc
    theta1 += dtheta
    theta2 += dtheta


def init(data):
    data.isPaused = True
    data.myHeap = BinaryHeap()
    data.nodeList = createNodes(data)
    data.moving = False
    data.buttons=[]
    data.buttons.append(customButton(30,30,35,30,"grey",5,"darkgrey","Insert"))

def createNodes(data):
    NodeList = [None] * (len(data.myHeap.heapArray))
    for i in range(1,len(data.myHeap.heapArray)):
        x,y = getCoordinate(data,i)
        NodeList[i] = Node(x,y,data.myHeap.heapArray[i])
    return NodeList
        
def drawLines(data,canvas):
    for i in range(1,len(data.nodeList)):
        x1 = data.nodeList[i].x
        y1 = data.nodeList[i].y
        if (i*2 < len(data.nodeList)):
                x2 = data.nodeList[2*i].x
                y2 = data.nodeList[2*i].y
                canvas.create_line(x1,y1,x2,y2)
        if (i*2+1 < len(data.nodeList)):
            x3 = data.nodeList[2*i+1].x
            y3 = data.nodeList[2*i+1].y
            canvas.create_line(x1,y1,x3,y3)

def drawButtons(data,canvas):
    for button in data.buttons:
        button.draw(canvas)
        
def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass


def timerFired(data):
    pass

def getCoordinate(data,i):
    heightMargin = data.height / (data.myHeap.maxDepth+2)
    depth = int(math.log(i)/math.log(2))
    sequence = i - 2**depth
    margin = data.width/(2**(depth+1))
    x = (sequence*2+1)*margin
    y = heightMargin*(depth+1)
    return (x,y)

def drawBinaryheap(canvas,data):
    for i in range (1,len(data.nodeList)):
        data.nodeList[i].drawNode(canvas)

def redrawAll(canvas, data):
    drawLines(data,canvas)
    drawBinaryheap(canvas,data)

def askForInsert(root):
    answer = simpledialog.askstring("Insert", "What is the value to insert", parent=root)
    if answer is not None:
        print(answer)

def askForRemove(root):
    answer = tkinter.messagebox.askokcancel("Caution","Are you sure to remove the max value?")


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(tkinter.ALL)
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
    root = tkinter.Tk()
    init(data)
    # create the root and the canvas
    canvas = tkinter.Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    insert = tkinter.Button(root, text = "Insert", command = askForInsert(root))
    insert.pack()
    remove = tkinter.Button(root, text = "Remove", command = askForRemove(root))
    remove.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")


run(800,800)
