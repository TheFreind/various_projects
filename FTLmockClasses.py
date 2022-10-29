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
    shields = 0
    shield_recharge_progress = 0
    shield_recharge_speed = 3 # Determined by manning crew, etc. Constant set to 3 seconds for now.
    evasion = 15
    oxygen = 100

    # Might need to add "rooms" parameter
    def __init__(self, name, playableShipsCollection):
        self.name = name

        self.weapons = {}
        self.systems = {}
        self.augments = []
        self.rooms = []
        self.storage = []

        if name in playableShipsCollection:
            self.hull = 30
            self.missiles = 12      # ! Import from StartingGear the proper starting missiles
            self.drone_parts = 0    # Ditto
        else:
            self.hull = randint(5, 15) # Should be bigger for bigger ships
            self.missiles = randint(5, 10)
            self.drone_parts = randint(4, 8)

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
        if shieldClass.power >= 2:
            
            if self.shield_recharge_progress < 3 and self.shields < floor(shieldClass.power / 2): 
                self.shield_recharge_progress += 1

            elif self.shields < floor(shieldClass.power / 2): 
                self.shields += 1
                self.shield_recharge_progress = 0


    # Needs more work
    def fireWeapon(self, gun, target):
        print(f'{gun} is firing at {target}!')
        # Choose room, hit shields, miss shots, damage system, damage crew, etc...
        # Enter targetting room. This here is just random room selection.
        
    # Suggestion: Make AI more likely to target high-value systems.
        for shot in range(gun.projectiles):
            room_targetted = choice(target.rooms) 
            roll_to_hit = randint(1, 100)
            if target.evasion > roll_to_hit and gun.type != "Beam":     # Beams cannot miss
                print("-- MISS!")
            else:
            ## Now evaluate what happens to the shields ##
                shieldsPenetrated = False
                damageDone = 0
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

                        else:
                            shieldsPenetrated = True
                            damageDone = gun.damage

                    elif target.shields == 0:
                        shieldsPenetrated = True
                        damageDone = gun.damage

                if shieldsPenetrated == True:
                    if room_targetted.system != "Empty": # System damage done, shift power level
                        room_targetted.system.damage += damageDone         
                        room_targetted.system.determineDamage(target, room_targetted.system)
                    # Crew damage applied to all crew in room
                    roll_to_add_fire = randint(1, 100)
                    roll_to_add_breach = randint(1, 100)
                    #roll_to_stun = randint(1, 100)
                    if roll_to_add_fire <= gun.fire_chance and len(room_targetted.fires) < room_targetted.size: # Max fires = size of room
                        room_targetted.fires.append(40) # Add a 40 health fire to the fire list
                        print("-! Fire started!")
                    if roll_to_add_breach <= gun.breach_chance and len(room_targetted.breaches) < room_targetted.size:
                        room_targetted.breaches.append(40)
                        print("-! Hull breached!")
                    #if roll_to_stun <= gun.stun_chance:
                    #    pass           


                if damageDone > 0:
                    target.hull -= damageDone
                    print(f"-- Target room: {room_targetted.system} | {target}'s Hull: {target.hull}")

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
    power = 2           # Amount of power in system
    systemLevel = 2     # Current Upgraded level of System. Can take up to this much power
    damage = 0
    ion_damage = 0

    def __init__(self, name, maxUpgradeableLevel):
        self.name = name
        self.maxUpgradeableLevel = maxUpgradeableLevel


    def __repr__(self):
        return self.name

    def determineDamage(self, shipClass, systemBlasted):
        self.power = self.systemLevel - self.damage - self.ion_damage       # ! Wait... how does ion damage work with actual damage?
        if self.power < 0:
            self.power = 0

        if systemBlasted.name == "Shields":
            shipClass.shields = floor(systemBlasted.power / 2)

        # Rightmost-powered weapon starts charging down at -2 charge/sec
        #if systemBlasted.name == "Weapons": 
        #    pass 

        # etc for other systems


    def powerUp(self):
        if self.power < self.systemLevel:
            self.power += 1
        else:
            print("\nNOTE: System is at maximum power. Cannot power any further!")

    def powerDown(self):  
        if self.power > 0:
            self.power -= 1
        else:
            print("\nNOTE: Cannot power down a system at 0 power.")




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