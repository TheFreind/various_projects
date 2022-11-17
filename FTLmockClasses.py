## ------- DIRECTORY
## 17  | Ship
## 109 | Weapon
## 165 | Room
## 187 | System
## 222 | Drone
## 230 | Crew
##
##
##




from random import randint, choice
from math import floor

class Ship(object):
    destroyed = False
    auto_ship = False
    cloaked = False

    shields = 0
    shield_recharge_progress = 0
    shield_recharge_speed = 3 # Determined by manning crew, etc. Constant set to 3 seconds for now.
    evasion = 0
    oxygen = 100

    # Might need to add "rooms" parameter
    def __init__(self, name, playableShipsCollection):
        self.name = name
        

        self.weapons = {}
        self.systems = {}
        self.crew = []
        self.augments = []
        self.rooms = []
        self.storage = []

        if name in playableShipsCollection:
            self.hull = 30
            self.missiles = 12      # Missiles imported from Data
            self.drone_parts = 0    # Ditto
            self.reactor = 8        # Ditto
            self.isPlayer = True
        else:
            self.hull = randint(5, 15) # Should be bigger for bigger ships
            self.missiles = randint(5, 10)
            self.drone_parts = randint(4, 8)
            self.isPlayer = False

    def __repr__(self):
        return self.name

    def grantStartingWeapons(self, playableShipsCollection, startingWeapons, weaponsCollection):
        if self.name in playableShipsCollection:           # Find weapons for a player's ship and add them to the dict .weapons 
            for desire in startingWeapons[self.name]: 
                for gun in weaponsCollection:                
                    if desire == gun.name:                      
                        self.weapons[gun.name] = gun
                        break

        #else enemy encounter weaponry

    # So long as the ship has shields, that it has at least 2 power, and that it currently has less
    #   shield bubbles than its maximum, start rejuvenating them. 
    def rejuvenateShield(self, shieldClass): # Check if Ship has shields within the main code...
        shieldLayerRechargeTime = [2, 2, 1.75, 1.5, 1.33]
        crewMateSkillList = [1.10, 1.20, 1.30]
        if self.systems["Shields"].manned == True:
            crewBonus = crewMateSkillList[self.systems["Shields"].mannedCrewMate.experience_skills["Shields"][0]]
        else:
            crewBonus = 1
        rechargeBooster = 1 # ! Shield Charge Booster augments is additive to this variable
        
        timeNeeded = shieldLayerRechargeTime[self.shields-1] * (1/crewBonus*rechargeBooster) 


        if shieldClass.power >= 2:
            
            if (self.shield_recharge_progress < timeNeeded and self.shields < floor(shieldClass.power / 2) ): 
                self.shield_recharge_progress += 1

            elif self.shields < floor(shieldClass.power / 2): 
                self.shields += 1
                self.shield_recharge_progress = 0

    # Update and check if evasion changes. 
    def checkEvasion(self, pilotingRoom, enginesRoom):
        if self.isPlayer == True:
            my_crew = "friendly"
        else:
            my_crew = "hostile"

        if self.cloaked == True:
            cloakEvasion = 60
        else:
            cloakEvasion = 0

        dodgeFromEngines = [0, 5, 10, 15, 20, 25, 28, 31, 35]
        dodgeFromCrewLevel = [5, 7, 10]
        autoPilotDodgeMultiplier = [0, 0, 0.5, 0.8] # Piloting power = index accesed from this. Or 1 if there is pilot.

        # ! Once I add AI adjutants, consider them as crew. Rework code below when I implement adjutants.

    # Auto-Ships are always "crewed." Consider piloting to be manned for autoPilotDodge purposes.
        if self.auto_ship == True:
            autoPilotDodgeMultiplier = 1
    # If piloting has a pilot, and it has power, give maximum evasion.
        elif pilotingRoom.system.manned == True and pilotingRoom.system.power > 0:
            autoPilotDodgeMultiplier = 1
    # If you have crew in your piloting, and it has power. Have evasion but no manned bonus.
        elif len(pilotingRoom.crewInRoom[my_crew]) > 0 and pilotingRoom.system.power > 0:
            autoPilotDodgeMultiplier = 1
    # No crew/manning pilot. Engage auto-pilot. 
        elif len(pilotingRoom.crewInRoom[my_crew]) == 0 and pilotingRoom.system.power >= 2:
            autoPilotDodgeMultiplier = autoPilotDodgeMultiplier[self.systems["Piloting"].power] 
    # No crew/manning pilot. No auto-pilot (lvl 2/3 piloting). System damaged.
        else:
            autoPilotDodgeMultiplier = 0

        # Provide bonuses to evasion from crew manning Piloting and Engineering. Based on skill level.
        if pilotingRoom.system.manned == True:
            dodgeFromPiloting = dodgeFromCrewLevel[pilotingRoom.system.mannedCrewMate.experience_skills["Piloting"][0]]
        else:
            dodgeFromPiloting = 0            
        if enginesRoom.system.manned == True:
            dodgeFromEngineering = dodgeFromCrewLevel[enginesRoom.system.mannedCrewMate.experience_skills["Engines"][0]]
        else:
            dodgeFromEngineering = 0

        # Evasion = (Power in engines + crew in Pilots/Engines) * Multiplier from auto-pilot + cloak evasion
        self.evasion = (dodgeFromEngines[enginesRoom.system.power] + dodgeFromPiloting + dodgeFromEngineering)*autoPilotDodgeMultiplier + cloakEvasion

    # Needs more work
    def fireWeapon(self, gun, target):
        print(f'{gun} is firing at {target}!')
        # Choose room, hit shields, miss shots, damage system, damage crew, etc...
        # Enter targetting room. This here is just random room selection.
        
    # Suggestion: Make AI more likely to target high-value systems.
        for shot in range(gun.projectiles):
            if self.systems["Weapons"].manned == True:
                target.systems["Weapons"].mannedCrewMate.earnXP("Weapons") 

            room_targetted = choice(target.rooms) 
            roll_to_hit = randint(1, 100)
            if target.evasion > roll_to_hit and gun.type != "Beam":     # Beams cannot miss
                print("-- MISS!")
                # Crewmembers get XP for dodging
                if target.systems["Piloting"].manned == True:
                    target.systems["Piloting"].mannedCrewMate.earnXP("Piloting") 
                if target.systems["Engines"].manned == True:
                    target.systems["Engines"].mannedCrewMate.earnXP("Engines") 
                                
            else:
            ## Now evaluate what happens to the shields ##
                shieldsPenetrated = False
                damageDone = 0
                #print("Gun type:", gun.type)
                #print("Target shields:", target.shields)

                if gun.type == "Beam":
                    if (gun.damage - target.shields) * gun.beam_length > 0:
                        shieldsPenetrated = True
                    damageDone = (gun.damage - target.shields) * gun.beam_length
                else:
                    if target.shields > 0:
                        if gun.type == "Ion":
                            # Add ion damage to shields system
                            pass#

                        elif gun.type != "Missile" and gun.type != "Bomb": # If not a bomb and missile type, projectile hits shield 
                            target.shields -= 1
                            print("-- Shield hit!")#
                            if target.systems["Shields"].manned == True:
                                target.systems["Shields"].mannedCrewMate.earnXP("Shields") 

                        else:
                            shieldsPenetrated = True
                            damageDone = gun.damage

                    elif target.shields == 0:
                        shieldsPenetrated = True
                        damageDone = gun.damage

                if shieldsPenetrated == True:
                    if room_targetted.system != "Empty": # System damage done, shift power level
                        room_targetted.system.damage += damageDone         
                        room_targetted.system.determineDamage()

                    for allegiance in room_targetted.crewInRoom:    # Crew damage applied to all crew in room
                        for crew in room_targetted.crewInRoom[allegiance]:
                            crew.sufferDamage(gun.crew_damage, gun)

                    roll_to_add_fire = randint(1, 100)
                    roll_to_add_breach = randint(1, 100)
                    roll_to_stun = randint(1, 100)

                    if roll_to_add_fire <= gun.fire_chance: 
                        room_targetted.startFire("Weapon", gun.name)

                    if roll_to_add_breach <= gun.breach_chance and len(room_targetted.breaches) < room_targetted.size:
                        room_targetted.breaches.append(10)
                        print("-! Hull breached!")
                    
                    if roll_to_stun <= gun.stun_chance:
                        if len(room_targetted.crewInRoom) > 0: # Notification. Could be refined further.
                            if len(room_targetted.crewInRoom["friendly"]) > 0:
                                namesFoundFriendly = "  FRIENDLIES: "
                                for crew in room_targetted.crewInRoom["friendly"]:
                                    namesFoundFriendly += crew.name + " | "
                                print(namesFoundFriendly + "have been stunned!")
                            if len(room_targetted.crewInRoom["hostile"]) > 0:
                                namesFoundHostile = "  HOSTILES: "
                                for crew in room_targetted.crewInRoom["hostile"]:
                                    namesFoundHostile += crew.name + " | "
                                print(namesFoundHostile + "have been stunned!")


                        for allegiance in room_targetted.crewInRoom:
                            for crew in room_targetted.crewInRoom[allegiance]:
                                crew.stats["Stun duration"] += gun.stun_duration


                if damageDone > 0:
                    target.hull -= damageDone
                    print(f"-- Target room: {room_targetted.system} | {target}'s Hull: {target.hull}") # Debugging

                if target.hull <= 0:
                    target.destroyed = True


        gun.charge = 0
        if gun.type == "Missile" or gun.type == "Bomb":
            self.missiles -= 1






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

            if type == "Laser" or type == "Beam" or type == "Missile":       # Side effects dependent on weapon type. Chances represented in percentages. 
                self.fire_chance = 10                       # However, it needs to be more refined.
            if type == "Laser" or type == "Missile":
                self.breach_chance = 10
            if type == "Missile":
                self.stun_chance = 20
                self.stun_duration = 5  # ! Each weapon has different stun duration. E.G. Stun bomb is 15 seconds.
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
    def __init__(self, size, system, vents, parentShip):
        self.size = size
        self.system = system
        self.vents = vents
        self.oxygen = 100
        self.parentShip = parentShip

        self.crewInRoom = {
            "friendly": [],
            "hostile":    []
            }

        self.doors = []     # Each door has a level, health, and Open/Closed status 
        self.breaches = []  # List containing health of each breach. # of breaches is len of the list.  
        self.fires = []     # Ditto
        self.fireProgress = 0   # Every fire in room increments progress to start another fire in the room
        self.fireChance = 0     # Random range from 12-18. A fire will occur when progress matches this chance
        self.fireJumpChance = 0 # A fire has a chance to spread to a nearby room. fireProgress contributes to this

    def __repr__(self):
        return self.system.name


    # function to add fires
    def startFire(self, method, perpetuator):
        if len(self.fires) < self.size:         # Max fires = Size of room
            self.fireChance = randint(12, 18)
            self.fires.append(40)

            if method == "Weapon":
                print("-! Fire started from a %s shot!" % (perpetuator) )
            elif method == "Spread":
                print("-! Fire is spreading in %s!" % (self.system))
            elif method == "Jump":
                print("-! Fire has now jumped to %s!" % () )


    # function to add breaches
    #### Ensure # of fires and # of breaches do NOT exceed room size


class System(object):
    power = 1               # Amount of power in system
    systemLevel = 2         # Current Upgraded level of System. Can take up to this much power
    systemPowerMemory = 1   # When systems are damaged/ionized, they'll automatically be re-powered to their intended power
    repairProgress = 0      # Crew repair progress will restore 1 power bar when >= 10. Reset if room empty of friendlies.
    damageProgress = 0      # Intruders and fire damage systems. 1 system damage when >= 10. Reset if room empty of hostiles. DONOT reset if fire present.
    damage = 0              # Damage to system prevents power intake to the system.
    ion_damage = 0
    parentRoom = ""         # System has access to the Room object that it resides in.

    def __init__(self, name, startingSystemLevel, maxUpgradeableLevel):
        mannableSystems = ["Piloting", "Shields", "Weapons", "Engines", "Sensors", "Doors"]

        self.name = name
        self.systemLevel = startingSystemLevel      
        self.maxUpgradeableLevel = maxUpgradeableLevel

        if self.name in mannableSystems:
            self.manned = False
            self.mannedCrewMate = ""
        else:
            self.manned = "Not possible"


    def __repr__(self):
        return self.name

    # When a system takes damage, reduce its power by damage. If system is fixed, restore power as necessary.
    # ! System blasted may be entirely unnecessary  
    #def determineDamage(self, shipClass, systemBlasted):
    def determineDamage(self):
        self.power = self.systemPowerMemory - self.damage - self.ion_damage       # ! Wait... how does ion damage work with actual damage?
        if self.power < 0:  # Cannot have negative power in a system
            self.power = 0
        if self.damage > self.systemLevel: # Cannot have more damage in a system than its system level
            self.damage = self.systemLevel

        # Is this necessary at all? I think it can be included in rejuvenate shields
        ## if systemBlasted.name == "Shields":
        ##     shipClass.shields = floor(systemBlasted.power / 2)

        # Rightmost-powered weapon starts charging down at -2 charge/sec
        #if systemBlasted.name == "Weapons": 
        #    pass 

        # etc for other systems

    # A system will lose all repair/damage progress if all friendlies/hostiles leave the room before fixing/destroying the system.
    # Exception - Fires will prevent damage reset because they are actively damaging the system.
    def checkCrewPresence(self, room):
        if len(room.fires) == 0:
            if ((len(room.crewInRoom["friendly"]) == 0 and room.parentShip.isPlayer == True) or
                (len(room.crewInRoom["hostile"]) == 0 and room.parentShip.isPlayer == False) ):
                room.system.repairProgress = 0
            if ((len(room.crewInRoom["friendly"]) == 0 and room.parentShip.isPlayer == False) or
                (len(room.crewInRoom["hostile"]) == 0 and room.parentShip.isPlayer == True) ):
                room.system.damageProgress = 0
 

    # powerUp and powerDown are for when the player manually increases or decreases power in a system
    def powerUp(self):
        if self.power < self.systemLevel:
            self.power += 1
            self.systemPowerMemory = self.power
        else:
            print("\nNOTE: System is at maximum power. Cannot inject any more power!")

    def powerDown(self):  
        if self.power > 0:
            self.power -= 1
            self.systemPowerMemory = self.power
        else:
            print("\nNOTE: Cannot power down a system at 0 power.")


    # ! Big exception! Medbay hacking must not only stop medbay healing, but cause damage
    # Medbays heal for 1x / 1.5x / 3x depending on level. Healing at lvl 1 is 6.4 hp/sec
    def medbayHeal(self, crewObject):
        if self.power > 0:  # Is Medbay powered?
            # Friendly medbay heals friendly crewmembers; or enemy medbay heals enemies
            if ( (self.parentRoom.parentShip.isPlayer == True and crewObject.stats["Allegiance"] == "friendly") or 
                (self.parentRoom.parentShip.isPlayer == False and crewObject.stats["Allegiance"] == "hostile" )):
                medbayHealingModifier = [0, 1, 1.5, 3]
                crewObject.stats["Health"] += 6.4 * medbayHealingModifier[self.power]


# Types: Ship drone, Boarding drone, attack drone, defense drone
# ! Make Boarding and Ship drones a subclass of Crew.
class Drone(object):
    health = 100

    def __init__(self, name, type):
        self.name = name
        self.type = type

class Crew(object):
    # Variables defined in __init__ --> [self.name, self.species, self.location, self.locationIndex, self.destinationIndex]
    movementProgress = 0
    combat_target_cycle = 0  # If not brawling directly in combat, attack an enemy on this tile. Cycle through all enemies.

    def __init__(self, species, shipOnboard, crewNameDatabase):
        self.name = choice(crewNameDatabase) # Name should be dependent on species
        self.species = species
        self.shipOnboard = shipOnboard  # Which ship is this crewmember on?
        shipOnboard.crew.append(self)   # Add this crewmember to Ship's crew list

        self.experience_skills = {   # Current Level 0/2, Current XP, XP needed to level up
            "Piloting":     [0, 0, 15],
            "Engines":      [0, 0, 15],
            "Shields":      [0, 0, 55],
            "Weapons":      [0, 0, 65],
            "Fighting":     [0, 0, 8],
            "Repairing":    [0, 0, 18],
        }
        self.stats = {
            "Allegiance": "friendly",
            "Health": 100,                      # Rock, Crystal, Zoltan, Drones
            "maxHealth": 100,
            "Damage": 1,                # Random damage modifier. 0.5 for Engi, 1.5 for Mantis
            "Repair speed": 1,                  # Engi, Mantis, Repair Drone
            "Stun duration": 0,
            "Movement speed": 1,                # Mantis, Rock, Lanius, Crystal, Drones
            "Fire fighting speed": 4,           # Mantis=0.5 | Crystal=0.83 | Rock=1.67 | Engi=2
            "Suffocation damage": 1,            # Crystal=0.5 | Lanius=0 | Drones=0
            "Store cost": 45,                   # Depends on species
            #"Crew Rarity": 1,                  # Rarity dependent on sector
        # -- ABILITIES -- # 
            "Zoltan power": False,              # Zoltan
            "Death explosion": False,           # Zoltan
            "Telepathy": False,                 # Slug revealing nearby rooms
            "Mind control immunity": False,     # Slug, Drones
            "Fire immunity": False,             # Rock, Drones
            "Drains oxygen": False,             # Lanius
            "Lockdown ability": False           # Crystal
            #"Regenerates oxygen": False        # AEGIS Drone (from my own ideas)
        }

        self.generateCrew(species, shipOnboard) # Set starting stats dependent on species
        self.spawnLocation(shipOnboard, shipOnboard.isPlayer) # Find starting location

    def __repr__(self):
        return "%s | %s > %s" % (self.name, self.species, self.location)


  # Set starting stats dependent on species.
    def generateCrew(self, species, parentShip):

        if parentShip.isPlayer == False:
            self.stats["Allegiance"] = "hostile"


        if species == "Human":
            for skill in self.experience_skills: # 10% Lower XP needed to level up
                self.experience_skills[skill][2] = float(self.experience_skills[skill][2])   # To be reduced by 10%, it must be converted into a floating number
                self.experience_skills[skill][2] = floor(self.experience_skills[skill][2]*0.9) 
                self.experience_skills[skill][2] = int(self.experience_skills[skill][2])     # Re-convert back to integer
        elif species == "Engi":
            self.stats["Store cost"] = 50
            self.stats["Damage"] = 0.5
            self.stats["Repair speed"] = 2
            self.stats["Fire fighting speed"] = 2
        elif species == "Zoltan":
            self.stats["Store cost"] = 60
            self.stats["Health"] = 70
            self.stats["maxHealth"] = 70
            self.stats["Zoltan power"] = True
            self.stats["Death explosion"] = True
        elif species == "Rockman":
            self.stats["Store cost"] = 55
            self.stats["Health"] = 150    
            self.stats["maxHealth"] = 150
            self.stats["Movement speed"] = 0.5
            self.stats["Fire fighting speed"] = 1.67
            self.stats["Fire immunity"] = True       
        # elif species == "Mantis"
        # elif species == "Lanius"
        # elif species == "Slug"
        # elif species == "Crystal"  
        # elif species == "Boarding Drone" / "Repair Drone" / "Ion Intruder" / "Anti-Personnel Drone"          


  # Spawn crewmember in piloting if your ship; pre-determined important systems if hostile. 
    def spawnLocation(self, parentShip, isPlayer):
        # Spawn in piloting. If full, try room adjacent to the left.
        if isPlayer == True:
            for index in range( len(parentShip.rooms)-1 , 0, -1):
                room = parentShip.rooms[index]
                if len(room.crewInRoom["friendly"]) < room.size: # If the room isn't full, spawn there
                    self.location = room
                    self.locationIndex = index
                    room.crewInRoom["friendly"].append(self)
                    self.roomPositionIndex = len(room.crewInRoom["friendly"]) - 1
                    self.destinationIndex = self.locationIndex
                    break
            else:
                print("DEBUG ERROR - Could not find a room for %s!" % (self.name))


        elif isPlayer == False:
            # When spawning in a ship, attempt to spawn at least 1 crew in these rooms, in this priority
            spawnRoomPriority = ["Piloting", "Weapons", "Shields", "Engine", "Medbay", "Teleporter"]       
            for roomPriority in spawnRoomPriority:
                index = 0

                if roomPriority not in parentShip.systems: # If room does not exist, skip to next check
                    continue
                for roomIndex, checkingShipRoom in enumerate(parentShip.rooms):
                    if checkingShipRoom.system != "Empty" and checkingShipRoom.system.name == roomPriority:
                        room = checkingShipRoom
                        index = roomIndex

                if len(room.crewInRoom["hostile"]) == 0: # If the room is empty, spawn there
                    self.location = room
                    self.locationIndex = index
                    room.crewInRoom["hostile"].append(self)
                    self.roomPositionIndex = len(room.crewInRoom["hostile"]) - 1
                    self.destinationIndex = self.locationIndex
                    break
            else:   
                print("\n! PROBLEM - Could not find a room for this crew to spawn in!\n")
                # Try randomizing room index spawn location for this.


    def moveAction(self):
        self.movementProgress += self.stats["Movement speed"]

        while self.movementProgress >= 1:
            self.movementProgress -= 1

            # Exit room, go to right/Left room and change current location, enter room
            self.shipOnboard.rooms[self.locationIndex].crewInRoom[self.stats["Allegiance"]].remove(self)
            
            if self.locationIndex < self.destinationIndex: # Move Right
                self.locationIndex += 1
            elif self.locationIndex > self.destinationIndex: # Move Left
                self.locationIndex -= 1

            self.location = self.shipOnboard.rooms[self.locationIndex]
            self.shipOnboard.rooms[self.locationIndex].crewInRoom[self.stats["Allegiance"]].append(self)
            self.roomPositionIndex = len(self.location.crewInRoom[self.stats["Allegiance"]]) - 1

        # Potential bug - what happens when you reach your location with leftover movement?
        #   i.e. Mantis/Mantis pheromones providing that
        # I believe the bug has been fixed. Delete comment when confirmed.

        if self.locationIndex == self.destinationIndex: # Notification of arrival to destination
            print(f" [% {self.name} has arrived in {self.location}.")


    def evaluateTask(self):
        # Always fight enemy crewmembers. This takes precedence over any other task.
        if ( (self.stats["Allegiance"] == "friendly" and len(self.location.crewInRoom["hostile"]) > 0) or 
            (self.stats["Allegiance"] == "hostile" and len(self.location.crewInRoom["friendly"]) > 0) ):
            self.combatAction()

        # If present in enemy system, start destroying it. You cannot trash a completely destroyed system!
        elif ( self.location.system.name != "Empty" and self.location.system.damage < self.location.system.systemLevel and
                (self.location.parentShip.isPlayer == False and self.stats["Allegiance"] == "friendly" or
                self.location.parentShip.isPlayer == True and self.stats["Allegiance"] == "hostile") ):
            self.destroySystemAction()
            
        # If room has fires, firefight. Only extinguish fires on your own ship.
        elif ( len(self.location.fires) > 0 and 
                (self.location.parentShip.isPlayer == True and self.stats["Allegiance"] == "friendly" or
                self.location.parentShip.isPlayer == False and self.stats["Allegiance"] == "hostile") ):
            self.firefightingAction()

        # If room has breaches, repair them. Only repair breaches on your own ship.
        elif ( len(self.location.breaches) > 0 and 
                (self.location.parentShip.isPlayer == True and self.stats["Allegiance"] == "friendly" or
                self.location.parentShip.isPlayer == False and self.stats["Allegiance"] == "hostile") ):
            self.repairBreachAction()

        # If room's system is damaged, repair it. Only repair friendly systems.
        elif ( self.location.system.damage > 0 and 
                (self.location.parentShip.isPlayer == True and self.stats["Allegiance"] == "friendly" or
                self.location.parentShip.isPlayer == False and self.stats["Allegiance"] == "hostile") ):
            self.repairSystemAction()

        #elif needtoreposition
            #print("DEBUGGING - Reposition to man system / fight boarder")

        # If room can be manned and it's not manned, man it. Only man friendly systems.
        elif ( self.location.system.manned == False and 
                (self.location.parentShip.isPlayer == True and self.stats["Allegiance"] == "friendly" or
                self.location.parentShip.isPlayer == False and self.stats["Allegiance"] == "hostile") ):
            self.location.system.manned = True
            self.location.system.mannedCrewMate = self

        # Else, idle.


    def combatAction(self):
        self.unmanSystemAction()
        me = self.stats["Allegiance"]
        if me == "friendly":
            them = "hostile"
        elif me == "hostile":
            them = "friendly"

        numEnemies = len(self.location.crewInRoom[them])

        if (self.roomPositionIndex) + 1 > numEnemies:
            #print("DEBUGGING - I'm all alone, I should be attacking someone!")
        # Attack enemies in clockwise order once each before repeating cycle
            if self.combat_target_cycle < numEnemies:
                combat_target = self.location.crewInRoom[them][self.combat_target_cycle]
                self.combat_target_cycle += 1

            elif self.combat_target_cycle == numEnemies:
                self.combat_target_cycle = 0
                combat_target = self.location.crewInRoom[them][self.combat_target_cycle]
                self.combat_target_cycle += 1                

        else:
            combat_target = self.location.crewInRoom[them][self.roomPositionIndex] # Fight in same tile

        dealingDamage = randint(4, 8) * self.stats["Damage"]
        combat_target.sufferDamage(dealingDamage, self)

        

    def destroySystemAction(self):
        self.location.system.damageProgress += 1 # All crew deal equal system damage

        if self.location.system.damageProgress >= 10: # When system accumulates enough damage, damage a power bar.
            self.location.system.damage += 1
            self.location.system.determineDamage()
            self.location.system.damageProgress = 0

            self.earnXP("Fighting")
            
            if self.location.system.damage == self.location.system.systemLevel:
                self.location.parentShip.hull -= 1
                print(" [! %s of %s has been destroyed by boarders!" % (self.location.system.name, self.location.parentShip.name) )

        
    def repairSystemAction(self):
        # What happens to the system's power when repaired?
        self.unmanSystemAction()
        self.location.system.repairProgress += self.stats["Repair speed"]

        if self.location.system.repairProgress >= 10: # When system accumulates enough repair, repair a power bar.
            self.location.system.damage -= 1
            self.location.system.determineDamage()
            self.location.system.repairProgress = 0

            # Earn XP
            self.earnXP("Repairing")
            
            # Fully repaired notification
            if self.location.system.damage == 0 and self.location.parentShip.isPlayer == True: 
                print(" {+ %s is fully repaired." % (self.location.system.name) )
            elif self.location.system.damage == 0 and self.location.parentShip.isPlayer == False:
                print(" {- Enemy %s is fully repaired." % (self.location.system.name) )
        
    
    def repairBreachAction(self):
        self.unmanSystemAction()
        self.location.breaches[0] -= self.stats["Repair speed"] # First breach in list 'loses' health at the rate of repair speed.

        if self.location.breaches[0] <= 0: 
            del self.location.breaches[0]   # Breaches don't 'move' tiles. They stay where they are. Change?

            # Earn XP
            self.earnXP("Repairing")
            
            # All breaches repaired notification
            if len(self.location.breaches) == 0 and self.location.parentShip.isPlayer == True:
                print(" {+ All breaches in %s are repaired." % (self.location.system.name) )


    def firefightingAction(self):
        self.unmanSystemAction()
        self.location.fires[0] -= self.stats["Fire fighting speed"] # First fire in list 'loses' health at the rate of fire fighting speed.

        if self.location.fires[0] <= 0: 
            del self.location.fires[0]
            
            # If all fires in a room are extinguished, check to see if all fires on ship are extinguished. Notification if so.
            if len(self.location.fires) == 0 and self.location.parentShip.isPlayer == True:
                print(" {+ All fires in %s are depleted." % (self.location.system.name) )
                firesFound = 0
                for room in self.location.parentShip.rooms:
                    firesFound += len(room.fires)
                    if firesFound > 0:
                        break

                else:
                    print(" {+ All fires onboard %s have been extinguished!" % (self.location.parentShip.name) )        

    # Doing any action will force the crewmember to unman the system, if it is mannable to begin with.
    def unmanSystemAction(self):
        if self.location.system.manned != "Not possible" and self.location.system.manned == True:
            self.location.system.manned = False
            self.location.system.mannedCrewMate = ""

    # Crewmember takes damage. They die, and are deleted, when health reaches 0.
    def sufferDamage(self, damage, source):
        self.stats["Health"] -= damage
        #print("DEBUGGING - %s has taken %d damage. Health now: %d" % (self.name, damage, self.stats["Health"]) )
        if self.stats["Health"] <= 0:
            if self.stats["Allegiance"] == "friendly":
                print("!! [%s | %s] has died!" % (self.name, self.species) )

            # If source of death was from crew combat, killer gains XP.
            if isinstance(source, Crew):
                source.earnXP("Fighting")

            for i, person in enumerate(self.shipOnboard.crew):
                if person.name == self.name:
                    del self.shipOnboard.crew[i]
                    #print(self.shipOnboard.crew)
            for i, person in enumerate(self.location.crewInRoom[self.stats["Allegiance"]]):
                if person.name == self.name:
                    del self.location.crewInRoom[self.stats["Allegiance"]][i]

            del self


    def earnXP(self, whatSkill):
        if self.experience_skills[whatSkill][0] < 2:    # Do not earn XP if max level already
            self.experience_skills[whatSkill][1] += 1
            print("DEBUGGING - %s has earned XP toward %s." % (self.name, whatSkill) )
            if self.experience_skills[whatSkill][1] >= self.experience_skills[whatSkill][2]:
                self.experience_skills[whatSkill][0] += 1
                self.experience_skills[whatSkill][1] = 0
                print(" [+ %s has leveled up in %s!" % (self.name, whatSkill) )

                if whatSkill == "Fighting":
                    self.stats["Damage"] += 0.1
                elif whatSkill == "Repairing":
                    self.stats["Repair speed"] += 0.1
                    self.stats["Fire fighting speed"] += 0.1