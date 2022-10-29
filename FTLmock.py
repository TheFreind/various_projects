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
from FTLmockClasses import *

   


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
        if X[1] != "Empty":                  # Whilst we're at it, add systems in rooms to the systems list
            sysName = X[1]
            maxUpgradeableLevel = systemsDatabase[sysName]
        # Simultaneously define the System class w/ newly made parameters and add it to ship system dictionary
            #whichShip.systems[sysName] = System(sysName, maxUpgradeableLevel) # Add to ship system dict ---> "Name": System Object
            addNewSystem = System(sysName, maxUpgradeableLevel)
            whichShip.systems[sysName] = addNewSystem
        else:
            addNewSystem = X[1]

        newRoom = Room(X[0], addNewSystem, X[2])     # The room's Size, System, and Vents 
        whichShip.rooms.append(newRoom)


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
    for index, gun in enumerate(shipClass.weapons.values() ):
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
# missiles and drone_parts variables are found in ship classes.


print("-----------------------------------------\n\n\n")


playerShip = Ship("Kestral", playableShipsCollection)
enemyShip = Ship("Rebel Fighter", playableShipsCollection)

playerShip.grantStartingWeapons(playableShipsCollection, startingWeapons, weaponsCollection)
# Insert Enemy grantStartingWeapons    once I finish adding enemy weapon logic

generateRooms(playerShip)
generateRooms(enemyShip)

##### Start of combat touch-up ######
combatants = [playerShip, enemyShip]
SECONDS = 0
for gun in playerShip.weapons.values():
    gun.charge = 0                      # If pre-igniter in augments, gun.charge = cooldown
playerShip.shield_recharge_progress = 0
##### Begin combat in terms of seconds, continue until destroyed ######
while enemyShip.destroyed == False:
    SECONDS += 1

    for thisPlayer in combatants:
        if "Shields" in thisPlayer.systems:
            thisPlayer.rejuvenateShield(thisPlayer.systems["Shields"])

    #print(f'Enemy shields: {enemyShip.shields}') 

    for gun in playerShip.weapons.values(): # All weapons not ready will charge up 1 second
        if gun.charge < gun.cooldown:
            gun.charge += 1

    checkWeaponStatus(playerShip)
    if otherShip(playerShip).destroyed == True: # You won the fight
        print("\n%s has been destroyed! Well done. Precluding combat." % otherShip(playerShip) )
        # Earn rewards
        break
    elif otherShip(enemyShip).destroyed == True: # You lose
        print("\nThe %s has been annihilated... We have failed our mission. Game over." % otherShip(enemyShip) )
        # Game over will occur
        break


    time.sleep(0.01)


# print("\n ---------- A.A.R. ----------")
# for room in enemyShip.rooms:
#     print("Room: %s | Fires: %d | Breaches: %d" % (room.system, len(room.fires), len(room.breaches)) )

# for room in enemyShip.rooms:
#     if room.system != "Empty":
#         print("Room's System: %s | Power: %d | Damage: %d " % (room.system, room.system.power, room.system.damage)) 
#     else:
#         print("Room's System: %s ")    

print("\n\n\n-----------------------------------------")
