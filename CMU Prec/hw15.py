#################################################################
# 15-112-n18 hw15
# Your Name: Eric Chen
# Your Andrew ID: tianyich
# Your Section: Bullet

#################################################################

class Asteroid(object):
		def __init__(self,cx,cy,radius,speed,direction):
				self.cx=cx
				self.cy=cy
				self.radius=radius
				self.speed=speed
				self.direction=direction

		def setDirection(self,dr):
				dx=dr[0]
				dy=dr[1]
				self.direction=(dx,dy)

		def getDirection(self):
				return self.direction

		def __repr__(self):
				dx,dy=self.getDirection()
				return "%s at (%d, %d) with radius=%d and direction (%d, %d)"%(self.__class__.__name__,self.cx,self.cy,self.radius,dx,dy)

		def isCollisionWithWall(self,width,height):
				x=self.cx
				y=self.cy
				r=self.radius
				if x+r>=width or x-r<=0 or y+r>=height or y-r<=0:
						return True
				return False

		def moveAsteroid(self):
				(dx,dy)=self.getDirection()
				self.cx+=dx*self.speed
				self.cy+=dy*self.speed

		def getPositionAndRadius(self):
				return (self.cx,self.cy,self.radius)

		def reactToBulletHit(self,data):
				self.setDirection((0,0))

		def draw(self,canvas,color="purple"):
				x=self.cx
				y=self.cy
				r=self.radius
				canvas.create_oval(x-r,y-r,x+r,y+r,fill=color)

		def move(self):
				dx,dy=self.getDirection()
				self.cx += dx*self.speed
				self.cy += dy*self.speed

		def onTimerFired(self,data):
				self.move()
				self.collisonWithWall(data)

		def collisonWithWall(self,data):
				if self.isCollisionWithWall(data.height,data.width):
						self.cx=self.cx%data.width
						self.cy=self.cy%data.height

class ShrinkingAsteroid(Asteroid):
		def __init__(self,cx,cy,radius,speed,direction=(0,1),shrinkAmount=5):
				super().__init__(cx,cy,radius,speed,direction)
				self.shrinkAmount=shrinkAmount

		def reactToBulletHit(self,data):
				self.radius-=self.shrinkAmount

		def bounce(self):
				(dx,dy) =self.getDirection()
				self.setDirection((dx*-1,dy*-1))

		def draw(self,canvas):
				super().draw(canvas,"pink")

		def onTimerFired(self,data):
				super().move()
				if self.isCollisionWithWall(data.width,data.height):
						self.bounce()

class SplittingAsteroid(Asteroid):
		def __init__(self,cx,cy,radius,speed,direction=(0,1)):
				super().__init__(cx,cy,radius,speed,direction)

		def reactToBulletHit(self,data):
				x= self.cx
				y= self.cy
				r= self.radius
				cx0=x-r
				cy0=y-r
				cx1=x+r
				cy1=y+r
				newR=self.radius/2
				newAsteroid0=SplittingAsteroid(cx0,cy0,newR,self.speed,self.direction)
				newAsteroid1=SplittingAsteroid(cx1,cy1,newR,self.speed,self.direction)
				data.asteroids.append(newAsteroid0)
				data.asteroids.append(newAsteroid1)
				data.asteroids.remove(self)

		def draw(self,canvas):
				super().draw(canvas,"blue")


#################################################################

# Starter Code begins here. Read and understand it!

import random, math

# Helper function for drawing the Rocket
def drawTriangle(canvas, cx, cy, angle, size, fill="black"):
    angleChange = 2*math.pi/3
    p1x, p1y = (cx + size*math.cos(angle), 
                    cy - size*math.sin(angle))
    p2x, p2y = (cx + size*math.cos(angle + angleChange), 
                    cy - size*math.sin(angle + angleChange))
    p3x, p3y = (cx, cy)
    p4x, p4y = (cx + size*math.cos(angle + 2*angleChange),
                    cy - size*math.sin(angle + 2*angleChange))
    
    canvas.create_polygon((p1x, p1y), (p2x, p2y), (p3x, p3y), (p4x, p4y),
                                                                 fill=fill)

# Read this class carefully! You'll need to call the methods!
class Rocket(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.angle = 90

    def rotate(self, numDegrees):
        self.angle += numDegrees

    def makeBullet(self):
        offset = 10
        dx, dy = (offset*math.cos(math.radians(self.angle)), 
                            offset*math.sin(math.radians(self.angle)))
        speedLow, speedHigh = 20, 40

        return Bullet(self.cx+dx, self.cy-dy,
                self.angle,random.randint(speedLow, speedHigh))

    def draw(self, canvas):
        size = 30
        drawTriangle(canvas, self.cx, self.cy, 
            math.radians(self.angle), size, fill="green2")

# Read this class carefully! You'll need to call the methods!
class Bullet(object):
    def __init__(self, cx, cy, angle, speed=20):
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed

    def moveBullet(self):
        dx = math.cos(math.radians(self.angle))*self.speed
        dy = math.sin(math.radians(self.angle))*self.speed
        self.cx, self.cy = self.cx + dx, self.cy - dy

    def isCollisionWithAsteroid(self, other):
        # in this case, other must be an asteroid
        if(not isinstance(other, Asteroid)):
            return False
        else:
            return (math.sqrt((other.cx - self.cx)**2 + 
                                (other.cy - self.cy)**2)
                                        < self.r + other.radius) 
    def draw(self, canvas):
        cx, cy, r = self.cx, self.cy, self.r
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
            fill="white", outline=None)

    def onTimerFired(self, data):
        self.moveBullet()

#################################################################

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.rocket = Rocket(data.width//2, data.height//2)
    # what else do you need to store here? 
    data.bullets = []
    data.asteroids = []
    data.timer = 0
    

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    # make the rocket rotate and fire!
    if event.keysym == "Right":
    		data.rocket.rotate(-5)
    if event.keysym == "Left":
    		data.rocket.rotate(5)
    if event.keysym == "space":
    		data.bullets.append(data.rocket.makeBullet())

def timerFired(data):
    # it might be a good idea to define onTimerFired methods in your classes...
    data.timer+=1
    for bullet in data.bullets:
    		bullet.onTimerFired(data)
    if data.timer%20==0:
    		createAsteroid(data)
    for asteroid in data.asteroids:
    		asteroid.onTimerFired(data)
    checkCollision(data)
    removeBullets(data)

def createAsteroid(data):
		cx=random.randint(1,data.width-1)
		cy=random.randint(1,data.height-1)
		r=random.randint(20,40)
		speed=random.randint(5,20)
		direction=random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
		asteroidType = random.choice([Asteroid,ShrinkingAsteroid,SplittingAsteroid])
		data.asteroids.append(asteroidType(cx,cy,r,speed,direction))

def checkCollision(data):
		for bullet in data.bullets:
				for asteroid in data.asteroids:
					 if bullet.isCollisionWithAsteroid(asteroid):
					 			asteroid.reactToBulletHit(data)
					 			break

def removeBullets(data):
		for bullet in data.bullets:
				if bullet.cx>data.width or bullet.cx<0 or bullet.cy>data.height or bullet.cy<0:
						data.bullets.remove(bullet)

def redrawAll(canvas, data):
    # draws the rocket and background
    canvas.create_rectangle(0, 0, data.width, data.height, fill="gray3")
    data.rocket.draw(canvas)
    for asteroid in data.asteroids:
    		asteroid.draw(canvas)
    for bullet in data.bullets:
    		bullet.draw(canvas)
    # don't forget to draw asteroids and bullets!

#################################################################
# use the run function as-is
#################################################################

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

run(600, 600)