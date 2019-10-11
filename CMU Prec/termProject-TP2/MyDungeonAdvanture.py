################

################
from tkinter import *
import math
import random


#class that deal with all moving things in the game
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
				self.skillCounter=0

		def getAttacked(self,other):
				dx,dy=self.direction
				self.health-=other.attack

		def move(self,data):
				(dx,dy)=self.direction
				if data.margin+10<self.x+dx*self.speed<(data.width-data.margin-10) and data.margin+10<self.y+dy*self.speed<(data.height-data.margin-10):
						self.x+=dx*self.speed
						self.y+=dy*self.speed
				if self.x<data.margin+10:
						self.x=data.margin+10
				if self.y<data.margin+10:
						self.y=data.margin+10
				if self.x>data.width-data.margin-10:
						self.x=data.width-data.margin-10
				if self.y>data.height-data.margin-10:
						self.y=data.height-data.margin-10

		def timerFiredAction(self,data):
				if self.attackOnCD==True:
						self.attackCD-=1
				if self.attackCD<=0:
						self.attackOnCD=False
						self.attackCD=self.attackCDTemp
				if self.skillOnCoolDown==True:
						self.skillCounter+=1
						if self.skillCounter%10==0:
							self.skillCoolDown-=1
				if self.skillCoolDown<=0:
						self.skillOnCoolDown=False
						self.skillCounter=0
						self.skillCoolDown=self.skillCoolDownTemp

class MeleeEntity(Entity):
		def __init__(self,x,y,health,attack,speed,attackRange):
				super().__init__(x,y,health,attack,speed)
				self.isShield=False
				self.attackRange=attackRange

		#attack range is a semicirle in front of the character
		def successAttacked(self,other):
				dx,dy=self.direction
				if other.x-self.x*dx>=0 and other.y-self.y*dy>=0 and ((self.x-other.x)**2+(self.y-other.y)**2)**0.5<self.attackRange:
						other.x+=dx*20
						other.y+=dy*20
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
						if bullet.x>data.width-data.margin-self.radius-self.speed-10 or bullet.x<data.margin+self.radius+self.speed+10 or bullet.y>data.height-data.margin-self.radius-self.speed-10 or bullet.y<data.margin+self.radius+self.speed+10:
								self.bullets.remove(bullet)


class Bullet(RangeEntity):
		def __init__(self,x,y,speed,direction,radius):
				self.x=x
				self.y=y
				self.speed=speed
				self.direction=direction
				self.radius=radius

		def hit(self,other):
				if 0<self.x-other.x<self.radius+20 and 0<self.y-other.y<self.radius+20:
						dx,dy=self.direction
						other.x+=dx*20
						other.y+=dy*20
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
				self.skillCoolDownTemp=12
				self.image=PhotoImage(file="Warrior-L.png")
				self.attackEffect=PhotoImage(file="AttackEffect-L.png")
				self.Shield=PhotoImage(file="Shield.png")
				self.leftImage=PhotoImage(file="Warrior-L.png")
				self.rightImage=PhotoImage(file="Warrior-R.png")
				self.leftAttackEffect=PhotoImage(file="AttackEffect-L.png")
				self.rightAttackEffect=PhotoImage(file="AttackEffect-R.png")
				self.player1=True
				self.attackCD=8

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
							super().attacking(monster)
				if data.gameState=="MultiPlayerBattle":
						if self.player1==True:
							super().attacking(data.character2)
						else:
							super().attacking(data.character)
				if data.gameState=="AI Battle":
						super().attacking(data.AI)
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

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
		def multiplayerTimerFiredAction(self,data):
				super().timerFiredAction(data)

		def AItimerFiredAction(self,data):
				super().timerFiredAction(data)
#other Characters to be created 
class Mage(RangeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,20,7,5,8)
				self.attackCD=20
				self.skillCoolDown=15
				self.skillCoolDownTemp=15
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
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)
										self.bullets.remove(bullet)

		def AItimerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.hit(data.AI):
							data.AI.getAttacked(self)
							self.bullets.remove(bullet)

		def AIControlledTimer(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.hit(data.character):
							data.character.getAttacked(self)
							self.bullets.remove(bullet)

		def multiplayerTimerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if bullet.x<=data.margin+bullet.radius or bullet.y<=data.margin+bullet.radius or bullet.x>=data.width-data.margin-bullet.radius or bullet.y>=data.height-data.margin-bullet.radius:
								self.bullets.remove(bullet)
						if self.player1==True and bullet.hit(data.character2):
								data.character2.getAttacked(self)
								self.bullets.remove(bullet)
						if self.player1==False and bullet.hit(data.character):
								data.character.getAttacked(self)
								self.bullets.remove(bullet)

class Ninja(RangeEntity):
		def __init__(self,x,y):
				super().__init__(x,y,15,5,5,10)
				self.attackCD=20
				self.skillCoolDown=15
				self.skillCoolDownTemp=15
				self.image=PhotoImage(file="Ninja-L.png")
				self.leftImage=PhotoImage(file="Ninja-L.png")
				self.rightImage=PhotoImage(file="Ninja-R.png")
				self.radius=5
				self.attackCounter=0
				self.zenMode=False
				self.skillEffect=PhotoImage(file="SkillEffect.png")
				self.player1=True

		def attacking(self,data):
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
				if self.zenMode==True:
						super().getAttacked(other)
						super().getAttacked(other)
				else:
						super().getAttacked(other)

		def timerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						for monster in data.monster:
								if bullet.hit(monster):
										monster.getAttacked(self)
										self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						self.health+=0.5
						self.counter+=1
						if self.counter>=20:
								self.speed=10
								self.zenMode=False
								self.skillOnCoolDown=True

		def AItimerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
								if bullet.hit(data.AI):
										data.AI.getAttacked(self)
										self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						self.health+=0.5
						self.counter+=1
						if self.counter>=20:
								self.speed=10
								self.zenMode=False
								self.counter=0
								self.skillOnCoolDown=True

		def AIControlledTimer(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
								if bullet.hit(data.character):
										data.character.getAttacked(self)
										self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						self.health+=0.5
						self.counter+=1
						if self.counter>=20:
								self.speed=10
								self.zenMode=False
								self.counter=0
								self.skillOnCoolDown=True

		def multiplayerTimerFiredAction(self,data):
				super().timerFiredAction(data)
				for bullet in self.bullets:
						if self.player1==True and bullet.hit(data.character2):
								data.character2.getAttacked(self)
								self.bullets.remove(bullet)
						if self.player1==False and bullet.hit(data.character):
								data.character.getAttacked(self)	
								self.bullets.remove(bullet)
				if self.zenMode==True:
						self.speed=0
						self.health+=0.5
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
				self.attackCD=10
				self.attackCDTemp=10

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
				self.attackCD=50
				self.attackCDTemp=50

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

class AIWarrior(Warrior):
			def __init__(self,x,y):
					super().__init__(x,y)
					self.actionCounter=0
					self.dodgeCounter=0
			
			def timerFiredAction(self,data):
					super().timerFiredAction(data)
					self.move(data)
					self.actionCounter+=1
					if self.actionCounter%2==0:
							dx=self.x-data.character.x
							dy=self.y-data.character.y
							if dy>0 and abs(dy)>abs(dx):
								self.direction=(0,-1)
							if dy<0 and abs(dy)>abs(dx):
								self.direction=(0,1)
							if dx>0 and abs(dx)>abs(dy):
								self.direction=(-1,0)
							if dx<0 and abs(dx)<abs(dy):
								self.direction=(1,0)
							self.heroDistance=((data.character.x-self.x)**2+(data.character.y-self.y)**2)**0.5
							if self.heroDistance<=200 and self.attackOnCD==False:
									self.attacking(data.character)
							if self.skillOnCoolDown==False:
									self.activateSkill()
							if not isinstance(data.character,Warrior):
									self.dodge(data)


			def attacking(self,other):
				if self.successAttacked(other):
					other.getAttacked(self)
					self.attackOnCD=True

			def dodge(self,data):
					for bullet in data.character.bullets:
							dx,dy=bullet.direction
							if abs(bullet.x+dx*bullet.speed-self.x)<=20 and abs(bullet.y-self.y)<=bullet.radius:
									self.direction=random.choice([(0,1),(0,-1)])
									self.move(data)
									self.dodgeCounter+=1
							if abs(bullet.y+dy*bullet.speed-self.y)<=20 and abs(bullet.x-self.x)<=bullet.radius:
									self.direction=random.choice([(1,0),(-1,0)])
									self.move(data)
									self.dodgeCounter+=1

class AIMage(Mage):
			def __init__(self,x,y):
						super().__init__(x,y)
						self.actionCounter=0
						self.dodgeCounter=0

			def timerFiredAction(self,data):
					super().AIControlledTimer(data)
					self.move(data)
					self.actionCounter+=1
					self.heroDistance=((data.character.x-self.x)**2+(data.character.y-self.y)**2)**0.5
					if self.actionCounter%2==0:
						dx=self.x-data.character.x
						dy=self.y-data.character.y
						if self.heroDistance<=150:
								self.activateSkill()
						if abs(dx)<=10 and self.attackOnCD==False:
								if dy>0:
									self.direction=(0,-1)
								else:
									self.direction=(0,1)
								self.attacking(data)
						if abs(dy)<=10 and self.attackOnCD==False:
								if dx>0:
									self.direction=(-1,0)
								else:
									self.direction=(1,0)
								self.attacking(data)
						if dx>0 and abs(dy)>abs(dx):
								self.direction=(-1,0)
						if dx<0 and abs(dy)>abs(dx):
								self.direction=(1,0)
						if dy>0 and abs(dx)>abs(dy):
								self.direction=(0,-1)
						if dy<0 and abs(dx)<abs(dy):
								self.direction=(1,0)
						if not isinstance(data.character,Warrior):
									self.dodge(data)

			def dodge(self,data):
					for bullet in data.character.bullets:
							dx,dy=bullet.direction
							if abs(bullet.x+dx*bullet.speed-self.x)<=20 and abs(bullet.y-self.y)<=bullet.radius:
									self.direction=random.choice([(0,1),(0,-1)])
									self.move(data)
									self.dodgeCounter+=1
							if abs(bullet.y+dy*bullet.speed-self.y)<=20 and abs(bullet.x-self.x)<=bullet.radius:
									self.direction=random.choice([(1,0),(-1,0)])
									self.move(data)
									self.dodgeCounter+=1

class AINinja(Ninja):
			def __init__(self,x,y):
						super().__init__(x,y)
						self.actionCounter=0
						self.dodgeCounter=0

			def timerFiredAction(self,data):
					super().AIControlledTimer(data)
					self.move(data)
					self.actionCounter+=1
					self.heroDistance=((data.character.x-self.x)**2+(data.character.y-self.y)**2)**0.5
					if self.actionCounter%2==0:
						dx=self.x-data.character.x
						dy=self.y-data.character.y
						if self.heroDistance>=300:
								self.activateSkill()
						if abs(dx)<=10 and self.attackOnCD==False:
								if dy>0:
									self.direction=(0,-1)
								else:
									self.direction=(0,1)
								self.attacking(data)
						if abs(dy)<=10 and self.attackOnCD==False:
								if dx>0:
									self.direction=(-1,0)
								else:
									self.direction=(1,0)
								self.attacking(data)
						if dx>0 and abs(dy)>abs(dx):
								self.direction=(-1,0)
						if dx<0 and abs(dy)>abs(dx):
								self.direction=(1,0)
						if dy>0 and abs(dx)>abs(dy):
								self.direction=(0,-1)
						if dy<0 and abs(dx)>abs(dy):
								self.direction=(1,0)
						if not isinstance(data.character,Warrior):
								self.dodge(data)

			def dodge(self,data):
						for bullet in data.character.bullets:
								dx,dy=bullet.direction
								if abs(bullet.x+dx*bullet.speed-self.x)<=20 and abs(bullet.y-self.y)<=bullet.radius:
										self.direction=random.choice([(0,1),(0,-1)])
										self.move(data)
										self.dodgeCounter+=1
								if abs(bullet.y+dy*bullet.speed-self.y)<=20 and abs(bullet.x-self.x)<=bullet.radius:
										self.direction=random.choice([(1,0),(-1,0)])
										self.move(data)
										self.dodgeCounter+=1

									

####################################	
# customize these functions
####################################
def importImages(data):
		data.background=PhotoImage(file="background.png")
		data.warriorImage=PhotoImage(file="Warrior-L.png")
		data.mageImage=PhotoImage(file="Mage-L.png")
		data.ninjaImage=PhotoImage(file="Ninja-L.png")
		data.currentImage=data.warriorImage

def init(data):
    data.gameState="Start Screen"
    data.level=1
    data.monster=[]
    data.margin=30
    data.startScreenButtons=[]
    data.characterSelectionButtons=[]
    createStartScreen(data)
    createCharacterSelection(data)
    importImages(data)
    data.character=Warrior(data.width/2,data.margin+10)
    data.character2=Warrior(data.width/2,data.width-data.margin-10)
    data.AI=AIWarrior(data.width/2,data.width-data.margin-10)
    data.pressedKeys=set()
    

def createStartScreen(data):
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,0+data.margin,200,80,"darkgrey",5,"grey","Classic"))
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,data.height/4,200,80,"darkgrey",5,"grey","Character"))
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,data.height/4*2,200,80,"darkgrey",5,"grey","Multiplayer"))
		data.startScreenButtons.append(Button(data.width-data.margin-10-200,data.height/4*3,200,80,"darkgrey",5,"grey","Against AI"))

def createCharacterSelection(data):
			data.characterSelectionButtons.append(Button(data.width/2-300,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))
			data.characterSelectionButtons.append(Button(data.width/2-80,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))
			data.characterSelectionButtons.append(Button(data.width/2+120,data.height/2+150,150,80,"darkgrey",5,"grey","Select"))

def mousePressed(event, data):
    startScreenMouse(event,data)
    characterSelectionMouse(event,data)
    multiplayerSelectionMouse(event,data)
    AISelectionMouse(event,data)


def startScreenMouse(event,data):
    if data.gameState=="Start Screen":
    	 for button in data.startScreenButtons:
    	 		if button.isClickedIn(event.x,event.y):
    	 				data.gameState=button.name
    	 				if button.name=="Classic":
    	 						createMonsters(data)
    	 				if button.name=="Against AI":
    	 						event.x=0
    	 						event.y=0
    	 						#to avoid the button in the next screeen to be clicked at the same time


def characterSelectionMouse(event,data):
		if data.gameState=="Character":
				for button in data.characterSelectionButtons:
						if button.isClickedIn(event.x,event.y):
								if data.characterSelectionButtons.index(button)==0:
							 		data.character=Warrior(data.width/2,data.margin+10)
							 		data.currentImage=data.warriorImage
								if data.characterSelectionButtons.index(button)==1:
							 		data.character=Mage(data.width/2,data.margin+10)
							 		data.currentImage=data.mageImage
								if data.characterSelectionButtons.index(button)==2:
							 		data.character=Ninja(data.width/2,data.margin+10)
							 		data.currentImage=data.ninjaImage
								data.gameState="Start Screen"

def AISelectionMouse(event,data):
		if data.gameState=="Against AI":
				for button in data.characterSelectionButtons:
						if button.isClickedIn(event.x,event.y):
								if data.characterSelectionButtons.index(button)==0:
							 		data.AI=AIWarrior(data.width/2,data.height-data.margin-50)
								if data.characterSelectionButtons.index(button)==1:
							 		data.AI=AIMage(data.width/2,data.height-data.margin-50)
								if data.characterSelectionButtons.index(button)==2:
							 		data.AI=AINinja(data.width/2,data.height-data.margin-50)
								data.character2.player1=False
								data.gameState="AI Battle"

def multiplayerSelectionMouse(event,data):
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
		for i in range(2+data.level):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Slime(x,y,10+2*data.level,5+data.level))
		for k in range(data.level):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Necromancer(x,y,3*data.level,8+data.level*2))
		for j in range(data.level-1):
				x=random.randint(data.margin,data.width-data.margin*2)
				y=random.randint(data.margin,data.height-data.margin*2)
				data.monster.append(Assassin(x,y,10*data.level,data.level*2))

def keyPressed(data):
		if "Escape" in data.pressedKeys:
				data.gameState="Start Screen" 
				init(data)
		classicKeyControl(data)
		multiPlayerKeyControl(data)



def classicKeyControl(data):
		if data.gameState=="Classic" or data.gameState=="MultiPlayerBattle" or data.gameState=="AI Battle":
				if "Up" in data.pressedKeys:
		    				data.character.direction=(0,-1)
		    				data.character.move(data)
				if "Down" in data.pressedKeys:
		    				data.character.direction=(0,1)
		    				data.character.move(data)
				if "Left" in data.pressedKeys:
						data.character.direction=(-1,0)
						data.character.move(data)
						data.character.image=data.character.leftImage
				if "Right"in data.pressedKeys:
						data.character.direction=(1,0)
						data.character.move(data)
						data.character.image=data.character.rightImage
				if "m" in data.pressedKeys:
						if data.character.skillOnCoolDown==False:
								data.character.activateSkill()
				if "n" in data.pressedKeys:
						if data.character.attackOnCD==False:
								data.character.attacking(data)
								data.character.attackOnCD=True

def multiPlayerKeyControl(data):
		if data.gameState=="MultiPlayerBattle":
				if  "w" in data.pressedKeys:
						data.character2.direction=(0,-1)
						data.character2.move(data)
				if "s" in data.pressedKeys:
						data.character2.direction=(0,1)
						data.character2.move(data)
				if "a" in data.pressedKeys:
						data.character2.direction=(-1,0)
						data.character2.move(data)
						data.character2.image=data.character2.leftImage
				if "d" in data.pressedKeys:
						data.character2.direction=(1,0)
						data.character2.move(data)
						data.character2.image=data.character2.rightImage
				if "1" in data.pressedKeys:
						if data.character2.skillOnCoolDown==False:
								data.character2.activateSkill()
				if "2" in data.pressedKeys:
						if data.character2.attackOnCD==False:
								data.character2.attacking(data)
								data.character2.attackOnCD=True

def timerFired(data):
		classicModeTimer(data)
		multiplayerTimer(data)
		AITimer(data)

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

def AITimer(data):
		if data.gameState=="AI Battle":
			data.character.AItimerFiredAction(data)
			data.AI.timerFiredAction(data)

def redrawAll(canvas, data):
		canvas.create_image(0,0,anchor=NW,image=data.background)
		drawStartScreen(canvas,data)
		drawClassicGame(canvas,data)
		drawCharacterSelection(canvas,data)
		drawMulitPlayer(canvas,data)
		drawAgainstAI(canvas,data)
		keyPressed(data)

def drawStartScreen(canvas,data):
		if data.gameState=="Start Screen":
			for button in data.startScreenButtons:
					button.draw(canvas)
					canvas.create_text(data.margin+150,data.margin+100,text="     My\nDungeon\nAdventure",font="Arial 32 bold",fill="light grey")
					canvas.create_rectangle(data.margin+80,data.margin+250,data.margin+200,data.margin+370,fill="white")
					canvas.create_image(data.margin+140,data.margin+310,image=data.currentImage)

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
						canvas.create_text(data.width/2,data.height/2,text="Game Over!!",font="Arial 25 bold",fill="white")
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
		if data.gameState=="Character":
				canvas.create_text(data.width/2,data.height/2,text="Please Choose Your Character",font="Arial 12 bold",fill="white")
		if data.gameState=="Multiplayer":
				canvas.create_text(data.width/2,data.height/2,text="Please Choose Player2 Character",font="Arial 12 bold",fill="white")
		if data.gameState=="Against AI":
			  canvas.create_text(data.width/2,data.height/2,text="Please Choose AI-controlled Character",font="Arial 12 bold",fill="white")

def drawMulitPlayer(canvas,data):
		if data.gameState=="MultiPlayerBattle":
				if data.character.health<=0:
						canvas.create_text(data.width/2,data.height/2,text="Player2 Won the Game!!",font="Arial 25 bold",fill="light blue")
				elif data.character2.health<=0:
						canvas.create_text(data.width/2,data.height/2,text="Player1 Won the Game!!",font="Arial 25 bold",fill="Red")
				else:	
						data.character.draw(canvas)
						data.character2.draw(canvas)
						canvas.create_text(60,20,text="Health: %d\nSkill CoolDown:%d" %(data.character.health,data.character.skillCoolDown), font="Arial 8 bold",fill="white")
						canvas.create_text(data.width-100,20,text="Health: %d\nSkill CoolDown:%d" %(data.character2.health, data.character2.skillCoolDown),font="Arial 8 bold",fill="white")


def drawAgainstAI(canvas,data):
		if data.gameState=="AI Battle":
			if data.character.health<=0:
						canvas.create_text(data.width/2,data.height/2,text="You Lost",font="Arial 25 bold",fill="light blue")
			elif data.AI.health<=0:
						canvas.create_text(data.width/2,data.height/2,text="You Win!!!",font="Arial 25 bold",fill="Red")
			else:	
						data.character.draw(canvas)
						data.AI.draw(canvas)
						canvas.create_text(60,20,text="Health: %d\nSkill CoolDown:%d" %(data.character.health,data.character.skillCoolDown), font="Arial 8 bold",fill="white")
						canvas.create_text(data.width-100,20,text="Health: %d\nSkill CoolDown:%d" %(data.AI.health, data.AI.skillCoolDown),font="Arial 8 bold",fill="white")

def onKeyPress(event):
		data = event.widget.data
		data.pressedKeys.add(event.keysym)

def onKeyRelease(event):
		data = event.widget.data
		data.pressedKeys.remove(event.keysym)


###Cited and modified based on Class Note###                                                                                         
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
    root.data = data
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<KeyPress>", onKeyPress)
    root.bind("<KeyRelease>", onKeyRelease)
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 600)

