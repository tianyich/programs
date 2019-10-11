
import hlt
from hlt import constants
import random
import logging

#Problems:
#Rule regarding ship to dropoff conversion, how do we spend halite: from stored halite
#Rule regarding ship overflow: wrap
#Ship crash: Baobi
#Getting dropoff locations: me.get_dropoffs()
#Manhattan distance between a and b: game_map.calculate_distance(a,b)


# This game object contains the initial game state.
game = hlt.Game()
# Respond with your name.
game.ready("TianyiBot2")
ship_status={}


def get_move(ship,game_map):
    halite_amount_around={}
    for d in ["n","w","s","e"]:
        targetCell = game_map(ship.position.directional_offset(d))
        halite_amount_around[d]=targetCell.halite_amount
    richest_amount = halite_amount_around["n"]
    bestd = "n"
    for d in ["n","w","s","e"]:
        if halite_amount_around[d]>richest_amount:
            bestd=d
            richest_amount=halite_amount_around[d]
    if not targetCell.is_occupied or isSafe(targetCell):
            return d

def isSafe(ship,game_map):
    for d in ["n","w","s","e"]:
        targetCell = game_map(ship.position.directional_offset(d))
        if not targetCell.is_occupied and not map_cell.has_structure:
            return False
    return True

def normalize_position(ship,game_map):
    x= ship.position[0]
    y= ship.position[1]
    if (x<0 and x>game_map.width and y<0 and y>game_map.height):
        ship.position=game_map.normalize(ship.position)



while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"
        
        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(move))
                continue
        elif ship.halite_amount >= constants.MAX_HALITE / 4:
            ship_status[ship.id] = "returning"
            
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(random.choice(["n", "s", "e", "w"])))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if game.turn_number <= 1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
