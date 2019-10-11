# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

# Load gene from batch
import sys

class GeneticBot1(object):
    def __init__(self,gene=[],game = hlt.Game()):
        self.distanceForSearch = gene[0]
        self.cellhaliteToStay = gene[1]
        self.shipHaliteToMove = gene[2]
        self.haliteToReturn = gene[3]
        self.maxShipAmount = gene[4]
        self.turnNumberToStop = gene[5]
        self.searchingForInspire = gene[6]
        self.scoreExp = gene[7]
        self.game = game
        self.map = game.game_map
        self.me = game.me
        self.shipList = self.me.get_ships()

    def searchForHalite(self, ship = self.shipList[0]):
        
        richest_amount = 0
        best_pos = null
        radius = self.distanceForSearch//2
        posx = ship.position[0]
        posy = ship.position[1]
        for i in range radius:
            for j in range radius:
                target_cell = self.map[Position(pox+i,posy+j)]
                target_halite_amount = target_cell.halite_amount
                if target_halite_amount > richest_amount:
                    best_pos = target_cell
                    richest_amount = target_halite_amount
        return best_pos

    def shouldProduce(self):
        if self.me.halite_amount > constants.SHIP_COST and len(self.shipList) <= self.maxShipAmount 
        and self.game.turn_number < self.turnNumberToStop:
            return True
        else:
            return False

    def shouldReturn(self,ship = self.shipList[0]):
        if ship.halite_amount >= self.haliteToReturn:
            return True
        else:
            return False
    
    def shouldMove(self, ship = self.shipList[0]):
        pos = ship.position
        if pos.halite_amount < self.haliteToStay and ship.halite_amount > self.shipHaliteToMove:
            return True
        else:
            return False

    def get_move(self, ship = self.shipList[0]):
        
        
