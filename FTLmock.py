# Imagine that all rooms are organized left to right, one dimension and in 2d.
# Game is played in "seconds":
#   - Every 1 seconds, all weapons get charge 1 seconds closer to firing. Cooldown measured in seconds
#   - Crewmembers move to adjacent rooms at a speed of 1 room/seconds
#   - Shields regenerate one bubble/2 seconds
#   - Weapons that are ready may all be fired at once
#   - Enemy weapons target random rooms (or give them targetting AI)
# WHAT IF I ADD MY OWN IDEAS OF FTL HERE??!?!?

# THINGS TO ADD LATER:
#   Fire needs spreading mechanics
#   The whole oxygen system
#   Opening vents
#   Drones
#   System effects.
#   Door system
#   Proper randomized enemy loadouts. They're pre-set.

# Cool idea - What if all print statements are put into a "notification" list?
#   And there are different kinds, like crewNotifications, shipNotifications, etc...
#   Best of all, if something happens in a room you have no vision of, you do not
#   get a corresponding notification (unless its obvious)!

# UNTESTED FEATURES
# The stun function  
# The loop in system.repairSystem(), regarding determineDamage. Any problems if Weapons is repaired by a repair bomb?
#   Speaking of which, the whole process of siphoning/delegating reactor power

# CURRENT BUGS.
# Fired at enemy ship's weapons. Enemy crewmember on MY SHIP got stunned. huh?
# As soon as combat ends, the loop terminates. Any projectiles in flight will "dissappear". 
#    Pretty convenient dodging a Breach Missile by ending the fight, huh?
# All missile weapons have their fire/breach/stun chance listed on wiki.
#   APPARENTLY - Cannot cause a fire and breach in the same shot. Fire chance rolls first.

import time
from random import randint, choice
from FTLmockData import * # Dictionaries info
from FTLmockClasses import *

secondsInterval = 0.1   # Game progresses at 0.1 second at a time.



#def grantStartingGear(shipClass, startingGear):
def grantStartingGear(shipClass):
    for selectShip in startingGear:
        if selectShip == shipClass.name:

        ### Get fuel, missiles, drones, reactor ###
        # ! Is it really only for player? I think enemies deserve it
            if shipClass.name in playableShipsCollection:
                FUEL = startingGear[selectShip][6][0]
                shipClass.missiles = startingGear[selectShip][6][1]
                shipClass.drone_parts = startingGear[selectShip][6][2]
                shipClass.reactorLevel = startingGear[selectShip][6][3]
        
        ### Get Weapons ###
        # ! Enemies should get randomized weapons
            for gunName in startingGear[selectShip][0]: 
                X = weaponsDatabase[gunName]    # Put dictionary's value list into X for quick indexing
                newWeapon = Weapon(shipClass, gunName, X[0], X[1], X[2], X[3], X[4], X[5], X[6])
                shipClass.weapons.append(newWeapon)

        ### Get Rooms ###
        # ! Enemies should have randomized systems
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
                if X[1] != "Empty":
                    shipClass.systems[X[1]].parentRoom = newRoom        # Give the newly created system an attribute to access its room

        ### Set starting levels of systems ###
        # ! TO Starting levels need to be dependent on sector difficulty.
            sysData = zip(startingGear[selectShip][2], startingGear[selectShip][3])
            for x in sysData:
                sysName = x[0]
                sysStartingLevel = x[1]

                shipClass.systems[sysName].systemLevel = sysStartingLevel # Set system level from ship database
                shipClass.systems[sysName].power = sysStartingLevel # Automatically give that system maximum power
                shipClass.systems[sysName].systemPowerMemory = shipClass.systems[sysName].power # Preferred power

        ### Get doors for rooms ###
            for room in shipClass.rooms:
                if "Doors" in shipClass.systems:    # If ship has door subsystem
                    doorLevel = shipClass.systems["Doors"].systemLevel
                    for x in range(2):
                        room.doors.append([ doorLevel , 10*doorLevel, "Closed" ])
                else:                               # Otherwise, level 1 doors
                    for x in range(2):
                        room.doors.append([ 1 , 10, False ])


        ### Get Drones ###

        ### Get crew ####
            for person in startingGear[selectShip][4]:
                Crew(person, shipClass, crewNameDatabase)

        # Is enemy ship an auto ship? Give it its property.
            if shipClass.name in enemyAutoShips:
                shipClass.auto_ship = True
            
        # If the ship doesn't come with an oxygen system, all rooms will have 0 oxygen.
            if "Oxygen" not in shipClass.systems:
                for room in shipClass.rooms:
                    room.oxygen = 0
        
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


# All projectiles travel to their target. When time to connect is 0, resolve a hit.
def checkProjectiles(projectilesInFlight):
    for index, projectile in enumerate(projectilesInFlight):
        projectile[1] -= secondsInterval
        if projectile[1] <= 0:
            projectile[0].resolveHit(projectile[2])
            del projectilesInFlight[index]




SCRAP = 20
FUEL = 13
# missiles and drone_parts variables are found in ship classes.

print("-----------------------------------------\n\n\n")


playerShip = Ship("Kestral", playableShipsCollection)
enemyShip = Ship("Rebel Fighter", playableShipsCollection)


grantStartingGear(playerShip)
grantStartingGear(enemyShip)       

#Testing scenario where all enemy crew board our ship in weapons
#! This is a useful, basic template for the Teleporter
#   for boarder in shipClass.systems["Teleporter"].parentRoom.crewInRoom[ -- INSERT PROPER ALLEGIANCE -- ]:
for boarder in enemyShip.crew:
    boardingChoice = "Engines"

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


playerShip.crew[0].destinationIndex = 3    # First crewmember goes to Kestrel's 2nd room (Engines)
playerShip.crew[2].destinationIndex = 4    # Third crewmember goes to Kestrel's 5th room (Shields)
#playerShip.systems["Medbay"].parentRoom.fires.append(40)    # Add a testing fire to see if it does damage

playerShip.crew.append( Drone() )
#print(playerShip.crew[3].movementProgress)


##### Start of combat touch-up ######
combatants = [playerShip, enemyShip]
projectilesInFlight = []    # [(Weapon, time_before_impact, targetShip)]
SECONDS_ELAPSED = 0

for ship in combatants:
    for systemName in ship.systems:
        for x in range(ship.systems[systemName].systemPowerMemory):
            if ship.reactorUsage < ship.reactorLevel:
                ship.reactorUsage += 1

for gun in playerShip.weapons:
    gun.charge = 0                      # If pre-igniter in augments, gun.charge = cooldown
#playerShip.shield_recharge_progress = 0        # Unnecessary? Ships are generated not charging shields, but you can be charging when jumping between beacons.
##### Begin combat in terms of seconds, continue until destroyed ######
while enemyShip.destroyed == False:
    SECONDS_ELAPSED += secondsInterval
    checkProjectiles(projectilesInFlight)

    for thisPlayer in combatants:
        # Regenerate shields
        if "Shields" in thisPlayer.systems:
            thisPlayer.rejuvenateShield(thisPlayer.systems["Shields"])

        # Double check if evasion has changed
        thisPlayer.checkEvasion(thisPlayer.systems["Piloting"].parentRoom, thisPlayer.systems["Engines"].parentRoom) 
        
        # Weapons are charged secondsInterval if powered; weapons rapidly lose charge if de-powered
        for gun in thisPlayer.weapons: 
            if gun.powered == False and gun.charge > 0:
                gun.charge -= 3 * secondsInterval
                #print("DEBUGGING - %s of %s is powered down!" % (gun.name, thisPlayer.name))#
            elif gun.powered == True and gun.charge < gun.cooldown:
                gun.charge += secondsInterval
            
            gun.checkWeaponStatus(thisPlayer, otherShip(thisPlayer), projectilesInFlight)


        # Systems being damaged/repaired will be reset if crew leave room 
        # Ion duration on systems reduced
        # Sensors, crew, telepathy reveals rooms 
        # ! Telepathy not implemented yet
        for room in thisPlayer.rooms:
            if room.system != "Empty":
                room.system.checkCrewPresence(room)
                if room.system.ion_duration > 0:       
                    room.system.ion_duration -= secondsInterval

            if "Sensors" in thisPlayer.systems:
                room.visible = True
            elif ( (thisPlayer.isPlayer == True and len(room.crewInRoom["friendly"]) > 0) or 
                   (thisPlayer.isPlayer == False and len(room.crewInRoom["hostile"]) > 0) ):
                room.visible = True
            # ! elif telepathy
            else:
                room.visible = False

        for crewMember in thisPlayer.crew: 
            if crewMember.location.system.name == "Medbay": # Crew always heal if in medbay
                crewMember.location.system.medbayHeal(crewMember)
            if crewMember.location.oxygen <= 5:             # Crew suffocate from low oxygen
                crewMember.sufferDamage(6.4 * secondsInterval * crewMember.stats["Suffocation damage"], "Suffocation")

            # Crew members do not take actions when stunned. Count down stun duration and skip this second.
            if crewMember.stats["Stun duration"] > 0:
                crewMember.stats["Stun duration"] -= secondsInterval
            else:
                if crewMember.locationIndex != crewMember.destinationIndex: # All crewmembers move 1 step closer to their destination
                    crewMember.moveAction()
                else:
                    crewMember.evaluateTask()   # If not moving, determine what task to do. Examine this function for details.

        # ! Venting rooms of oxygen not implemented
        # ! Oxygen flowing to rooms with less oxygen not implemented
        if "Oxygen" in thisPlayer.systems:
            if thisPlayer.systems["Oxygen"].power == 0:
                for room in thisPlayer.rooms:
                    room.oxygen -= 1.2 * secondsInterval

            else:
                oxygenRegenerationRateModifier = [0, 1, 2, 3]
                for room in thisPlayer.rooms:
                    room.oxygen += 1.2 * secondsInterval * oxygenRegenerationRateModifier[thisPlayer.systems["Oxygen"].power]

        # Fire suppression augment should extinguish fires in this section of code.
        for room in thisPlayer.rooms:
            if len(room.fires) > 0:
                if room.system != "Empty" and room.system.damage < room.system.systemLevel:  # System takes damage from fire
                    room.system.damageProgress += 0.75 * secondsInterval * len(room.fires)

                    if room.system.damageProgress >= 10: # When system accumulates enough damage, damage a power bar.
                        room.system.damageSystem(1, False)
                        room.system.damageProgress = 0

                        if room.system.damage == room.system.systemLevel:
                            room.parentShip.hull -= 1
                            print(" [! %s of %s has been burned down by fire!" % (room.system.name, room.parentShip.name) )

                for allegiance in room.crewInRoom:  # All crew in room take fire damage
                    for crew in room.crewInRoom[allegiance]:
                        if crew.stats["Fire immunity"] == False:
                            crew.sufferDamage(3 * secondsInterval * len(room.fires), "Fire") # 3 dmg per fire / second

                # Fires consume oxygen
                room.oxygen -= 1.2 * secondsInterval * len(room.fires)

                # No oxygen will lead to fires getting extinguished
                if room.oxygen <= 5:
                    for fire in room.fires:
                        fire -= 10 * secondsInterval

                # Fire spreads in room.
                room.fireJumpChance += len(room.fires) * secondsInterval
                room.fireProgress += len(room.fires) * secondsInterval
                if room.fireProgress >= room.fireChance:
                    room.startFire("Spread", "Something")

                # Fire has a random % chance to spread to nearby room.
                # rollToSpreadFire = randint(0, 100)
                # if rollToSpreadFire < room.fireJumpChance:
                #     oddsForEachRoom = [100/len(room.doors)] * len(room.doors)
                    
                #     for checkingDoorIndex, doorStats in enumerate(room.doors):
                #         if doorStats[-1] == "Open":



                    #for door in room.doors:
                    #    oddsForEachRoom.append(50)

                    # Since it's a 2d map from left to right only, rooms to left & right have a 50/50 chance of 'catching' the fire.
                    # If door is open for any reason, that room has a 80% of 'catching' the fire.
                    # If doors on both sides are open, revert back to 50/50. Chances are reduced by level of doors.
                    pass

                


    # -- You won -- #
    if enemyShip.destroyed == True: 
        print("\n%s has been destroyed! Well done. Precluding combat." % (enemyShip.name) )
        break
        # Earn rewards
    elif len(enemyShip.crew) == 0 and enemyShip.auto_ship == False:
        print("\nAll enemy crew aboard %s have died! Precluding combat." % (enemyShip.name) )
        break
        # Earn extra rewards for fully looting ship   
    # -- You lose -- #     
    elif playerShip.destroyed == True: 
        print("\nThe %s has been annihilated... We have failed our mission. Game over." % (playerShip.name) )
        break
        # Game over will occur
    elif len(playerShip.crew) == 0 and len(playerShip.clone_bay_queue) == 0:
        print("\nValiant crew of %s have all fallen... Our ship has been pilfered for unknowable means. Game over." % (playerShip.name) )
        break
        # Game over will occur

    time.sleep(0.12) # This sleep aligns the game time with real time 


print("\n ---------- A.A.R. ----------")
print(f"Combat has finished after %d seconds." % (SECONDS_ELAPSED))
# for crew in playerShip.crew:
#     print("Name: %s | Stun duration: %s" % (crew.name, crew.stats["Stun duration"] ) )

# medbay = playerShip.systems["Medbay"].parentRoom
# print("Medbay oxygen: %d | Medbay power: %d | # of fires: %d " % (medbay.oxygen, medbay.system.power, len(medbay.fires) ) )
# print("Crew and their health: ")
# for allegiance in medbay.crewInRoom:
#     for crew in medbay.crewInRoom[allegiance]:
#         print("Name: %s | Health: %d" % (crew.name, crew.stats["Health"]) )

# for room in enemyShip.rooms:
#     if room.system != "Empty":
#         print("Room's System: %s | Power: %d | Damage: %d " % (room.system, room.system.power, room.system.damage)) 
#     else:
#         print("Room's System: %s ")    

print("\n\n\n-----------------------------------------")
