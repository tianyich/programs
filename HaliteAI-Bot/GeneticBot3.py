# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position

# This library allows you to self.generate random numbers.
import random

import math

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

# Load self.gene from batch
import sys

# This game object contains the initial game state.
game = hlt.Game()
map = game.game_map
me = game.me
max_turn = constants.MAX_TURNS
shipList = None
#A register of all the ships modelled
geneticShips = {}

class GeneticShip:
    def __init__(self, ship, gene=[]):
        self.gene =gene
        self.ship = ship
        self.position = ship.position
        self.target = None
        self.target_score=0

    def findTarget(self):
        best_score = 0
        best_pos = None
        radius = self.gene[0]
        posx = self.ship.position.x
        posy = self.ship.position.y
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                target_cell = map[Position(posx+i,posy+j)]
                target_score = self.getScore(target_cell)
                if target_score > best_score:
                    best_pos = target_cell
                    best_score = target_score
        return (best_pos,best_score)
    # tc = target cell

    def getScore(self, tc = map[Position(0,0)]):
        s= self.f1(tc)+self.f2(tc)+self.f3(tc)+self.f4(tc)
        logging.info("score of "+str(tc)+": "+str(s))
        logging.info(" f1: "+str(self.f1(tc))+" f2: "+str(self.f2(tc))+" f3: "+str(self.f3(tc))+" f4: "+str(self.f4(tc)))
        return s

    def f1(self, tc = map[Position(0,0)]):
        hc = tc.halite_amount
        d = map.calculate_distance(self.ship.position, tc.position)
        return hc-self.gene[1]*H(self.ship.position, tc.position) if(d!=0) else 0

    def f2(self,tc):
        h=self.ship.halite_amount
        yard=me.shipyard
        d=map.calculate_distance(tc.position,yard.position)
        return self.gene[2]*(h-self.e2())/d if d != 0 else self.gene[2]*(h-self.e2())/0.1

    def e2(self):
        return self.gene[6]*(1-game.turn_number/max_turn)

    def f3(self,tc):
        h = self.ship.halite_amount
        total = 0
        for dropoff in me.get_dropoffs():
            d = map.calculate_distance(tc.position, yard.position)
            if(d!=0):total += self.gene[3]*(h-self.e3())/d
            else: total += self.gene[3]*(h-self.e3())/0.1
        return total

    def e3(self):
        return self.gene[7]*(1-game.turn_number/max_turn)

    def f4(self, tc):
        total = 0
        for ship in me.get_ships():
            if ship not = self.ship:
                d = map.calculate_distance(tc.position, ship.position)
                #d doesn't have special case here since no two ships can occupy the same place
                total += self.gene[4]/d
        return total
    
    def t(self, s1, s2):
        if(s2==None): return true
        return (s2-s1)/self.ship.halite_amount if(self.ship.halite_amount>0) else 0.1>self.gene[5]

    def get_move(self):
        return map.naive_navigate(self.ship, self.target.position)


# turnNumberToStop and maxShipAmount are potentially genes
def shouldProduce():
        maxShipAmount = self.gene[8]
        turnNumberToSto = self.gene[9]
        return (me.halite_amount > constants.SHIP_COST and len(shipList) <= maxShipAmount and game.turn_number <2)

def isSafe(ship, game_map):
    for d in ["n", "w", "s", "e"]:
        targetCell = game_map(ship.position.directional_offset(d))
        if not targetCell.is_occupied and not map_cell.has_structure:
            return False
    return True


def normalize_position(ship, game_map):
    x = ship.position[0]
    y = ship.position[1]
    if (x < 0 and x > game_map.width and y < 0 and y > game_map.height):
        ship.position = game_map.normalize(ship.position)

game.ready("Pinecone bot")

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    shipList = me.get_ships()
    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in shipList:
        logging.info("Ship {} has {} halite.".format(
            ship.id, ship.halite_amount))
        if(not ship.id in geneticShips):
            ngs = GeneticShip(ship, [3,1,1,1,1,0.5, 300, 300])
            geneticShips[ship.id]= ngs
            (ngs.target,ngs.target_score) = ngs.findTarget()
        gs = geneticShips[ship.id]
        if(ship.position == gs.target.position):
            command_queue.append(ship.stay_still())
        else:
            command_queue.append(ship.move(gs.get_move()))
        (newTarget, newTargetScore)=gs.findTarget()
        if(gs.t((gs.target_score), newTargetScore)):
            gs.target = newTarget
            logging.info("current target:"+str(gs.target.position))
        # See google sheets for algorithm


    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if shouldProduce():
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
