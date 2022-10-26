# Imagine that all rooms are organized left to right, one dimension and in 2d.
# Game is played in "seconds":
#   - Every 1 seconds, all weapons get charge 1 seconds closer to firing. Cooldown measured in seconds
#   - Crewmembers move to adjacent rooms at a speed of 1 room/seconds
#   - Shields regenerate one bubble/2 seconds
#   - Weapons that are ready may all be fired at once
#   - Enemy weapons target random rooms (or give them targetting AI)
# WHAT IF I ADD MY OWN IDEAS OF FTL HERE??!?!?

import time
from random import randint, choice
from FTLmockData import * # Dictionaries info


class Ship(object):
    destroyed = False
    shields = 0
    evasion = 15
    oxygen = 100

    # Might need to add "rooms" parameter
    def __init__(self, name):
        self.name = name

        self.weapons = {}
        self.systems = {}
        self.rooms = []

        if name in playableShipsCollection:
            self.hull = 30
        else:
            self.hull = randint(5, 15) # Should be bigger for bigger ships



    def grantStartingWeapons(self, playableShipsCollection, startingWeapons, weaponsCollection):
        if self.name in playableShipsCollection:           # Find weapons for a player's ship. 
            for desire in startingWeapons[self.name]: 
                for gun in weaponsCollection:   
                    print(desire, gun.name)#                
                    if desire == gun.name:                      
                        self.weapons[gun.name] = gun
                        break

        #else enemy encounter weaponry

    def __repr__(self):
        return self.name


    # Needs more work
    def fireWeapon(self, gun, target):
        #print(f'{gun} is firing at {target}!')
        # Choose room, hit shields, miss shots, damage system, damage crew, etc...
        # Enter targetting room. This here is just random room selection.
        

        for shot in range(gun.projectiles):
            room_targetted = choice(target.rooms) # Suggestion: Make AI more likely to target high-value systems.
            roll_to_hit = randint(1, 100)
            if target.evasion > roll_to_hit and gun.type != "Beam":     # Beams cannot miss
                print("MISS!")
            else:

                if gun.type == "Beam":
                    target.hull -= gun.damage * gun.beam_length
                else:
                    target.hull -= gun.damage
                # System in room takes 2 damage
                # Crew damage applied to all crew in room
                roll_to_add_fire = randint(1, 100)
                roll_to_add_breach = randint(1, 100)
                #roll_to_stun = randint(1, 100)
                if roll_to_add_fire <= gun.fire_chance and len(room_targetted.fires) < room_targetted.size: # Max fires = size of room
                    room_targetted.fires.append(40) # Add a 40 health fire to the fire list
                    print("Fire started!")
                if roll_to_add_breach <= gun.breach_chance and len(room_targetted.breaches) < room_targetted.size:
                    room_targetted.breaches.append(40)
                    print("Hull breached!")
                #if roll_to_stun <= gun.stun_chance:
                #    pass           

                if target.hull <= 0:
                    target.destroyed = True
                else:
                    print(f"{target}'s hull has been reduced down to {target.hull}.")


        gun.charge = 0
        if gun.type == "Missile" or gun.type == "Bomb":
            global MISSILES
            MISSILES -= 1






# Types - Laser, Flak, Missile, Bomb, Beam, Ion
class Weapon(object):
    charge = 0
    
    ion_damage = 0
    fire_chance = 0    # Chances are in %
    breach_chance = 0
    stun_chance = 0
    beam_length = 0

    autoFire = True    # When enemy AI cloaks, it deactivates autoFire and reenables when exiting cloak

    # Name of weapon, type determines rules it follows, # of damage it does, # of seconds before firing, # of projectiles, cost at shop.
    def __init__(self, name, type, damage, cooldown, projectiles, powerNeeded, shopCost):
        self.name = name    
        self.type = type
        self.damage = damage
        self.cooldown = cooldown
        self.projectiles = projectiles
        self.powerNeeded = powerNeeded
        self.shopCost = shopCost
        # set to Auto or Manual firing?

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
    oxygen = 100

    def __init__(self, size, system, vents):
        self.size = size
        self.system = system
        self.vents = vents

        self.fires = [] # List containing health of each fire. # of fires is len of the list.   
        self.breaches = [] # Ditto

    def __repr__(self):
        if self.size == 2:
            return "Small - %s" % self.system
        elif self.size == 4:
            return "Big - %s" % self.system

    # function to add fires
    # function to add breaches
    #### Ensure # of fires and # of breaches do NOT exceed room size


class System(object):
    power = 1           # Amount of power in system
    systemLevel = 2     # Current level of System. Can take up to this much power
    damage = 0
    ion_damage = 0
        #allowablePower = systemLevel
    allowablePower = systemLevel - damage - ion_damage

    def __init__(self, name, maxUpgradeableLevel):
        self.name = name
        self.maxUpgradeableLevel = maxUpgradeableLevel


    def __repr__(self):
        return self.name

    #def determinePower(self):
    #    allowablePower = self.systemLevel - self.damage - self.ion_damage

    #def powerUp(self, amount):     # Cannot exceed allowablePower
    #def powerDown(self, amount):   # Cannot exceed allowablePower

    def rejuvenateShield(self, ship):
        for item in ship.systems:
            if item.name == "Shields":
                
                
                break




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
            sysName = X[1]
            maxUpgradeableLevel = systemsDatabase[sysName]
        # Simultaneously define the System class w/ newly made parameters and add it to ship system dictionary
            whichShip.systems[sysName] = System(sysName, maxUpgradeableLevel) # Add to ship system dict ---> "Name": System Object


def grantStartingWeapons(shipClass):
    if shipClass.name in playableShipsCollection:           # Find weapons for a player's ship. 
        for desire in startingWeapons[shipClass.name]: 
            for gun in weaponsCollection:                   
                if desire == gun.name:                      
                    shipClass.weapons[gun.name] = gun       # Add to ship weapon dictionary ---> "Name": Weapon Object 
                    continue
    #else enemy encounter weaponry

# What if this is a seperate method of Ship and not a function?
def otherShip(whoAreWe):
    if whoAreWe == playerShip:
        return enemyShip
    elif whoAreWe == enemyShip:
        return playerShip


def checkWeaponStatus(shipClass):
    for index, gun in enumerate(shipClass.weapons):
        if gun.charge == gun.cooldown and gun.autoFire == True:
            shipClass.fireWeapon(gun, otherShip(shipClass) )
        elif gun.charge == gun.cooldown and gun.autoFire == False:
            #print("#%d [%s] %s - READY" % (index+1, "I"*gun.powerNeeded, gun) )
            pass
        elif gun.charge < gun.cooldown:
            #print("#%d [%s] %s - %ds remaining..." % (index+1, "I"*gun.powerNeeded, gun, (gun.cooldown-gun.charge)) )
            pass



SCRAP = 20
FUEL = 13
MISSILES = 12
DRONEPARTS = 0


print("-----------------------------------------\n\n\n")


playerShip = Ship("Kestral")
enemyShip = Ship("Rebel Fighter")

playerShip.grantStartingWeapons(playableShipsCollection, startingWeapons, weaponsCollection)
# Insert Enemy grantStartingWeapons    once I finish adding enemy weapon logic

generateRooms(playerShip)
generateRooms(enemyShip)

#print(playerShip.checkWeaponStatus())



# SECONDS = 0
# for x in range(1, 60):
#     SECONDS += 1
#     for gun in playerShip.weapons: # All weapons not ready will charge up 1 second
#         if gun.charge < gun.cooldown:
#             gun.charge += 1

#     #checkWeaponStatus(playerShip)
#     if otherShip(playerShip).destroyed == True: # You won the fight
#         print("%s has been destroyed! Well done. Precluding combat." % otherShip(playerShip) )
#         # Earn rewards
#         break
#     elif otherShip(enemyShip).destroyed == True: # You lose
#         print("The %s has been annihilated... We have failed our mission. Game over." % otherShip(enemyShip) )
#         # Game over will occur
#         break


#     time.sleep(0.1)



print(playerShip.weapons.keys())
print("This %s can deal %d damage" % (playerShip.weapons["Artemis"].name, playerShip.weapons["Artemis"].damage) )

for name in playerShip.systems:
    print("Max upgrades for %s: %d" % (name, playerShip.systems[name].maxUpgradeableLevel) )

        

print("\n\n\n-----------------------------------------")
