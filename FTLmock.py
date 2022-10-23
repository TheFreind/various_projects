# Imagine that all rooms are organized left to right, one dimension and in 2d.
# Game is played in "seconds":
#   - Every 1 seconds, all weapons get charge 1 seconds closer to firing. Cooldown measured in seconds
#   - Crewmembers move to adjacent rooms at a speed of 1 room/seconds
#   - Shields regenerate one bubble/2 seconds
#   - Weapons that are ready may all be fired at once
#   - Enemy weapons target random rooms (or give them targetting AI)
# WHAT IF I ADD MY OWN IDEAS OF FTL HERE??!?!?


from random import randint
import time
from FTLmockData import weaponsDatabase, roomsDatabase



class Ship(object):
    shields = 0
    evasion = 0
    oxygen = 100

    # Might need to add "rooms" parameter
    def __init__(self, name):
        self.name = name

        self.weapons = []
        self.systems = []
        self.rooms = []

        if name in playableShipsCollection:
            self.hull = 30
        else:
            self.hull = randint(5, 15) # Should be bigger for bigger ships

    def __repr__(self):
        return self.name

# Types - Laser, Flak, Missile, Bomb, Beam, Ion
class Weapon(object):
    recharge = 0
    
    ion_damage = 0
    fire_chance = 0    # Chances are in %
    breach_chance = 0
    stun_chance = 0
    beam_length = 0

    # Name of weapon, type determines rules it follows, # of damage it does, # of seconds before firing, # of projectiles, cost at shop.
    def __init__(self, name, type, damage, cooldown, projectiles, powerNeeded, shopCost):
        self.name = name    
        self.type = type
        self.damage = damage
        self.cooldown = cooldown
        self.projectiles = projectiles
        self.powerNeeded = powerNeeded
        self.shopCost = shopCost

        if type == "Laser" or type == "Beam" or type == "Missile" or type == "Flak":     # Normal damage + system damage
            self.system_damage = self.damage
            self.crew_damage = self.system_damage * 15

            if type == "Laser" or type == "Beam":       # Side effects dependent on weapon type. Chances represented in percentages. 
                self.fire_chance = 10                       # However, it needs to be more refined.
            if type == "Laser" or type == "Missile":
                self.breach_chance = 10
            if type == "Missile":
                self.stun_chance = 20
            if type == "Beam":
                self.beam_length = 2 # ! This needs reworking. 2 Represents a mini-beam length of 2 rooms.

        elif type == "Bomb":    # No damage, but system damage + crew damage
            self.damage = 0 
            self.system_damage = damage
            self.crew_damage = self.system_damage * 15
            self.breach_chance = 20
            self.fire_chance = 10
            self.stun_chance = 10

        elif type == "Ion":     # Damage converted solely to ion damage
            self.ion_damage = damage 
            self.damage = 0 
            self.system_damage = 0
            self.crew_damage = 0
            self.stun_chance = 15 

    def __repr__(self):
        return self.name


# Each room should have spaces for people, # of vents, breaches, fire, o2 in the room, and a system.
# A ship has a list of room OBJECTS, whose data is pulled from a dictionary  
class Room(object):
    fires = 0       
    breaches = 0
    oxygen = 100

    def __init__(self, size, system, vents):
        self.size = size
        self.system = system
        self.vents = vents

    def __repr__(self):
        if self.size == 2:
            return "Small - %s" % self.system
        elif self.size == 4:
            return "Big - %s" % self.system

    # function to add fires
    # function to add breaches
    #### Ensure # of fires and # of breaches do NOT exceed room size


class System(object):
    def __init__(self, name, startingLevel):
        self.name = name
        self.level = startingLevel


    def __repr__(self):
        return self.name


# Types: Ship drone, Boarding drone, attack drone, defense drone
# ! Make Boarding and Ship drones a subclass of Crew.
class Drone(object):
    health = 100

    def __init__(self, name, type):
        self.name = name
        self.type = type

# Allegiance is either "player", or "enemy"
class Crew(object):
    health = 100 # ! Exceptions needed for Zoltan, Rock, Crystal
    allegiance = ""
    speed = 1

    def __init__(self, name, species):
        self.name = name
        self.species = species

        self.skills = {
        "Piloting": 0,
        "Engines": 0,
        "Shields": 0,
        "Weapons": 0,
        "Fighting": 0,
        "Repairing": 0
        }
        self.location = randint(5) # Random spawn location       

# Database of Weapon objects in FTL (converted to Tuple later). Info imported from ..Data.py weaponsDatabase  
weaponsCollection = []

systemsCollection = ("Piloting", "Engines", "Weapons", "Shields", "Oxygen", "Medbay", "Clone Bay", "Drone Control",
                "Backup Battery", "Doors", "Sensors", "Hacking", "Mind Control", "Cloaking", "Teleporter")
encounterShipsCollection = ("Slug Interceptor", "Auto Scout", "Auto Assault", "Rebel Fighter")
playableShipsCollection = ("Kestral", "Nissan", "Osprey", "Red-Tail") # Fill this up later

SCRAP = 20

# Turn all weapons imported from a dictionary into proper Weapon classes
for gun in weaponsDatabase:
    X = weaponsDatabase[gun]  # Put dictionary's value list into X for quick indexing
    newWeapon = Weapon(gun, X[0], X[1], X[2], X[3], X[4], X[5])
    weaponsCollection.append(newWeapon)
weaponsCollection = tuple(weaponsCollection) # Solidify list by turning into tuple

# Transform room dictionary into a list of Room objects and add them to the inputted ship
# Parameter must take the Ship object
def generateRooms(whichShip):
    for X in roomsDatabase[whichShip.name]:    # Similar logic as weapons loop above this
        newRoom = Room(X[0], X[1], X[2])     # The room's Size, System, and Vents 
        whichShip.rooms.append(newRoom)
        if X[1] != "Empty":                  # Whilst we're at it, add systems in rooms to the systems list
            whichShip.systems.append(X[1])       # REMOVE THIS? Systems should be a class in of its own


print("-----------------------------------------\n\n\n")


playerShip = Ship("Kestral")

enemyShip = Ship("Rebel Fighter")




#SECONDS = 0
#for x in range(1, 31):
#    SECONDS += 1
#    time.sleep(0.1)


print("\n\n\n-----------------------------------------")
