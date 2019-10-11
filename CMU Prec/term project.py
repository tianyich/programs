################
""" 
This is an adventure game which has 3 different modes- Classic, Multi player and against AI. In Classic mode you can play as your favorite character to fight against monsters when all monster's are killed, you will go to the next level. You can earn money in this mode to unlock more'
characters or upgrade your current one. In Multi player you can play against your friend who can control a different character from yours. In against AI mode, you can play against an AI which is very skillful at this game.
"""
################
from tkinter import *
import math
import random

class Entity (object):
		def __init__(self,x,y,health,attack,speed):
				self.x=x
				self.y=y
				self.health = health
				self.attack= attack
				self.speed=speed
				self.direction=(0,1)
				self.skillOnCoolDown=False
				self.skillCoolDown=5
				self.counter=0
				self.attackOnCD=False
				self.attackCD=8

		def getAttacked(self,other):
				dx,dy=self.direction
				self.health-=other.attack
				self.x-=dx*40
				self.y-=dy*40

		def move(self,data):
				(dx,dy)=self.direction
				if data.margin<self.x+dx*self.speed<(data.width-data.margin) and data.margin<self.y+dy*self.speed<(data.height-data.margin):
						self.x+=dx*self.speed
						self.y+=dy*self.speed
				if self.x<data.margin:
						self.x=data.margin
				if self.y<data.margin:
						self.y=data.margin
				if self.x>data.width-data.margin:
						self.x=data.width-data.margin
				if self.y>data.height-data.margin:
						self.y=data.height-data.margin

		def timerFiredAction(self,data):
				if self.attackOnCD==True:
						self.attackCD-=1
				if self.attackCD<=0:
						self.attackOnCD=False
						self.attackCD=8
				if self.skillOnCoolDown==True:
						self.counter+=1
				if self.counter%(self.skillCoolDown*10)==0:
						self.skillOnCoolDown==False

class MeleeEntity(Entity):
		def __init__(self,x,y,health,attack,speed,attackRange):
				super().__init__(x,y,health,attack,speed)
				self.isShield=False
				self.attackRange=attackRange

		def successAttacked(self,other):
				dx,dy=self.direction
				if other.x-self.x*dx>=0 and other.y-self.y*dy>=0 and ((self.x-other.x)**2+(self.y-other.y)**2)**0.5<self.attackRange:
						return True
				return False 

		def attacking(self,other):
				if self.successAttacked(other):
					other.getAttacked(self)
					self.attackOnCD=True


class RangeEntity(Entity):
		def __init__(self,x,y,health,attack,speed):
				super().__init__(self,x,y,health,attack,speed,bulletSpeed)
				self.bullets=[]
				self.bulletSpeed=bulletSpeed

		def attack(self,speed):
				self.bullets.append(Bullet(self.x,self.y,self.bulletSpeed,direction))

		def timerFiredAction(self,data):
				super().timerFiredAction
				for bullet in self.bullets:
						bullet.move()
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)
						if bullet.x>data.width or bullet.x<0 or bullet.y>data.height or bullet.y<0:
								self.bullets.remove(bullet)


class Bullet(RangeEntity):
		def __init__(self,x,y,speed,direction):
				self.x=x
				self.y=y
				self.speed=speed
				self.direction=direction

		def hit(self,other):
				if math.abs(self.x-other.x)<5 and math.abs(self.y-other.y)<5:
						return True
				return False

		def move(self):
				super().move()


##Characters                                                                                                                           
class Warrior(MeleeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,30,7,10,40)
				self.isShield=False
				self.skillCoolDown=12
				self.image=PhotoImage(file="Warrior-L.png")
				self.attackEffect=PhotoImage(file="AttackEffect-L.png")
				self.Shield=PhotoImage(file="Shield.png")

		def getAttacked(self,other):
				if self.isShield ==True:
						self.isShield=False
				else:
						super().getAttacked(other)

		def activateSkill(self):
				if self.skillOnCoolDown==False:
						self.isShield=True
						self.skillOnCoolDown==True

		def attacking(self,data):
				for monster in data.monster:
						if self.attackOnCD==False:
								super().attacking(monster)

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				if self.isShield:
						canvas.create_image(self.x,self.y,anchor=NW,image=self.Shield)
				if self.attackOnCD==True:
						canvas.create_image(self.x,self.y,anchor=NW,image=self.attackEffect)

#other Characters to be created 
class Mage(RangeEntity):
		pass
class Archor(RangeEntity):
		pass
#Monsters
class Slime(MeleeEntity):
		def __init__(self,x,y,health,attack):
				super().__init__(x,y,health,attack,2,20)
				self.maxHealth=health
				self.image=PhotoImage(file="Slime.png")
				self.direction=random.choice([(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)])

		def move(self,data):
				self.heroDistance=((data.character.x-self.x)**2+(data.character.y-self.y)**2)**0.5
				if self.heroDistance<=100:
						self.direction=((data.character.x-self.x)/self.heroDistance,(data.character.y-self.y)/self.heroDistance)
						super().move(data)	
				else:
						super().move(data)
		
		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				self.counter+=1
				if self.counter%30==0:
						self.direction=random.choice([(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)])
				self.move(data)
				if self.heroDistance<=self.attackRange:
						if self.attackOnCD==False:
							super().attacking(data.character)

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				canvas.create_rectangle(self.x-20,self.y-20,self.x+20,self.y-14,fill="red")
				healthLength=(self.maxHealth-self.health)/self.maxHealth*36
				canvas.create_rectangle(self.x+18-healthLength,self.y-18,self.x+18,self.y-16,fill="white")


class Necromancer(RangeEntity):
		def __init__(self,x,y,health,attack):
				super().__init__(x,y,health,attack,1)
				self.maxHealth=health
				self.image=PhotoImage(file="Necro.png")
				self.direction=random.choice([(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)])

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				canvas.create_rectangle(self.x-20,self.y-20,self.x+20,self.y-14,fill="red")
				healthLength=(self.maxHealth-self.health)/self.maxHealth*36
				canvas.create_rectangle(self.x+18-healthLength,self.y-18,self.x+18,self.y-16,fill="white")

class Assassin(MeleeEntity):
		pass
class Button(object):
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

####################################	
# customize these functions
####################################
def importImages(data):
		data.background=PhotoImage(file="background.png")

def init(data):
    data.gameState="Start Screen"
    data.level=1
    data.monster=[]
    data.margin=25
    data.startScreenButtons=[]
    createStartScreen(data)
    importImages(data)
    data.character=Warrior(data.width/2,data.margin)

def createStartScreen(data):
		data.startScreenButtons.append(Button(0+data.margin,0+data.margin,80,50,"darkgrey",5,"grey","Shop"))
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,0+data.margin,200,50,"darkgrey",5,"grey","Character"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4,200,80,"darkgrey",5,"grey","Classic"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4*2,200,80,"darkgrey",5,"grey","Multiplayer"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4*3,200,80,"darkgrey",5,"grey","Against AI"))


def mousePressed(event, data):
    if data.gameState=="Start Screen":
    	 for button in data.startScreenButtons:
    	 		if button.isClickedIn(event.x,event.y):
    	 				data.gameState=button.name
    	 				createMonsters(data)
    	 						
def createMonsters(data):
		for i in range(8+data.level*2):
				x=random.randint(data.margin,data.width-data.margin)
				y=random.randint(data.margin,data.height-data.margin)
				data.monster.append(Slime(x,y,10+2*data.level,5+data.level))


def keyPressed(event,data,canvas):
    if data.gameState=="Classic":
    		classicKeyControl(event,data,canvas)


def classicKeyControl(event,data,canvas):
    if event.keysym=="Up":
    				data.character.direction=(0,-1)
    				data.character.move(data)
    if event.keysym=="Down":
    				data.character.direction=(0,1)
    				data.character.move(data)
    if event.keysym=="Left":
    				data.character.direction=(-1,0)
    				data.character.move(data)
    				data.character.image=PhotoImage(file="Warrior-L.png")
    				data.character.attackEffect=PhotoImage(file="AttackEffect-L.png")
    if event.keysym=="Right":
    				data.character.direction=(1,0)
    				data.character.move(data)
    				data.character.image=PhotoImage(file="Warrior-R.png")
    				data.character.attackEffect=PhotoImage(file="AttackEffect-R.png")
    if event.keysym=="m":
    				if not data.character.skillOnCoolDown:
    						data.character.activateSkill()
    if event.keysym=="a":
    				data.character.attacking(data)

def timerFired(data):
		if data.gameState=="Classic":
				data.character.timerFiredAction(data)
				for monster in data.monster:
						monster.timerFiredAction(data)
						if monster.health<=0:
								data.monster.remove(monster)
		 
def drawStartScreen(canvas,data):
		for button in data.startScreenButtons:
				button.draw(canvas)

def redrawAll(canvas, data):
		canvas.create_image(0,0,anchor=NW,image=data.background)
		if data.gameState=="Start Screen":
				drawStartScreen(canvas,data)
		if data.gameState=="Classic":
				if data.character.health>0:
						canvas.create_text(50,30,text="Health: %d" %data.character.health, font="Arial 12 bold")
						canvas.create_text(data.width/2,30,text="Level:%d" %data.level,font="Arial 12 bold")
						data.character.draw(canvas)
						for monster in data.monster:
								monster.draw(canvas)
				else:
						canvas.create_text(data.width/2,data.height/2,text="Game Over!!",font="Arial 25")
				if data.monster==[]:
						data.level+=1
						createMonsters()

				
###Cited From Class Note###                                                                                         
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
        keyPressed(event, data,canvas)
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

run(700, 600)
