# List containing weapons in FTL. Format is built around the Weapon class parameters.
## "Name" : ["Type", damage, cooldown, projectiles, powerNeeded, cost] 
## Missing values will be represented by None
weaponsDatabase = { "Basic Laser": ["Laser",1,10,1,1,20],  "Burst Laser Mk II": ["Laser",1,12,3,2,60], 
                    "Small Bomb": ["Bomb",2,14,1,1,20],      "Mini Beam": ["Beam",1,10,1,1,20], 
                    "Flak I": ["Flak",1,8,3,2,40],           "Artemis": ["Missile",2,11,1,1,40],
                    "Ion Blast": ["Ion",1,8,1,1,10]
                }

# [Weapons], [Drones], [Systems], [SystemsStartingLevel], [crew], [augmentations], 
# [Fuel/Missile/Drones/Reactor], maxWeapons and maxDrones...
startingGear = {
    # -- PLAYER SHIPS -- #
    "Kestral": [ ["Burst Laser Mk II", "Artemis"], [""], ["Shields","Engines","Weapons","Oxygen",
                    "Medbay","Doors","Sensors","Piloting"], [2, 2, 3, 1, 1, 1, 1, 1], 
                    ["Human", "Human", "Human"], [], [16, 12, 0, 8], 4, 2],
    # -- ENEMY SHIPS -- #
    "Rebel Fighter": [ ["Basic Laser", "Artemis"], [""], ["Shields","Engines","Weapons","Oxygen",
                    "Medbay","Piloting"], [2, 2, 3, 1, 1, 1], 
                    ["Human", "Human", "Human"], [], 4, 2],
}

# Maybe make it proper 2d and not 1d?
## "Name of Ship" : [ [Size of room, System within room, # of vents], etc...  ]
roomsDatabase = {
    "Kestral": [ [2,"Empty",2],[4,"Engines",0],[2,"Oxygen",0],[4,"Weapons",0],[4,"Shields",0],
                 [2,"Doors",2],[3,"Medbay",0],[2,"Sensors",0],[2,"Piloting",0] ],
    "Rebel Fighter": [  [4,"Weapons",0],[4,"Engines",0],[4,"Shields",0],[2,"Medbay",0],
                        [2,"Empty",0],[2,"Oxygen",0],[2,"Piloting",0] ],
    "Auto Assault": [ [2,"Weapons",0],[2,"Drone Control",0],[2,"Piloting",0],[2,"Engines",0],[2,"Shields",0] ]
    }

## "Name of System" : maxLevel
systemsDatabase = { 
    "Shields": 8, "Engines": 8, "Weapons": 8, "Drone Control": 8,  
    "Teleporter": 3, "Cloaking": 3, "Mind Control": 3, "Artillery Beam": 4,
    "Flak Artillery": 4, "Hacking": 3, "Oxygen": 3, "Medbay": 3, "Clone Bay": 3,
    "Piloting": 3, "Sensors": 3, "Doors": 3, "Backup Battery": 2
}



# Database of Weapon objects in FTL (converted to Tuple later). Info imported from ..Data.py weaponsDatabase  
weaponsCollection = []

#systemsCollection = ("Piloting", "Engines", "Weapons", "Shields", "Oxygen", "Medbay", "Clone Bay", "Drone Control",
#                "Backup Battery", "Doors", "Sensors", "Hacking", "Mind Control", "Cloaking", "Teleporter")

encounterShipsCollection = ("Slug Interceptor", "Auto-Scout", "Auto-Assault", "Rebel Fighter")

enemyAutoShips = ("Auto-Scout", "Auto-Assault")

playableShipsCollection = ("Kestral", "Nissan", "Osprey", "Red-Tail") # Fill this up later

# Change this to be a dictionary with different species as its key
crewNameDatabase = ("Jeff", "Ivan", "Katherine", "Raven", "Zach", "Ainsley", "Sasha", "Kaladin",
                "Lexica", "Koloianov", "Berk", "Justeen", "Dillonovich", "Sonaki", "Falon", "Ihan",
                "Osiris", "Penn", "Raymond", "Makella", "Charlotte", "Terri") 

