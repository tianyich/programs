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
				self.skillCoolDownTemp=self.skillCoolDown
				self.counter=0
				self.attackOnCD=False
				self.attackCD=8
				self.attackCDTemp=self.attackCD

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
						self.attackCD=self.attackCDTemp
				if self.skillOnCoolDown==True:
						self.skillCoolDown-=0.1
				if self.skillCoolDown<=0:
						self.skillOnCoolDown==False
						self.skillCoolDown=self.skillCoolDownTemp

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
		def __init__(self,x,y,health,attack,speed,bulletSpeed):
				super().__init__(x,y,health,attack,speed)
				self.bullets=[]
				self.bulletSpeed=bulletSpeed
				self.radius=3

		def attacking(self):
				self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,self.direction,self.radius))
				self.attackOnCD=True


		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						bullet.move(data)
						if bullet.x>data.width-data.margin or bullet.x<data.margin or bullet.y>data.height-data.margin or bullet.y<data.margin:
								self.bullets.remove(bullet)


class Bullet(RangeEntity):
		def __init__(self,x,y,speed,direction,radius):
				self.x=x
				self.y=y
				self.speed=speed
				self.direction=direction
				self.radius=radius

		def hit(self,other):
				if abs(self.x-other.x)<self.radius+10 and abs(self.y-other.y)<self.radius+10:
						return True
				return False

		def move(self,data):
				super().move(data)

		def draw(self,canvas,color):
				canvas.create_oval(self.x-self.radius,self.y-self.radius,self.x+self.radius,self.y+self.radius,fill=color )



##Characters                                                                                                                           
class Warrior(MeleeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,30,7,10,40)
				self.isShield=False
				self.skillCoolDown=12
				self.image=PhotoImage(file="Warrior-L.png")
				self.attackEffect=PhotoImage(file="AttackEffect-L.png")
				self.Shield=PhotoImage(file="Shield.png")
				self.leftImage=PhotoImage(file="Warrior-L.png")
				self.rightImage=PhotoImage(file="Warrior-R.png")
				self.leftAttackEffect=PhotoImage(file="AttackEffect-L.png")
				self.rightAttackEffect=PhotoImage(file="AttackEffect-R.png")
				self.player1=True

		def getAttacked(self,other):
				if self.isShield ==True:
						self.isShield=False
						self.skillOnCoolDown=True
				else:
						super().getAttacked(other)

		def activateSkill(self):
				if self.skillOnCoolDown==False:
						self.isShield=True


		def attacking(self,data):
				if data.gameState=="Classic":
						for monster in data.monster:
								if self.attackOnCD==False:
										super().attacking(monster)
				if self.image==self.rightImage:
						self.attackEffect=self.rightAttackEffect
				else:
						self.attackEffect=self.leftAttackEffect

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				if self.isShield:
						canvas.create_image(self.x,self.y,anchor=NW,image=self.Shield)
				if self.attackOnCD==True:
						canvas.create_image(self.x,self.y,anchor=NW,image=self.attackEffect)

		def multiplayerTimerFiredAction(self,data):
				super().timerFiredAction(data)

#other Characters to be created 
class Mage(RangeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,20,7,5,8)
				self.attackCD=20
				self.skillCoolDown=15
				self.image=PhotoImage(file="Mage-L.png")
				self.leftImage=PhotoImage(file="Mage-L.png")
				self.rightImage=PhotoImage(file="Mage-R.png")
				self.radius=9
				self.player1=True
		def activateSkill(self):
				if self.skillOnCoolDown==False:
						directions=[(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)]
						for direction in directions:
								self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,direction,self.radius))
				self.skillOnCoolDown=True

		def draw(self,canvas):
					canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
					for bullet in self.bullets:
							bullet.draw(canvas,"light blue")

		def attacking(self,data):
				super().attacking()

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin+bullet.radius or bullet.y<=data.margin+bullet.radius or bullet.x>=data.width-data.margin-bullet.radius or bullet.y>=data.height-data.margin-bullet.radius:
								self.bullets.remove(bullet)
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)

		def multiplayerTimerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin+bullet.radius or bullet.y<=data.margin+bullet.radius or bullet.x>=data.width-data.margin-bullet.radius or bullet.y>=data.height-data.margin-bullet.radius:
								self.bullets.remove(bullet)
						if self.player1==True and bullet.hit(data.character2):
								data.character2.getAttacked(self)
						if self.player1==False and bullet.hit(data.character):
								data.character.getAttacked(self)

										

class Ninja(RangeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,20,5,5,10)
				self.attackCD=20
				self.skillCoolDown=15
				self.image=PhotoImage(file="Ninja-L.png")
				self.leftImage=PhotoImage(file="Ninja-L.png")
				self.rightImage=PhotoImage(file="Ninja-R.png")
				self.radius=5
				self.attackCounter=0
				self.zenMode=False
				self.skillEffect=PhotoImage(file="SkillEffect.png")
				self.player1=True

		def attacking(self,data):
				if data.gameState=="Classic":
						super().attacking()
						dx,dy=self.direction
						if dx==0:
								self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,(-1,dy),self.radius))
								self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,(1,dy),self.radius))
						if dy==0:
								self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,(dx,-1),self.radius))
								self.bullets.append(Bullet(self.x+10,self.y+10,self.bulletSpeed,(dx,1),self.radius))

		def activateSkill(self):
				if self.skillOnCoolDown==False:
						self.zenMode=True


		def getAttacked(self,other):
				if self.zenMode==False:
						super().getAttacked(other)

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin+bullet.radius or bullet.y<=data.margin+bullet.radius or bullet.x>=data.width-data.margin-bullet.radius or bullet.y>=data.height-data.margin-bullet.radius:
								self.bullets.remove(bullet)
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)
										self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						for monster in data.monster:
								monster.health-=0.05
						self.counter+=1
						if self.counter>=30:
								self.speed=10
								self.zenMode=False
								self.skillOnCoolDown=True

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin+bullet.radius or bullet.y<=data.margin+bullet.radius or bullet.x>=data.width-data.margin-bullet.radius or bullet.y>=data.height-data.margin-bullet.radius:
								self.bullets.remove(bullet)
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)
										self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						if self.player1==True:
								data.character2.health-=0.05
						self.counter+=1
						if self.counter>=30:
								self.speed=10
								self.zenMode=False
								self.skillOnCoolDown=True

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				for bullet in self.bullets:
						bullet.draw(canvas,"black")
				if self.zenMode==True:
						canvas.create_image(self.x,self.y,anchor=NW,image=self.skillEffect)

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
				if self.attackOnCD==False:
						self.move(data)
				if self.heroDistance<=self.attackRange:
						if self.attackOnCD==False:
							super().attacking(data.character)

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				canvas.create_rectangle(self.x-10,self.y-5,self.x+25,self.y,fill="red")
				healthLength=(self.maxHealth-self.health)/self.maxHealth*36
				canvas.create_rectangle(self.x+25-healthLength,self.y-4,self.x+23,self.y-2,fill="white")

class Necromancer(RangeEntity):
		def __init__(self,x,y,health,attack):
				super().__init__(x,y,health,attack,1,10)
				self.maxHealth=health
				self.image=PhotoImage(file="Necro.png")
				self.direction=random.choice([(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)])
				self.attackCD=30

		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				canvas.create_rectangle(self.x-20,self.y-20,self.x+20,self.y-14,fill="red")
				healthLength=(self.maxHealth-self.health)/self.maxHealth*36
				canvas.create_rectangle(self.x+18-healthLength,self.y-18,self.x+18,self.y-16,fill="white")
				for bullet in self.bullets:
							bullet.draw(canvas,"purple")

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				self.heroDistance=((data.character.x-self.x)**2+(data.character.y-self.y)**2)**0.5
				self.counter+=1
				if self.heroDistance<=200 and self.attackOnCD==False:
						self.direction=((data.character.x-self.x)/self.heroDistance,(data.character.y-self.y)/self.heroDistance)
						super().attacking()
				if self.attackOnCD==False:
						super().move(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin or bullet.y<=data.margin or bullet.x>=data.width-data.margin or bullet.y>=data.height-data.margin:
								self.bullets.remove(bullet)
						if bullet.hit(data.character):
								data.character.getAttacked(self)
								self.bullets.remove(bullet)
	
class Assassin(MeleeEntity):
		def __init__(self,x,y,health,attack):
				super().__init__(x,y,health,attack,10,20)
				self.maxHealth=health
				self.image=PhotoImage(file="Assassin.png")
				self.direction=random.choice([(-1,-1),(0,-1),(1,-1),
																			(-1,0),         (1,0),
																			(-1,1),(0,1),(1,1)])
				self.attackCD=3
				self.attackCDCounter=3
				self.attackOnCD=False
				self.shadowForm=False
				self.shadowFormCounter=0

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
				if self.attackOnCD==False:
						self.move(data)
				if self.heroDistance<=self.attackRange:
						if self.attackOnCD==False and self.shadowForm==False:
							super().attacking(data.character)
							self.shadowForm=True
				if self.shadowForm==True:
						self.speed=0
						self.shadowFormCounter+=1
						self.image=PhotoImage(file="Shadow.png")
						if self.shadowFormCounter==15:
								self.x=random.randint(data.margin,data.width-data.margin*2)
								self.y=random.randint(data.margin,data.height-data.margin*2)
						if self.shadowFormCounter==20:
								self.image=PhotoImage("Assassin.png")
								self.speed=10
								self.shadowFormCounter=0
								self.shadowForm=False
								self.image=PhotoImage(file="Assassin.png")


		def getAttacked(self,other):
				if self.shadowForm==False:
						super().getAttacked(other)
				self.shadowForm=True


		def draw(self,canvas):
				canvas.create_image(self.x,self.y,anchor=NW,image=self.image)
				canvas.create_rectangle(self.x-20,self.y-20,self.x+20,self.y-14,fill="red")
				healthLength=(self.maxHealth-self.health)/self.maxHealth*36
				canvas.create_rectangle(self.x+18-healthLength,self.y-18,self.x+18,self.y-16,fill="white")

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
		data.warriorImage=PhotoImage(file="Warrior-L.png")
		data.mageImage=PhotoImage(file="Mage-L.png")
		data.ninjaImage=PhotoImage(file="Ninja-L.png")

def init(data):
    data.gameState="Start Screen"
    data.level=1
    data.monster=[]
    data.margin=25
    data.startScreenButtons=[]
    data.characterSelectionButtons=[]
    createStartScreen(data)
    createCharacterSelection(data)
    importImages(data)
    data.character=Warrior(data.width/2,data.margin+10)
    data.character2=Warrior(data.width/2,data.margin+10)
    pressedStatus = {"Up": False, "Down": False, "Left": False, "Right": False,"2": False, "s": False, "a": False, "dt": False,"m": False, "n": False, "1": False, "2": False}

def createStartScreen(data):
		data.startScreenButtons.append(Button(0+data.margin,0+data.margin,80,50,"darkgrey",5,"grey","Shop"))
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,0+data.margin,200,50,"darkgrey",5,"grey","Character"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4,200,80,"darkgrey",5,"grey","Classic"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4*2,200,80,"darkgrey",5,"grey","Multiplayer"))
		data.startScreenButtons.append(Button(data.width/2-100,data.height/4*3,200,80,"darkgrey",5,"grey","Against AI"))

def createCharacterSelection(data):
			data.characterSelectionButtons.append(Button(data.width/2-300,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))
			data.characterSelectionButtons.append(Button(data.width/2-80,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))
			data.characterSelectionButtons.append(Button(data.width/2+120,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))

def mousePressed(event, data):
    startScreenMouse(event,data)
    characterSelectionMouse(event,data)

def startScreenMouse(event,data):
    if data.gameState=="Start Screen":
    	 for button in data.startScreenButtons:
    	 		if button.isClickedIn(event.x,event.y):
    	 				data.gameState=button.name
    	 				if button.name=="Classic":
    	 						createMonsters(data)


def characterSelectionMouse(event,data):
		if data.gameState=="Character":
				for button in data.characterSelectionButtons:
						if button.isClickedIn(event.x,event.y):
								if data.characterSelectionButtons.index(button)==0:
							 		data.character=Warrior(data.width/2,data.margin+10)
								if data.characterSelectionButtons.index(button)==1:
							 		data.character=Mage(data.width/2,data.margin+10)
								if data.characterSelectionButtons.index(button)==2:
							 		data.character=Ninja(data.width/2,data.margin+10)
								data.gameState="Start Screen"
		if data.gameState=="Multiplayer":
				for button in data.characterSelectionButtons:
						if button.isClickedIn(event.x,event.y):
								if data.characterSelectionButtons.index(button)==0:
							 		data.character2=Warrior(data.width/2,data.height-data.margin-50)
								if data.characterSelectionButtons.index(button)==1:
							 		data.character2=Mage(data.width/2,data.height-data.margin-50)
								if data.characterSelectionButtons.index(button)==2:
							 		data.character2=Ninja(data.width/2,data.height-data.margin-50)
								data.character2.player1=False
								data.gameState="MultiPlayerBattle"


    	 						
def createMonsters(data):
		for i in range(4+data.level):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Slime(x,y,10+2*data.level,5+data.level))
		for k in range(data.level):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Necromancer(x,y,3*data.level,8+data.level*2))
		for j in range(data.level):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Assassin(x,y,10*data.level,data.level*2))

def keyPressed(event,data):
		if event.keysym=="Escape":
				data.gameState="Start Screen" 
				if data.gameState=="Classic":
						if event.keysym=="Escape":
								data.monster=[]
		classicKeyControl(event,data)
		multiPlayerKeyControl(event,data)


def classicKeyControl(event,data):
		if data.gameState=="Classic" or data.gameState=="MultiPlayerBattle":
				if event.keysym=="Up":
		    				data.character.direction=(0,-1)
		    				data.character.move(data)
				if event.keysym=="Down":
		    				data.character.direction=(0,1)
		    				data.character.move(data)
				if event.keysym=="Left":
						data.character.direction=(-1,0)
						data.character.move(data)
						data.character.image=data.character.leftImage
				if event.keysym=="Right":
						data.character.direction=(1,0)
						data.character.move(data)
						data.character.image=data.character.rightImage
				if event.keysym=="m":
						if data.character.skillOnCoolDown==False:
								data.character.activateSkill()
				if event.keysym=="n":
						if data.character.attackOnCD==False:
								data.character.attacking(data)
								data.character.attackOnCD=True

def multiPlayerKeyControl(event,data):
		if data.gameState=="MultiPlayerBattle":
				if event.keysym=="w":
						data.character2.direction=(0,-1)
						data.character2.move(data)
				if event.keysym=="s":
						data.character2.direction=(0,1)
						data.character2.move(data)
				if event.keysym=="a":
						data.character2.direction=(-1,0)
						data.character2.move(data)
						data.character2.image=data.character2.leftImage
				if event.keysym=="d":
						data.character2.direction=(1,0)
						data.character2.move(data)
						data.character2.image=data.character2.rightImage
				if event.keysym=="1":
						if data.character2.skillOnCoolDown==False:
								data.character2.activateSkill()
				if event.keysym=="2":
						if data.character2.attackOnCD==False:
								data.character2.attacking(data)
								data.character2.attackOnCD=True

def timerFired(data):
		classicModeTimer(data)
		multiplayerTimer(data)

def classicModeTimer(data):
		if data.gameState=="Classic":
				data.character.timerFiredAction(data)
				for monster in data.monster:
						monster.timerFiredAction(data)
						if monster.health<=0:
								data.monster.remove(monster)
		 
def multiplayerTimer(data):
		if data.gameState=="MultiPlayerBattle":
				data.character.multiplayerTimerFiredAction(data)
				data.character2.multiplayerTimerFiredAction(data)
def redrawAll(canvas, data):

		canvas.create_image(0,0,anchor=NW,image=data.background)
		drawStartScreen(canvas,data)
		drawClassicGame(canvas,data)
		drawCharacterSelection(canvas,data)
		drawMulitPlayer(canvas,data)

def drawStartScreen(canvas,data):
		if data.gameState=="Start Screen":
			for button in data.startScreenButtons:
					button.draw(canvas)

def drawClassicGame(canvas,data):
		if data.gameState=="Classic":
				if data.character.health>0:
						canvas.create_text(50,30,text="Health: %d" %data.character.health, font="Arial 12 bold",fill="white")
						canvas.create_text(data.width/2,30,text="Level:%d" %data.level,font="Arial 12 bold",fill="white")
						canvas.create_text(data.width-100,30,text="Skill CoolDown:%d" %data.character.skillCoolDown,font="Arial 12 bold",fill="white")
						data.character.draw(canvas)
						for monster in data.monster:
								monster.draw(canvas)
				else:
						canvas.create_text(data.width/2,data.height/2,text="Game Over!!",font="Arial 25")
				if data.monster==[]:
						data.level+=1
						createMonsters(data)

def drawCharacterSelection(canvas,data):
		if data.gameState=="Character" or data.gameState=="Multiplayer" or data.gameState=="Against AI":
				canvas.create_rectangle(data.width/2-50,data.height/2-150,data.width/2+50,data.height/2-50,fill="white")
				canvas.create_rectangle(data.width/2-250,data.height/2-150,data.width/2-150,data.height/2-50,fill="white")
				canvas.create_rectangle(data.width/2+150,data.height/2-150,data.width/2+250,data.height/2-50,fill="white")
				canvas.create_image(data.width/2-16,data.height/2-100-16,anchor=NW,image=data.mageImage)
				canvas.create_image(data.width/2-200-16,data.height/2-100-16,anchor=NW,image=data.warriorImage)
				canvas.create_image(data.width/2+200-16,data.height/2-100-16,anchor=NW,image=data.ninjaImage)
				for button in data.characterSelectionButtons:
						button.draw(canvas)
		if data.gameState=="Multiplayer":
				canvas.create_text(data.width/2,data.height/2,text="Please Choose Player2 Character",font="Arial 12 bold",fill="white")
		if data.gameState=="Agaisnt AI":
			  canvas.create_text(data.width/2,data.height/2,text="Please Choose AI-controlled Character",font="Arial 12 bold",fill="white")

def drawMulitPlayer(canvas,data):
		if data.gameState=="MultiPlayerBattle":
				data.character.draw(canvas)
				data.character2.draw(canvas)
				canvas.create_text(60,20,text="Health: %d\nSkill CoolDown:%d" %(data.character.health,data.character.skillCoolDown), font="Arial 8 bold",fill="white")
				canvas.create_text(data.width-100,20,text="Health: %d\nSkill CoolDown:%d" %(data.character.health, data.character.skillCoolDown),font="Arial 8 bold",fill="white")

def pressed(event):
		pressedStatus[event.keysym]=True

def released(event):
		pressedStatus[event.keysym]=False

def binding():
		for char in ["Up", "Down", "Left", "Right","w","s","a","d","m","n","1","2"]:
				root.bind("<KeyPress-%s>" % char, pressed)
        root.bind("<KeyRelease-%s>" % char, released)


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

run(700, 600)

