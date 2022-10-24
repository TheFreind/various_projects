# List containing weapons in FTL. Format is built around the Weapon class parameters.
## "Name" : ["Type", damage, cooldown, projectiles, powerNeeded, cost] 
## Missing values will be represented by None
weaponsDatabase = { "Basic Laser": ["Laser",1,10,1,1,20],  "Ion Blast": ["Ion",1,8,1,1,10], 
                    "Small Bomb": ["Bomb",2,14,1,1,20],      "Mini Beam": ["Beam",1,10,1,1,20], 
                    "Flak I": ["Flak",1,8,3,2,40],           "Artemis": ["Missile",2,11,1,1,40],
                    "Burst Laser Mk II": ["Laser",1,12,3,2,60]
                }

startingWeapons = {
    "Kestral": ["Burst Laser Mk II", "Artemis"],
}

# Maybe make it proper 2d and not 1d?
roomsDatabase = {
    # Kestral Layout - [Small empty(vent)][Big Engines][small O2][big weapons][big shields][small doors(vent)][big medbay][small sensors][small cockpit]
    "Kestral": [ [2,"Empty",2],[4,"Engines",0],[2,"Oxygen",0],[4,"Weapons",0],[4,"Shields",0],
                 [2,"Doors",2],[4,"Medbay",0],[2,"Sensors",0],[2,"Piloting",0] ],
    "Rebel Fighter": [  [4,"Weapons",0],[4,"Engines",0],[4,"Shields",0],[2,"Medbay",0],
                        [2,"Empty",0],[2,"Oxygen",0],[2,"Piloting",0] ],
    "Auto Assault": [ [4,"Weapons",0],[4,"Engines",0],[4,"Shields",0] ]
    }


# Database of Weapon objects in FTL (converted to Tuple later). Info imported from ..Data.py weaponsDatabase  
weaponsCollection = []

systemsCollection = ("Piloting", "Engines", "Weapons", "Shields", "Oxygen", "Medbay", "Clone Bay", "Drone Control",
                "Backup Battery", "Doors", "Sensors", "Hacking", "Mind Control", "Cloaking", "Teleporter")

encounterShipsCollection = ("Slug Interceptor", "Auto Scout", "Auto Assault", "Rebel Fighter")

playableShipsCollection = ("Kestral", "Nissan", "Osprey", "Red-Tail") # Fill this up later


