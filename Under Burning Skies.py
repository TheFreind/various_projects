## Raven's Birthday gift
# What if Under Falling Skies... but Avatar themed?

import random, time, appaTester

# -- GAME COMPONENTS LEGEND --
# Research Track == Avatar State 
# Research Marker == Aang's Mastery
# Energy Track == Bags (of supplies)
# Energy Marker == Supplies (food, morale, favor, sleep)
# Excavator == Appa (represents distance traveled across the world)
# Damage Track == Hope
# Damage Marker == Devastation
# Mothership tile == The Drill / Admiral Zhang / Firelord Ozai [Dependent on City scenario]
# Purple ships == Fire Nation Forces [List of Fire Nation goons and squadrons thematic to each map]
# White ships == Other Hostile Group [Ditto. Jett and his crew may be one of these hostile groups.]
# White dice == Gaang members doing something and making a revolutionary new idea [List of names]
# Gray dice == Gaang members doing something
# Blue dice == Allies [List of names respective to map]
# Direction Spaces == List of random actions that divert attention. I.E. New Orders, Reinforce Assault, Avatar Rumors Surfaced
# City tiles - represent the major areas, such as Ba Sing Se or the world. Ba Sing Se damaged side = White Lotus Liberators 
#   THE 3 SCENARIOS - Ba Sing Se and Drill / White Lotus Liberation
#                   - The North Water Tribe city and the Fleet / The ebb and flow are captured by Admiral Zhang
#                   - The Whole World and Sozen's Comet / The Last Stand against Phoenix King Ozai 
# AA Guns == Disruption
# Energy Rooms == Respite
# Jet Fighter Rooms == Confrontation
# Research Rooms == Training
# Robot Rooms == Recruitment


# All player commands and inputs must not cause errors. It's also helpful to display an appropriate error message to the user.
# This is a catch-all function that houses all the different validations under one section.
# - inputVar - the input variable that is being checked.
# - task - a string key that tells the function which validation to initiate.
def inputValidation(inputVar, task):

    if task == "Selecting Dice":
        while inputVar.isdigit() == False or int(inputVar) <= 0 or int(inputVar) > len(DICE) or DICE[int(inputVar)-1][-1] != "":
            inputVar = input("Error. You failed to select a die. Try-again:\n")
            

    elif task == "chooseLocationX":
        repeat = True
        locationsChosen = []
        for location in DICE:
            if location[-1] == "":
                locationsChosen.append( False )
            else:
                locationsChosen.append( (location[-1][0][0])+1 )
        
        while repeat == True:
            if inputVar.isdigit() == False:
                inputVar = input("Error. That is not a number! Try-again:\n")

            elif int(inputVar) in locationsChosen: # May not place multiple dice in a column
                inputVar = input("Error. You may not choose a column that has another dice in it! Try-again:\n")

            elif inputVar.isdigit():
                if int(inputVar) <= 0 or int(inputVar) > 5:
                    inputVar = input("Error. That is not a valid X-coordinate for a location. Try-again:\n")
                else:
                    repeat = False
                
            else:
                inputVar = input("Error! Re-try:\n")

    elif task == "chooseLocationY":
        repeat = True
        while repeat == True:
            if inputVar.isdigit() == False:
                inputVar = input("Error. That is not a number! Try-again:\n")
            
            # May not place directly on Appa, or too far ahead of him
            # This condition check is found within the DicePhase function

            elif inputVar.isdigit():
                if int(inputVar) <= 0 or int(inputVar) > 6:
                    inputVar = input("Error. That is not a valid Y-coordinate for a location. Try-again:\n")
                else:
                    repeat = False
                
            else:
                inputVar = input("Error! Re-try:\n")

    
    return inputVar

# When the player does actions, it helps to have feedback on what was done.
#  The randomness of the dialogues creates funny scenarios and moments that are unique with each run.
def dialogue(scenario):

    if scenario == "Confrontation":
        randomGaang = gaangMembers[ random.randint(0, len(gaangMembers)-1 ) ]
        randomVerb = verbsCo[ random.randint(0, len(verbsCo)-1 ) ]
        return randomGaang, randomVerb

    elif scenario == "Raiding":
        randomVerb = verbsCo[ random.randint(0, len(verbsCo)-1 ) ]
        randomObject = raidedObjects[ random.randint(0, len(raidedObjects)-1 ) ]
        return randomVerb, randomObject

    elif scenario == "Distracting":
        randomGaang = gaangMembers[ random.randint(0, len(gaangMembers)-1 ) ]
        randomVerb = verbsDi[ random.randint(0, len(verbsDi)-1 ) ]
        return randomGaang, randomVerb

    elif scenario == "Learning":
        randomLesson = avatarLearning[ random.randint(0, len(avatarLearning)-1 ) ]
        return randomLesson

    time.sleep(1.5)

# All verbs must obey past simple tense grammar
gaangMembers = [ "Aang", "Sokka", "Katara", "Toph", "Momo" ]
verbsCo = ["decimated", "eradicated", "annihilated", "beat the shit out of", "clobbered",
           "discombobulated", "beat", "destroyed", "defeated", "outsmarted", "bodied",
           "blasted", "thrashed", "vibe checked", "K.O.'d" ]
verbsDi = ["distracted", "charmed", "harrassed", "impeded", "mocked", "taunted",
           "sabotaged", "insulted their mother", "failed the PS150 exam of"] 
raidedObjects = ["a Village", "the Outer Wall farms", "a child's lollipop", "several families",
                 "Uncle Iroh's tea", "some bridges", "parts of the Royal Palace", "Zuko's honor",
                 "the Cabbage Dealer", "a cup of lean"]
avatarLearning = ["the secrets of Earthbending", "the secrets of Waterbending", "the secrets of Firebending",
                  "inner peace", "to release all earthly attachments", "the chakra of sound", "the chakra of light",
                  "common sense", "how not to be a simp"]
                  

# BA SING SE, MOST VANILLA CITY
WORLD = [ #[X,Y], Size, Location Type, Thematic name, Supply cost, Dice assigned, Modifier
    # ROW 1 - A
        [ [0,0], 1, "Di", "Disguises", 0, 0, 0], [ [1,0], 1, "Di", "Commander Incapacitated", 0, 0, 0],
        [ [2,0], 1, "Di", "False Avatar Whereabouts", 0, 0, 0], [ [3,0], 1, "Di", "Allied help", 0, 0, 0],
        [ [4,0], 1, "Di", "Distraction", 0, 0, 0],
    # ROW 2
        [ [0,1], 1, "Co", "Pao Family Tea House Scuffle", -1, 0, -1], [ [1,1], 1, "Tr", "Training with Toph", -2, 0, 0],
        [ [2,1], 0, "NU", "NULL", 0, 0, 0],      [ [3,1], 2, "Re", "Earth King's Quarters", 0, 0, -3],
        [ [4,1], 2, "Re", "Earth King's Quarters", 0, 0, -3],
    # ROW 3
        [ [0,2], 1, "Re", "Cabbage Seller", 0, 0, 0], [ [1,2], 2, "Co", "Outer Wall Perimeter", -2, 0, 0],
        [ [2,2], 2, "Co", "Outer Wall Perimeter", -2, 0, 0], [ [3,2], 1, "Tr", "Joo Dee's tour", -1, 0, -1],
        [ [4,2], 0, "NU", "NULL", 0, 0, 0],
    # ROW 4 - B
        [ [0,3], 1, "Tr", "University of Ba Sing Se", 0, 0, -1], [ [1,3], 0, "NU", "NULL", 0, 0, 0],
        [ [2,3], 2, "Tr", "Teachings of the Guru", -2, 0, 0],  [ [3,3], 2, "Tr", "Teachings of the Guru", -2, 0, 0],
        [ [4,3], 1, "Co", "Kyoshi Warrior Infiltration", -2, 0, 0],
    # ROW 5
        [ [0,4], 1, "Co", "Royal Palace", -2, 0, 1], [ [1,4], 1, "Re", "Upper Ring House", 0, 0, 1],
        [ [2,4], 1, "Co", "The Crystal Catacombs", -1, 0, 0], [ [3,4], 0, "NU", "NULL", 0, 0, 0],
        [ [4,4], 1, "Tr", "The Jasmine Dragon", 0, 0, 0],
    # ROW 6
        [ [0,5], 0, "NU", "NULL", 0, 0, 0],   [ [1,5], 3, "Tr", "Lake Laogai", -2, 0, 0],
        [ [2,5], 3, "Tr", "Lake Laogai", -2, 0, 0], [ [3,5], 3, "Tr", "Lake Laogai", -2, 0, 0],
        [ [4,5], 0, "NU", "NULL", 0, 0, 0],
    ]


APPA = 11               # Appa's progress in numerical form. 
appaLocation = ["", ""] # Appa's room location. May not use locations past it.
AVATARSTATE = 0         # Progress toward winning the game
SUPPLIES = 2            # Energy needed to use locations
DEVASTATION = 0         # How close you are to losing the game


# Mothership - This represents the row it's currently on, and its Thematic Name dependent on the map you are playing on
MOTHERSHIP = [ 0, "The Drill" ]

# Enemy ships and hostile groups are tracked here
FIRENATION = [ # [X, Y], Map Abbreviation, Thematic name, Is respawning in mothership? , Is in play?
    # Fire Nation Forces
    [ [1, 0], "FN", "Azula",  False, True],
    [ [2, 0], "FN", "Ty Lee", False, True],
    [ [3, 0], "FN", "Mai",    False, True],
    [ [4, 0], "FN", "a firebender company", False,  True],
    [ [5, 0], "FN", "a Tundra Tank batallion", False,  True],
    # Hostile Groups
    [ [1, 0], "HO", "The Dai Li", False, False],
    [ [2, 0], "HO", "Prince Zuko", False, False],
    [ [3, 0], "HO", "Jet", False, False],
    [ [5, 0], "HO", "Long Feng", False, False],
    
    ]

# The sky or "battleground" - holds sky information much like WORLD 
BATTLEGROUND = [ # Avatar State cost, What is in columns 1-5, Mothership action, Mothership passed this row boolean?
#>> = move ship to right space, << = move ship to left, VV = move mothership down, 4X = Destroy Ships if greater than coefficient number
    [0 , "  ", "  ", "  ", "  ", "  ", "      ", True],
    # Easy segment - 1st
    [11, "  ", "  ", "  ", ">>", "  ", "+1 Hos", False],
    [3 , "  ", "<<", ">>", "  ", "  ", "-2 App", False],
    [1 , "VV", "  ", "1X", "  ", "  ", "+1 Hos", False],
    [5 , "2X", "  ", "<<", "  ", "4X", "      ", False],
    # Easy segment - 2nd
    [3,  "VV", ">>", "  ", "4X", "  ", "+1 Hos", False],
    [1 , "  ", "VV", "  ", "  ", "  ", "-1 App", False],
    [6 , "4X", "3X", "  ", "<<", "2X", "-1 AVA", False],
    [1 , ">>", "  ", "6X", "  ", "<<", "      ", False],
    # Easy segment - 3rd
    [2,  "  ", "  ", "4X", ">>", "  ", "-1 AVA", False],
    [3 , "5X", "  ", "<<", "  ", "  ", "+1 Hos", False],
    [1 , "  ", "VV", ">>", "  ", "6X", "      ", False],
    [4 , "VV", "3X", "  ", "4X", "VV", " Doom ", False],
    # Easy segment - 4th
    [1,  "3X", ">>", "  ", "VV", "  ", "      ", False],
    [3 , "  ", "6X", "  ", "<<", "4X", "      ", False],
    [1 , ">>", "  ", "3X", "  ", "<<", "      ", False],
    [3 , "  ", "5X", "VV", "4X", "  ", "      ", False],
    
]

# The dice that are in your possession and will be rolled
#   [ "Color", die number rolled, Location's information ]
DICE = [ ["White", 1, "" ], ["White", 1, "" ], ["Grey", 1, "" ], ["Grey", 1, "" ], ["Grey", 1, "" ] ]


def displayMap():
    global appaLocation
    
    # Sky/Battleground part
    print("      |======|======|======|======|======|         ")
    rowIndex = 0
    YColumnIndex = len(BATTLEGROUND)
    for piece in BATTLEGROUND:          # Avatar State
        if AVATARSTATE >= YColumnIndex:    # If this step is fulfilled, block it out
            print("[{#}]", end = " ")
        elif piece[0] >= 10: 
            print("[" + str(piece[0]) + " ]", end = " ")
        elif piece[0] < 10 and piece[0] != 0:
            print("[ " + str(piece[0]) + " ]", end = " ")
        else:
            print(" "*6, end = "")

        for X in range(1, 6): # The 5 columns
            enemyFound = False
            for enemy in FIRENATION:
                if enemy[0][0] == X and enemy[0][1] == rowIndex and enemy[-1] == True:
                    enemyFound = True
                    break

            if piece[-1] == True and enemyFound == True: # Mothership is printed, but enemy is printed on top first 
                print("|==" + enemy[1] + "==", end = "") 
            elif piece[-1] == True:
                print("|======", end = "")
            elif enemyFound == True and BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ][1] == "X": # Enemy is vulnerable
                print("| " + BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ][0] + enemy[1] + "X ", end = "")
            elif enemyFound == True: 
                print("| !" + enemy[1] + "! ", end = "") # Print a Fire Nation ship in the column
            else:    
                print("|  " + piece[X] + "  ", end = "") # Otherwise, the terrain
        print("|", end = "")

        if piece[-1] == False: # Mothership actions, if it hasnt reached them yet
            print(" [" + piece[6] + "]", end = "") 
        print("") # New line at last

        rowIndex += 1
        YColumnIndex -= 1

    print("[{#}] ------------ Ba Sing Se ------------ [  A/B ]\n" +
          "---------------------------------------------------")

    # World part
    # 3 BUGS - Cannot properly combine bigger sized locations; and their stats underneath
    
    locationSizeCounter = 1 # Counter is used to special print bigger locations
    locationIndexStart = 0  # Index is needed to iterate back in time through the loop
    locationIndexEnd = 0
    verticalConnection = 0 # 0 - Leftside; 1 - Rightside
    for location in WORLD:
        
        if location[0][0] == 0: 
            print(" "*7 , end = "") # New line gets 7 Spaces, and reset Counter
            locationSizeCounter = 1

        appaLocation = appaTester.findAppa(APPA) # Get Appa's location USING A FUNCTION IMPORTED FROM ANOTHER MODULE
            
        if location[0] == appaLocation and location[1] == 0:  # Appa overrides the location
            print("{APPA}", end = "")
        elif location[0] == appaLocation and location[5] == 0:
            print("[APPA]", end = "")

        elif location[1] == 0 and location[-2] != 0:
            print("={><}=", end = "") # Empty location you're traveling to
        elif location[1] == 0:
            print("=={}==", end = "") # Empty location connections
        elif location[5] != 0:
            print("(>" + location[2] + "<)", end = "") # Dice Chosen location
        else:
            print("[ " + location[2] + " ]", end = "") # Dice Non-chosen location


        if location[1] > 1 and locationSizeCounter < location[1]:
            print("|", end = "") # Double location
            locationSizeCounter += 1
        # ELIF dice chosen
        # ELSE
        
        elif location[0][0] != 4:
            print("=", end = "") # Connections, unless its on edge of map

        locationIndexEnd += 1
        
        if location[0][0] == 4: # Each location will have their costs shown underneath
            print("") 
            print(" "*7 , end = "")
            for X in range(locationIndexStart, locationIndexEnd):
                if WORLD[X][1] == 0: # Skip over empty locations
                    print(" "*7, end = "")
                else:                # Absurd amounts of logic just to add spaces to make everything line up
                    
##                    if WORLD[X][1] > 1: # Bigger locations have a shared cost, not separate
##                        print(" "*4*WORLD[X][1], end = "")
##                        if WORLD[X][1] == 2:
                            

                    
                    if WORLD[X][-3] != 0:
                        print( str(WORLD[X][-3]) + ":", end = "")
                    else:
                        print(" " + str(WORLD[X][-3]) + ":", end = "")

                    
                    if WORLD[X][-1] == 0:
                        print( str(WORLD[X][-1]), end = "   ")
                    elif WORLD[X][-1] > 0:
                        print("+" + str(WORLD[X][-1]), end = "  ")
                    elif WORLD[X][-1] < 0:
                        print( str(WORLD[X][-1]), end = "  ")
                        
            locationIndexStart = locationIndexEnd

            # Vertical connection goes on new line and either on left or right, reverse afterwards.
            if location[0][1] != 5 and verticalConnection == 0:
                print("")
                print(" "*9, end = "")
                print("||")
            elif location[0][1] != 5 and verticalConnection == 1:
                print("")
                print(" "*37, end = "")
                print("||")
            if verticalConnection == 0: 
                verticalConnection = 1
            elif verticalConnection == 1:
                verticalConnection = 0

# Dice Phase
# POSSIBLE BUG - Empty locations you wish to travel to display "NULL", which is a little ugly. Maybe "Empty" is better?
def dicePhase():
    global DEVASTATION, APPA, appaLocation, gameOver
    exploring = False
    
    for dice in DICE: # Roll all 5 dice
        dice[1] = random.randint(1,6)

    dicePlaced = 0
    print("\n ========== PHASE 1 - Dice Phase ==========")
    while dicePlaced < 5:
        displayMap()
        print("\n")
        for index, dice in enumerate(DICE):
           
            if dice[-1] != "":
                print("#" + str(index+1) + ":", dice[0], str(dice[1]), "| Col.", (dice[-1][0][0]+1), "|\t- ("+ dice[-1][2] + ")", dice[-1][3])
            else:
                print("#" + str(index+1) + ":", dice[0], str(dice[1]), "\t-    ?")
            
        print("-----------------------------\n",
              "Supplies: ["+str(SUPPLIES)+"/7]  |  " +
              "Avatar State: ["+str(AVATARSTATE)+"/"+str(len(BATTLEGROUND)-1)+"]  |  " +
              "Devastation: ["+str(DEVASTATION)+"/8]")

        repeat = True
        while repeat == True:
            chooseDice = input("\nCHOOSE WHICH DICE YOU'D LIKE TO USE:\n")
            chooseDice = inputValidation(chooseDice, "Selecting Dice")
            print("\nPlease choose a location to activate with your", DICE[int(chooseDice)-1][0], str(DICE[int(chooseDice)-1][1])+":")

            chooseLocationX = input("ENTER X COORDINATE:  ")
            chooseLocationX = inputValidation(chooseLocationX, "chooseLocationX")
            
            chooseLocationY = input("ENTER Y COORDINATE:  ")
            chooseLocationY = inputValidation(chooseLocationY, "chooseLocationY")
        
            for location in WORLD:
                if ( location[0][0] == int(chooseLocationX)-1 ) and ( location[0][1] == int(chooseLocationY)-1 ):
                    pendingLocation = location
                    break

            pendingLocationIndex = appaTester.findLocationIndex( pendingLocation )

        ### Must pass additional verification to see if dice placement was legal (especially according to Appa)
            # Cannot place directly on Appa
            
            if pendingLocation[0][0] == appaLocation[0] and pendingLocation[0][1] == appaLocation[1]:
                print("Error. You cannot place a die on Appa. Resetting...\n")

            # May not use "empty rooms" (unless you're exploring, then it's alright)
            elif pendingLocation[1] == 0 and pendingLocationIndex < APPA:
                print("Error. There's nothing to do in that explored, empty location! Resetting...\n")

            # Appa must be able to fly the distance equal to the die's number. You're only able to explore once per turn, though.
            elif pendingLocationIndex > APPA:
                if exploring == True:
                    print("Error. You may only place one die ahead of Appa. You may not explore more than once in a turn. Resetting...\n")
                elif pendingLocationIndex - APPA > DICE[int(chooseDice)-1][1]:
                    print("Error. Appa can only fly a distance equal to your die. That location is too far. Resetting...\n")
                elif DICE[int(chooseDice)-1][1] >= pendingLocationIndex - APPA:
                    exploring = True
                    repeat = False
                    

            else:
                repeat = False
                    

        pendingLocation[-2] = DICE[int(chooseDice)-1][1]
        if pendingLocationIndex > APPA:
            pendingLocation[3] = "Exploring with Appa"
        DICE[int(chooseDice)-1][-1] = pendingLocation

        # ENEMIES MUST MOVE IN COLUMN
        for enemy in FIRENATION:
            if enemy[0][0] == int(chooseLocationX) and enemy[-1] == True:
                if WORLD[int(chooseLocationX)-1][2] == "Di" and int(chooseLocationY)-1 == 0: # Enemies advance slower if disrupted
                    member, verb = dialogue("Distracting")
                    print("\n##", member, verb, enemy[2] + "! ##\n")
                    enemy[0][1] += DICE[int(chooseDice)-1][1] - 1
                else:
                    enemy[0][1] += DICE[int(chooseDice)-1][1] # Move full length

                if enemy[0][1] > 16:            # Damage the city and reset the enemy's back to mothership
                    verbEnemy, raidedObject = dialogue("Raiding")
                    print("\n##", enemy[2], verbEnemy, raidedObject + "! ##\n")
                    DEVASTATION += 1
                    enemy[0][1] = 0
                    if DEVASTATION >= 8:
                        gameOver = True
                    
                elif BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ] == "<<":    # Move left if no enemy in the way
                    #DIALOGUE -- 'A battallion of firebenders received new orders'
                    enemyBlock = False
                    for enemyToLeft in FIRENATION:
                        if enemyToLeft[0][0] == (enemy[0][0]-1) and enemyToLeft[0][1] == (enemy[0][1]):
                            enemyBlock = True
                    if enemyBlock == False: 
                        enemy[0][0] -= 1
                        
                elif BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ] == ">>":    # Move Right if no enemy in the way
                    enemyBlock = False
                    for enemyToRight in FIRENATION:
                        if enemyToRight[0][0] == (enemy[0][0]+1) and enemyToRight[0][1] == (enemy[0][1]):
                            enemyBlock = True
                    if enemyBlock == False:    
                        enemy[0][0] += 1
                        
                elif BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ] == "VV":    # Move mothership
                    print("\n##", MOTHERSHIP[1], "approaches... ## \n")
                    MOTHERSHIP[0] += 1
                    BATTLEGROUND[ MOTHERSHIP[0] ][-1] = True
                    for enemy in FIRENATION:
                        if enemy[0][1] == (MOTHERSHIP[0]-1) and enemy[-2] == False: # Any enemies in spawn points will move WITH the mothership
                            enemy[0][1] = MOTHERSHIP[0]

                        elif enemy[0][1] == MOTHERSHIP[0]: # Enemies that are bulldozed by mothership are reset & put inside the mothership
                            enemy[0][1] = 0
                            enemy[-2] = True 

        # If a white dice was placed, reroll other dice not yet placed
        if DICE[int(chooseDice)-1][0] == "White":
            diceFound = 0
            for dice in DICE:
                if dice[-1] == "":
                    dice[1] = random.randint(1,6)
                    diceFound += 1
                else:
                    pass
            if diceFound > 0:
                print(" ## All unchosen dice have been rerolled! ## \n")
                #DIALOGUE -- Directly quote a relevant inspirational quote, or generic 'Aang praises the group'
                time.sleep(2)
        
        dicePlaced += 1

    displayMap() 
        

def roomPhase():
    # BUG - For some reason, the program is having issues iterating through an enemy after it lost in combat
    global AVATARSTATE, SUPPLIES, APPA

    print("\n\n ========== PHASE 2 - Location Phase ==========\n") 
    diceLeft = 5
    # Remove all Distraction locations from dice. You cannot use them in Location Phase anyway
    for dice in DICE:
        if dice[-1][2] == "Di":
            dice[-1][-2] = 0
            dice[-1] = "" 
            diceLeft -= 1

        
    while diceLeft > 0:
        for index, dice in enumerate(DICE):
            if dice[-1] != "":
                print("#" + str(index+1) + ":", dice[0], str(dice[1]), "| Col.", (dice[-1][0][0]+1), "|\t- ("+ dice[-1][2] + ")", dice[-1][3])

        print("-----------------------------\n",
              "Supplies: ["+str(SUPPLIES)+"/7]  |  " +
              "Avatar State: ["+str(AVATARSTATE)+"/"+str(len(BATTLEGROUND)-1)+"]  |  " +
              "Devastation: ["+str(DEVASTATION)+"/8]")

        resolveDice = input("\nYou will resolve all locations in any order you desire.\nCHOOSE DICE:\n")
    # INPUT VALIDATION - Do not permit player to choose a dice that is not displayed. It causes an error.
        while resolveDice.isdigit() == False or int(resolveDice) < 1 or int(resolveDice) > 5 or DICE[int(resolveDice)-1][-1] == "":
            if resolveDice.isdigit() == False:
                resolveDice = input("Error. That is not a number to select a dice. Try again:\n")
            else:
                resolveDice = input("Error. You've already resolved that dice. Choose one that has not been resolved:\n")

        locationResolve = DICE[int(resolveDice)-1][-1]
        canAffordSupplyCost = True

        # Double rooms are resolved as one, consuming both dice.
        multiRoom = False
        multiLocationsResolve = []
        if locationResolve[1] > 1 and locationResolve[3] != "Exploring with Appa":
            locations = []
            for locationName in DICE:
                if locationName[-1] != "":
                    locations.append( locationName[-1][3] )
                    if locationName[-1][3] == locationResolve[3]:
                        multiLocationsResolve.append( locationName[-1] )

            spotsFilled = locations.count( locationResolve[3] )
            if spotsFilled == locationResolve[1]:
                multiRoom = True


        if locationResolve[1] > 1 and multiRoom == False and locationResolve[3] != "Exploring with Appa": # A non-full room is a wasted dice.
            print("Not all spaces of this multi-spaced location are filled. You do not gain any benefits!")
            
            
        elif locationResolve[3] == "Exploring with Appa":
            if SUPPLIES > 0:
                destination = appaTester.findLocationIndex( locationResolve )
                APPA = destination
                SUPPLIES -= 1
                print("Appa just consumed 1 bag of supplies during the trip.")
            else:
                print("Appa does not have enough food to make the journey! You have 0 supplies.")
                canAffordSupplyCost = False

        elif locationResolve[2] == "Re":
            if multiRoom == True:
                suppliesOwed = locationResolve[-1] # Double/triple rooms power is the modifier and both dice combined
                for place in multiLocationsResolve:
                    suppliesOwed += place[-2]

            else:
                suppliesOwed = locationResolve[-2] + locationResolve[-1] # Dice + modifier

            if suppliesOwed + SUPPLIES > 7:
                SUPPLIES = 7
            elif suppliesOwed > 0:
                SUPPLIES += suppliesOwed
            print("The Gaang now has", str(SUPPLIES), "bags of supplies.")

            
        elif locationResolve[2] == "Co":
            if multiRoom == True:
                strength = locationResolve[-1]
                for place in multiLocationsResolve:
                    strength += place[-2]                

            else:
                strength = locationResolve[-2] + locationResolve[-1]

            if SUPPLIES >= (locationResolve[-3] * -1):
                for enemy in FIRENATION:
                    if BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ][1] == "X":
                        strengthNeeded = int(BATTLEGROUND[ enemy[0][1] ][ enemy[0][0] ][0])
                        if strength >= strengthNeeded and enemy[-1] == True:
                            enemy[0][0] = 0
                            enemy[0][1] = 0
                            member, verb = dialogue("Confrontation")
                            print("\n##", member, verb, enemy[2] + "! ##\n")
            else:
                print("The group is too wounded to attempt a confrontation. You need more supplies!")
                canAffordSupplyCost = False

        elif locationResolve[2] == "Tr":
            if multiRoom == True:
                lessonsLearned = locationResolve[-1]
                for place in multiLocationsResolve:
                    lessonsLearned += place[-2]

            else:
                lessonsLearned = locationResolve[-2] + locationResolve[-1]

            if SUPPLIES >= (locationResolve[-3] * -1):
                attempts = 3
                while attempts > 0:
                    if lessonsLearned >= BATTLEGROUND[ AVATARSTATE*-1 ][0]:
                        randomLesson = dialogue("Learning")
                        print("\n## Aang has learned", randomLesson + "! ##")
                        AVATARSTATE += 1
                        lessonsLearned -= BATTLEGROUND[ AVATARSTATE*-1 ][0]
                    else:
                        attempts -= 1
            else:
                print("Aang is exhausted. He is in no shape to practice the Avatar state. You need more supplies!")
                canAffordSupplyCost = False

        if canAffordSupplyCost == True:
            if locationResolve[-3] < 0 and locationResolve[3] != "Exploring with Appa":
                SUPPLIES += locationResolve[-3] # Addition because negative and positive makes negative 
                print( str(-1*locationResolve[-3]), "bag of supplies were used at", locationResolve[3] + ".")

        # Remove location from dice; location no longer has a dice number on it. Double or triple rooms have all dice removed.
        if multiRoom == True:
            for resolvemultiRoom in DICE:
                if resolvemultiRoom[-1] == "":
                    pass
                elif resolvemultiRoom[-1][3] == locationResolve[3]:
                    resolvemultiRoom[-1][-2] = 0
                    diceLeft -= 1
                    resolvemultiRoom[-1] = ""
                    
        else:
            DICE[int(resolveDice)-1][-1] = "" 
            locationResolve[-2] = 0
            diceLeft -= 1
        print("\n")

    
# Mothership Phase (Fire Nation Phase)
# BUG - It doesn't know what to do when it wants to spawn an enemy
def mothershipPhase():
    global MOTHERSHIP, APPA, AVATARSTATE, DEVASTATION, gameOver

    print("\n ========== PHASE 3 - Fire Nation Phase ==========") 

    MOTHERSHIP[0] += 1 # Mothership goes down a step
    BATTLEGROUND[ MOTHERSHIP[0] ][-1] = True
    for enemy in FIRENATION:
        if enemy[0][1] == (MOTHERSHIP[0]-1) and enemy[-2] == False: # Any enemies in spawn points will move WITH the mothership
            enemy[0][1] = MOTHERSHIP[0]

        elif enemy[0][1] == MOTHERSHIP[0]: # Enemies that are bulldozed by mothership are reset & put inside the mothership
            enemy[0][1] = 0
            enemy[-2] = True 

    if BATTLEGROUND[ MOTHERSHIP[0] ][-2] == " Doom ":
        gameOver = True
        if MOTHERSHIP[1] == "The Drill":
            print("\n\n\n The Drill has breached the Outer Walls... A legion of Firenation troops loom over the horizon. \n" +
                  "They descend upon the farms of Ba Sing Se like locusts. Within a matter of weeks, the inner city is forced to capitulate from starvation. \n" +
                  "THE DAY IS LOST... BUT THE EARTH PEOPLE ARE RESILIENT. THE OUTSIDERS MAY YET BE DRIVEN BACK BY A HERO...")
        
    elif BATTLEGROUND[ MOTHERSHIP[0] ][-2][3:] == "App": # Appa gets lost
        APPA -= int(BATTLEGROUND[ MOTHERSHIP[0] ][-2][1])
        if int(BATTLEGROUND[ MOTHERSHIP[0] ][-2][1]) == 1:
            print("\n## Appa has been feeling sick as of late... Appa is set back 1 space. ##\n")
        elif int(BATTLEGROUND[ MOTHERSHIP[0] ][-2][1]) == 2:
            print("\n## Appa has been captured! Appa is set back 2 spaces. ##\n")
        
    elif BATTLEGROUND[ MOTHERSHIP[0] ][-2][3:] == "AVA":
        AVATARSTATE -= int(BATTLEGROUND[ MOTHERSHIP[0] ][-2][1])
        print("\n## Aang faces a traumatic experience, clarifying his mortality and great burden. He is set back 1 space. ##\n")
        
    elif BATTLEGROUND[ MOTHERSHIP[0] ][-2][3:] == "Hos":
        for enemy in FIRENATION:
            if enemy[1] == "HO" and enemy[-1] == False:
                enemy[-2] = True
                enemy[-1] = True
                break
                # DIALOGUE -- 

    elif BATTLEGROUND[ MOTHERSHIP[0] ][-2][3:] == "Dev":
        DEVASTATION += 1
        verbEnemy, raidedObject = dialogue("Raiding")
        print("\n##", MOTHERSHIP[1], verbEnemy, raidedObject + "! ##\n")
        if DEVASTATION >= 8:
            gameOver = True

    enemiesRespawning = []
    for enemy in FIRENATION:
        if enemy[-1] == True and enemy[-2] == True:
            enemiesRespawning.append(enemy)

    availableSpawnPoint = [True, True, True, True, True]
    for enemy in FIRENATION:
        if enemy[-1] == False:
            pass
        else:
            if enemy[0][1] == MOTHERSHIP[0]:
                availableSpawnPoint[ (enemy[0][0])-1 ] = False

    
    columnsWithEnemies = []
    for enemy in enemiesRespawning:

        # Check which columns have enemies in them
        for enemyInAction in FIRENATION:
            if enemyInAction[-1] == False:
                pass
            else:
                columnsWithEnemies.append( enemyInAction[0][0] )

        # Place the respawning enemy in first column found with no enemy
        # UNKNOWN - Can it distinguish which spawnpoints are available without calling it??
        enemyDeployed = False
        for column in range(1, 6):
            if column not in columnsWithEnemies:
                enemy[0][0] = column
                enemy[0][1] = MOTHERSHIP[0]
                enemyDeployed = True
                enemy[-2] = False
                break

        # Otherwise, remaining enemies are placed in columns with furthest enemies from mothership
        if enemyDeployed == False:
            distanceOfEnemies = []
            availableColumns = []
            for enemyInAction in FIRENATION:
                if enemyInAction[-1] == False:
                    pass
                else:
                # Condition to add only if the spawning spot over the viable option is empty
                    if availableSpawnPoint[ (enemyInAction[0][0])-1 ] == True:
                        distanceOfEnemies.append( enemyInAction[0][1] )
                        availableColumns.append( enemyInAction[0][0] ) # Remember their respective X coords

            options = []
            for Y in distanceOfEnemies:
                index = distanceOfEnemies.index( Y )
                index = availableColumns[index]
                
                if Y == max(distanceOfEnemies):
                    options.append( [index, Y] )

            # Respawning enemy goes in THE column with furthest enemy
            if len(options) == 1:
                enemy[0][0] = options[0][0]
                enemy[0][1] = MOTHERSHIP[0]
                enemyDeployed = True
                enemy[-2] = False
                
            # If multiple options, the player gets to choose which column enemy spawns in
            elif len(options) > 1:
                print(options)
                print("BUG TESTING - Found multiple options. What now, boss?")
            
        
        
            

gameOver = False
while gameOver == False:
    
    dicePhase()
    roomPhase()
    mothershipPhase()


if DEVASTATION >= 8 or MOTHERSHIP[0] >= 12:
    if MOTHERSHIP[1] == "The Drill":
        print("\n\n\n The Drill has breached the Outer Walls... A legion of Firenation troops loom over the horizon. \n" +
              "They descend upon the farms of Ba Sing Se like locusts. Within a matter of weeks, the inner city is forced to capitulate from starvation. \n" +
              "THE DAY IS LOST... BUT THE EARTH PEOPLE ARE RESILIENT. THE OUTSIDERS MAY YET BE DRIVEN BACK BY A HERO...")
elif AVATARSTATE >= len(BATTLEGROUND)-1:
    print("\n\n ###### VICTORY! ######" ,
          "\n Aang has mastered the Avatar State and unleashed the full fury of all 4 elements on the Fire Nation!")
