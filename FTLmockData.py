# List containing weapons in FTL. Format is built around the Weapon class parameters.
## "Name" : ["Type", damage, cooldown, projectiles, powerNeeded, cost] 
## Missing values will be represented by None
weaponsDatabase = { "Basic Laser": ["Laser",1,10,1,1,None],  "Ion Blast": ["Ion",1,8,1,1,10], 
                    "Small Bomb": ["Bomb",2,14,1,1,20],      "Mini Beam": ["Beam",1,10,None,1,None], 
                    "Flak I": ["Flak",1,8,3,2,40]
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