# Imagine that all rooms are organized left to right, one dimension and in 2d.
# Game is played in "seconds":
#   - Every 1 seconds, all weapons get charge 1 seconds closer to firing. Cooldown measured in seconds
#   - Crewmembers move to adjacent rooms at a speed of 1 room/seconds
#   - Shields regenerate one bubble/2 seconds
#   - Weapons that are ready may all be fired at once
#   - Enemy weapons target random rooms (or give them targetting AI)
# WHAT IF I ADD MY OWN IDEAS OF FTL HERE??!?!?

# THINGS TO ADD LATER:
#   Fire needs to spreading mechanics
#   The whole oxygen system
#   Opening vents
#   Fire needs to damage
#   Drones

# UNTESTED FEATURES
# XP


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



def grantStartingGear(shipClass, startingGear, weaponsDatabase):
    for selectShip in startingGear:
        if selectShip == shipClass.name:
        
        ### Get Weapons ###
            for desire in startingGear[selectShip][0]: 
                for gun in weaponsCollection:                   
                    if desire == gun.name:                      
                        shipClass.weapons[gun.name] = gun       # Add to ship weapon dictionary ---> "Name": Weapon Object 
                        continue

        ### Get Rooms ###
            for X in roomsDatabase[shipClass.name]:    # Similar logic as weapons loop above this
                if X[1] != "Empty":                  # Whilst we're at it, add systems in rooms to the systems list
                    sysName = X[1]
                    maxUpgradeableLevel = systemsDatabase[sysName]
                # Simultaneously define the System class w/ newly made parameters and add it to ship system dictionary
                    addNewSystem = System(sysName, 1, maxUpgradeableLevel)
                    shipClass.systems[sysName] = addNewSystem
                else:
                    addNewSystem = X[1]

                newRoom = Room(X[0], addNewSystem, X[2], shipClass)     # The room's Size, SystemClass, Vents, and ship its a part of 
                shipClass.rooms.append(newRoom)

        ### Set starting levels of systems ###
            sysData = zip(startingGear[selectShip][2], startingGear[selectShip][3])
            for x in sysData:
                sysName = x[0]
                sysStartingLevel = x[1]

                shipClass.systems[sysName].systemLevel = sysStartingLevel # Set system level from ship database
                shipClass.systems[sysName].power = sysStartingLevel # Automatically give that system maximum power
                #print("System name: %s | System level: %d | Power: %d" % (sysName, shipClass.systems[sysName].systemLevel, shipClass.systems[sysName].power) )

        ### Get Drones ###

        ### Get crew ####
            for person in startingGear[selectShip][4]:
                Crew(person, shipClass, crewNameDatabase)
        
        else:
            continue



    if shipClass.name in playableShipsCollection:           # Find weapons for a player's ship. 
        pass
    #else enemy encounter weaponry


# What if this is a seperate method of Ship and not a function?
def otherShip(whoAreWe):
    if whoAreWe == playerShip:
        return enemyShip
    elif whoAreWe == enemyShip:
        return playerShip


def checkWeaponStatus(shipClass):
    for index, gun in enumerate(shipClass.weapons.values() ):
        if gun.charge >= gun.cooldown and gun.autoFire == True:
            shipClass.fireWeapon(gun, otherShip(shipClass) )
        elif gun.charge >= gun.cooldown and gun.autoFire == False:
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


grantStartingGear(playerShip, startingGear, weaponsCollection)
grantStartingGear(enemyShip, startingGear, weaponsCollection)       

#Testing scenario where all enemy crew board our ship in weapons
#! This is a useful, basic template for the Teleporter
#   for boarder in teleporter.room.crewInRoom:
for boarder in enemyShip.crew:
    boardingChoice = "Weapons"

    # Fundamental problem - checkRoom.system.name not possible on "Empty" rooms b/c it's a string and not a system object
    # What do I do if you board an "Empty" room? The code depends on that. Unless... its room index!
    for roomIndex, checkRoom in enumerate(otherShip(boarder.shipOnboard).rooms):
        if checkRoom.system != "Empty" and checkRoom.system.name == boardingChoice:
            # MISSING CHECK - What if room is full of crew? Where do excess go?
            boarder.location = checkRoom                            # Boarder is now in room
            boarder.shipOnboard = checkRoom.parentShip              # Boarder is now in room's ship
            boarder.locationIndex = roomIndex                       # Get this room's index in ship's list
            boarder.destinationIndex = roomIndex                    # Boarder isn't immediately moving.
            checkRoom.crewInRoom[boarder.stats["Allegiance"]].append(boarder)   # Add boarder to his team in room
            boarder.roomPositionIndex = len(checkRoom.crewInRoom[boarder.stats["Allegiance"]]) - 1  # Get his tile in room

            break
    else:
        print("%s does not exist onboard %s!" % (boardingChoice, boarder.shipOnboard.name) )

    print("%s %s is in %s, onboard the %s." % (boarder.stats["Allegiance"], boarder.name, boarder.location, boarder.shipOnboard))


playerShip.crew[0].destinationIndex = 3    # First crewmember goes to Kestrel's 4th room (weapons)

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

        thisPlayer.checkEvasion() # Double check if evasion has changed
        
        for gun in thisPlayer.weapons.values(): # All weapons not ready will charge up 1 second
            if gun.charge < gun.cooldown:
                gun.charge += 1

        checkWeaponStatus(thisPlayer)

        for room in thisPlayer.rooms:
            if room.system != "Empty":
                room.system.checkCrewPresence(room)

        for crewMember in thisPlayer.crew: # All crewmembers move 1 step closer to their destination
            # if stunned, skip this second and count down stun duration
            #
            if crewMember.locationIndex != crewMember.destinationIndex:
                crewMember.moveAction()
            else:
                crewMember.evaluateTask()

        # ! Oxygen depletion not yet implemented
        # Fire suppression augment should extinguish fires in this section of code.
        for room in thisPlayer.rooms:
            if len(room.fires) > 0:
                if room.system != "Empty":  # System takes damage from fire
                    room.system.damageProgress += 0.75 * len(room.fires)

                    if room.system.damageProgress >= 10: # When system accumulates enough damage, damage a power bar.
                        room.system.damage += 1
                        room.system.damageProgress = 0

                        if room.system.damage == room.system.systemLevel:
                            room.parentShip.hull -= 1
                            print(" [! %s of %s has been burned down by fire!" % (room.system.name, room.parentShip.name) )

                for allegiance in room.crewInRoom:  # All crew in room take fire damage
                    for crew in room.crewInRoom[allegiance]:
                        if crew.stats["Fire immunity"] == False:
                            crew.sufferDamage(5 * len(room.fires)) # 5 dmg per fire / second

                # Deplete oxygen

                # Fire spreads in room.
                # ! Needs functionality to spread to other rooms
                room.fireProgress += len(room.fires)
                if room.fireProgress >= room.fireChance:
                    room.startFire("Spread")



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
print(f"Combat has finished after {SECONDS} seconds." )
# for room in enemyShip.rooms:
#     print("Room: %s | Fires: %d | Breaches: %d" % (room.system, len(room.fires), len(room.breaches)) )

# for room in enemyShip.rooms:
#     if room.system != "Empty":
#         print("Room's System: %s | Power: %d | Damage: %d " % (room.system, room.system.power, room.system.damage)) 
#     else:
#         print("Room's System: %s ")    

print("\n\n\n-----------------------------------------")
