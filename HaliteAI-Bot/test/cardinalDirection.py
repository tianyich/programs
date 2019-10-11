
import math


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def getCardinal(c,d):
    a = c
    b = d
    theta = math.asin((b.y-a.y)/math.sqrt((b.y-a.y)**2+(b.x-a.x)**2))
    if(b.x-a.x < 0):
        theta = math.pi-theta
    cardinals = ['n', 'w', 's', 'e']
    return cardinals[int(((theta+2*math.pi-math.pi/4) % (2*math.pi))/(math.pi/2))]


print(getCardinal(Position(0, 0), Position(1, 0)))
print(getCardinal(Position(0, 0), Position(0, 1)))
print(getCardinal(Position(0, 0), Position(-1, 0)))
print(getCardinal(Position(0, 0), Position(0, -1)))
print(getCardinal(Position(0, 0), Position(1, 1)))
print(getCardinal(Position(0, 0), Position(-1, 1)))
print(getCardinal(Position(0, 0), Position(-1, -1)))
print(getCardinal(Position(0, 0), Position(1, 1)))
