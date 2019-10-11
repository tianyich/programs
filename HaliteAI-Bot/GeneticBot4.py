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
targetList = []

# gene 0: search radius percentage
# gene 1: score 
# gene 2: least halite to continue moving
# gene 3: return coefficient
# gene 4: maxship amount
# gene 5: turn number to stop producing
# gene 6: turn number to retrieving all ships

class GeneticShip:
    def __init__(self,ship,gene):
        self.gene =gene
        self.ship = ship
        self.position = ship.position
        self.target = None
        self.target_score = 0
        self.isLocked = False

    def findTarget(self):
        best_score = 0
        best_pos = None
        radius = int(self.gene[0]*map.width)
        posx = self.ship.position.x
        posy = self.ship.position.y
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                target_cell = map[Position(posx+i,posy+j)]
                target_score = self.getScore(target_cell)
                if (target_score > best_score) and (not target_cell in targetList) and (target_cell.position != self.position):
                    best_pos = target_cell
                    best_score = target_score
        if (not self.target is None) and (self.target != map[me.shipyard.position]):
            targetList.remove(self.target)
        self.target = best_pos
        self.target_score = best_score
        self.isLocked = True
        targetList.append(self.target)

    def getScore(self, tc = map[Position(0,0)]):
        hc = tc.halite_amount
        d = map.calculate_distance(self.ship.position, tc.position)
        return hc-d*self.gene[1] if d !=0 else 0

    def shouldMove(self):
        haliteToMove = gene[2]
        if self.ship.halite_amount > haliteToMove or self.ship.position == me.shipyard.position:
            return True
        else:
            return False

    def shouldReturn(self):
        d = map.calculate_distance(self.ship.position,me.shipyard.position)
        hc = self.ship.halite_amount
        return hc*self.gene[3]/d if d != 0 else 0

    def get_move(self):
        naive_dir = map.naive_navigate(self.ship, self.target.position)
        if not self.shouldMove():
            return "o"
        elif self.isSafe(naive_dir):
            return naive_dir
        else:
            self.isLocked = False
            return self.getSafeDir()

    def closestDropOff(self):
        return me.shipyard

    def isSafe(self,d):
        target_cell = self.position.directional_offset(d)
        return (not map[target_cell].is_occupied)
    
    def getSafeDir(self):
        for direction in [(1,0),(0,1),(-1,0),(0,-1)]:
            target_cell = self.position.directional_offset(direction)
            if (not map[target_cell].is_occupied):
                return direction
        else:
            return "o"

    def normalize_position(self,ship, map):
        x = ship.position[0]
        y = ship.position[1]
        if (x < 0 and x > game_map.width and y < 0 and y > game_map.height):
            ship.position = game_map.normalize(ship.position)
    

def shouldProduce(maxShipAmount,turnNumberToStop):
        return (me.halite_amount > constants.SHIP_COST and len(shipList) <= maxShipAmount and game.turn_number < turnNumberToStop*constants.MAX_TURNS)

game.ready("Pinecone bot")

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    shipList = me.get_ships()
    # A command queue holds all the commands you will run this turn.
    command_queue = []
# gene 0: search radius
# gene 1: score coefficient
# gene 2: least halite to continue moving
# gene 3: return coefficient
# gene 4: maxship amount
# gene 5: turn number percent to stop producing
# gene 6: turn number to retrieving all ships
    gene = [0.4,1,200,1,40,0.6,0.8,600]
    for ship in shipList:
        logging.info("Ship {} has {} halite.".format(
            ship.id, ship.halite_amount))
        if(not ship.id in geneticShips):
            ngs = GeneticShip(ship, gene)
            geneticShips[ship.id]= ngs
            ngs.findTarget()
        gs = geneticShips[ship.id]

        if(ship.position == gs.target.position):
            command_queue.append(ship.stay_still())
            gs.isLocked = False
            gs.findTarget()
        if(gs.isLocked == False):
            gs.findTarget()
            command_queue.append(ship.move(gs.get_move()))
        if(ship.halite_amount >= gene[7]):
            gs.target = map[me.shipyard.position]
            gs.isLocked = True
            command_queue.append(ship.move(gs.get_move()))
        
        logging.info(str(ship.id)+str(gs.isLocked))
    if (game.turn_number >= constants.MAX_TURNS*gene[6]):
        for ship in geneticShips:
            gs.isLocked = True
            gs.target = gs.closestDropOff()
        
    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if shouldProduce(gene[4],gene[5]):
        command_queue.append(game.me.shipyard.spawn())

    
    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
