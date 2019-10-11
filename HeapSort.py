import tkinter as tk
import math
import random

teacherList = ["Dr. Andy","Mr. Bachner","Mr. Davidson","Dr. Dixon","Ms. Ekeberg",
                "Dr. Fay","Ms. Gropp","Mr. Hammer","Ms. Haselrig","Mr. Hodges","Ms. Holmes",
                "Dr. Horton","Ms. Kovacic","Mr. Lorenzi","Mr. Maione","Mr. Marcus","Ms. Martin",
                "Mr. Marx", "Ms. McDermott","Mr. Miller","Dr.Naragon","Mr.Nassar","Ms. Nesbitt",
                "Ms. Presnar","Rui Laoshi", "Dr. Seward","Ms.Sickler", "Ms. Skiba"]
class Teacher(object):
        def __init__(self,name):
                self.name = name
                self.teacherList = ["Dr. Andy","Mr. Bachner","Mr. Davidson","Dr. Dixon","Ms. Ekeberg",
                "Dr. Fay","Ms. Gropp","Mr. Hammer","Ms. Haselrig","Mr. Hodges","Ms. Holmes",
                "Dr. Horton","Ms. Kovacic","Mr. Lorenzi","Mr. Maione","Mr. Marcus","Ms. Martin",
                "Mr. Marx", "Ms. McDermott","Mr. Miller","Dr.Naragon","Mr.Nassar","Ms. Nesbitt",
                "Ms. Presnar","Rui Laoshi", "Dr. Seward","Ms.Sickler", "Ms. Skiba"]

        def __eq__(self,other):
                return self.name == other.name

        def __str__(self):
                return self.name
        
        def __lt__(self,other):
                return self.teacherList.index(self.name)>self.teacherList.index(other.name)

        def __gt__(self,other):
                return self.teacherList.index(self.name)<self.teacherList.index(other.name)
class Node(object):
        def __init__(self,x=0,y=0,value=""):
                self.x = x
                self.y = y    
                self.value = value
                self.radius =50
                self.targetpos = []
                self.speed = 8

        def drawNode(self,canvas):
                x = self.x
                y = self.y
                r = self.radius
                canvas.create_oval(x-r,y-r,x+r,y+r,fill="yellow")
                canvas.create_text(x,y,text=self.value,font="12")
    
        def move(self):
                if len(self.targetpos) == 0:
                        return 
                theta = math.atan2(self.targetpos[1]-self.y,self.targetpos[0]-self.x)
                self.x += self.speed*math.cos(theta)
                self.y += self.speed*math.sin(theta)
                return False
        
        def stopMove(self):
                if len(self.targetpos) == 0:
                        return 
                if abs(self.y-self.targetpos[1])<9 and abs(self.x-self.targetpos[0])<9:
                        return True
                return False

heapArray = [Teacher("")]
def createNodes(data):
        NodeList = [None] * (len(heapArray))
        for i in range(1,len(heapArray)):
                x,y = getCoordinate(data,i)
                NodeList[i] = Node(x,y,heapArray[i])
        data.nodeList = NodeList

def getCoordinate(data,i):
        maxDepth = int(math.log(len(heapArray))/math.log(2))
        heightMargin = data.height / (maxDepth+2)
        depth = int(math.log(i)/math.log(2))
        sequence = i - 2**depth
        margin = data.width/(2**(depth+1))
        x = (sequence*2+1)*margin
        y = heightMargin*(depth+1)
        return (x,y)
          
def init(data):
        createNodes(data)
        data.buttons=[]
        b1 = tk.Button(data.root, text="Insert", command=lambda:onButton(data,1))
        b1.pack()
        b2 = tk.Button(data.root, text="Remove", command=lambda:onButton(data,2))
        b2.pack()
        data.state = ""
        data.pos = []

def resetTarget(data):
        for i in range(1,len(data.nodeList)):
                if data.nodeList[i] is None:
                        continue
                setTarget(data,i)

def setTarget(data,i):
        if data.nodeList[i] is None:
                return 
        if data.state == "sink":
                if 2*i+1 < len(data.nodeList) and data.nodeList[2*i+1].value > data.nodeList[i].value and data.nodeList[2*i].value < data.nodeList[2*i+1].value:
                        data.nodeList[i].targetpos = [data.nodeList[i*2+1].x,data.nodeList[i*2+1].y]
                        data.nodeList[i*2+1].targetpos = [data.nodeList[i].x,data.nodeList[i].y]
                elif 2*i < len(data.nodeList) and data.nodeList[2*i].value > data.nodeList[i].value:
                        data.nodeList[i].targetpos = [data.nodeList[i*2].x,data.nodeList[i*2].y]
                        data.nodeList[i*2].targetpos = [data.nodeList[i].x,data.nodeList[i].y]
        if data.state == "swim":
                if i > 1 and data.nodeList[i//2] is not None and data.nodeList[i//2].value < data.nodeList[i].value :
                        data.nodeList[i].targetpos = [data.nodeList[i//2].x,data.nodeList[i//2].y]
                        data.nodeList[i//2].targetpos =[data.nodeList[i].x,data.nodeList[i].y]

def onButton(data,buttonId):
        if buttonId == 1:
                name = random.choice(teacherList)
                heapArray.append(Teacher(name))
                teacherList.remove(name)
                createNodes(data)
                data.state = "swim"
                resetTarget(data)

        if buttonId == 2:
                x = data.nodeList[1].x
                y = data.nodeList[1].y
                data.nodeList[1] = None
                heapArray[1] = None
                resetTarget(data)
                data.nodeList[len(data.nodeList)-1].targetpos = [x,y]
                data.state = "top"
                
                
                
                

def keyPressed(event, data):
        pass

def timerFired(data):
        pass

def mousePressed(event,data):
        pass

def drawBinaryheap(canvas,data):
        for i in range (1,len(data.nodeList)):
                if data.nodeList[i] is not None:
                        data.nodeList[i].drawNode(canvas)

def drawLines(canvas,data):
        for i in range(1,len(data.nodeList)):
                (x1,y1) = getCoordinate(data,i)
                if i*2 < len(data.nodeList):
                        (x2,y2)=getCoordinate(data,i*2)
                        canvas.create_line(x1,y1,x2,y2)
                if i*2+1 < len(data.nodeList):
                        (x3,y3)=getCoordinate(data,i*2+1)
                        canvas.create_line(x1,y1,x3,y3)


def redrawAll(canvas, data):
        drawLines(canvas,data)
        drawBinaryheap(canvas,data)
        for i in range(1,len(data.nodeList)):
                if data.nodeList[i] is None:
                        continue
                data.nodeList[i].move()
        for i in range(len(data.nodeList)-1,1,-1):
                if data.nodeList[i] is None:
                        continue
                if data.nodeList[i].stopMove():
                        if  data.state == "swim" :
                                tempNode = data.nodeList[i//2]
                                data.nodeList[i//2] = data.nodeList[i]
                                data.nodeList[i] = tempNode
                                temp = heapArray[i//2]
                                heapArray[i//2] = heapArray[i]
                                heapArray[i] = temp
                                createNodes(data)
                                resetTarget(data)
                                return 
                        if  data.state == "top":
                                data.nodeList[1] = data.nodeList[i]
                                data.nodeList.pop(i)
                                heapArray[1] = heapArray[i]
                                heapArray.pop(i)
                                createNodes(data)
                                data.state = "sink"
                                resetTarget(data)
                                return
                       
        if  data.state == "sink":
                for i in range(1,len(data.nodeList)):
                        if data.nodeList[i].stopMove():
                                if 2*i+1 < len(data.nodeList) and data.nodeList[2*i+1].value > data.nodeList[i].value and data.nodeList[2*i].value < data.nodeList[2*i+1].value:
                                        tempNode = data.nodeList[2*i+1]
                                        data.nodeList[2*i+1] = data.nodeList[i]
                                        data.nodeList[i] = tempNode
                                        temp = heapArray[2*i+1]
                                        heapArray[2*i+1] = heapArray[i]
                                        heapArray[i] = temp
                                        createNodes(data)
                                        resetTarget(data)
                                        return

                                elif 2*i < len(data.nodeList) and data.nodeList[2*i].value > data.nodeList[i].value:
                                        tempNode = data.nodeList[2*i]
                                        data.nodeList[2*i] = data.nodeList[i]
                                        data.nodeList[i] = tempNode
                                        temp = heapArray[2*i]
                                        heapArray[2*i] = heapArray[i]
                                        heapArray[i] = temp
                                        createNodes(data)
                                        resetTarget(data)
                                        return
        

                        
                


def run(width=300, height=300):
        def redrawAllWrapper(canvas, data):
                canvas.delete(tk.ALL)
                canvas.create_rectangle(0, 0, data.width, data.height,fill='white', width=0)
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
                canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 100 
        root = tk.Tk()
        data.root = root
        init(data)
        canvas = tk.Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)
        root.mainloop() 
        print("bye!")

run(800, 600)