import time
# Everything related to positioning:
#   - Teleporters
#   - Crewmovement
#   - Crew repositioning in tiles
#   - Fire spreading to other rooms
#   - Should crew automatically reposition to exact tile of terminal for manning?
#   - Crew spawn location


Kestral = [
    list('      HH       '),
    list(' HHHH HHHH     '),
    list('HHH HHHHHHHHHHH'),
    list('HHH HHHHHHHHHHH'),
    list(' HHHH HHHH     '),
    list('      HH       '),
]

Kestral2 = [
    list('                     /==-==\                    '),
    list('                     |     |\                   '),
    list('      /-----------\  |---==+-----\              '),
    list('      |   X }     |  |     }     |\             '),
    list('  /-------==----==---+     |     +---------+\   '),
    list('  }   }     ||||     }     |     }     | O |]\  '),
    list('  |   |     ||||     |-----|==---|-----|   |]]  '),
    list('  }   }     ||||     }     |     }     }   |]/  '),
    list('  \-------==----==---+     |     +---------+/   '),
    list('      |     }     |  |     }     |/             '),
    list('      \-----------/  |---==+-----/              '),
    list('                     |     |/                   '),
    list('                     \==-==/                    '),
]
# May path through: ==, }, ' '
# May NOT path through: |, -, \, /, +, ]

Kestral3 = [
    list('             /=-=\              '),
    list('             |   |\             '),
    list('    /-------\|-==+---\          '),
    list('    | X }   ||   }   |\         '),
    list('  /---==--==-+   |   +-----+\   '),
    list('  } }   ||   }   |   }   |O|]\  '),
    list('  | |   ||   |---|==-|---| |]]  '),
    list('  } }   ||   }   |   }   } |]/  '),
    list('  \---==--==-+   |   +-----+/   '),
    list('    |   }   ||   }   |/         '),
    list('    \-------/|-==+---/          '),
    list('             |   |/             '),
    list('             \=-=/              '),
]



def drawMap(map, shortestPath):
    for coordinate in shortestPath:
        x, y = coordinate
        if map[y][x] == ' ':
            map[y][x] = '.'
        
        for row in map:
            print( ''.join(row))
        
        print('')
        time.sleep(0.25)


def getNextMoves(x, y):
    return {
        'left':  [x-1, y], 
        'right': [x+1, y],
        'up':  [x, y-1],
        'down':  [x, y+1]
    }.values()

# Arguments:
#   level - Map in list form
#       NOTE: the level list must be made up from multiple lists (representing Yrows) and 
#         an identical amount of Xcolumns to form a square. 
#   startString - Begin pathfinding from this string on the map.
#       ALTERNATE ARGUMENT: startCoordinate - Starting position in coordinate form [X, Y]
#   destinationString - Find a path from the startString to this string character on the map.
#       ALTERNATE ARGUMENT: endCoordinate - Ending position in coordinate form [X, Y]
#       ! return 'currentPath' logic must change to "currentCoordinate == endCoordinate:" 
def getShortestPath(level, startString, destinationString):
    # Check if destination/start location actually exist on the map. Raise an error if not.
    foundDestination = False
    foundStart = False
    verifyLocationsOfInterest = [startString, destinationString]
    for seekLocation in verifyLocationsOfInterest:
        for Y, Yrow in enumerate(level):
            for X, Xcolumn in enumerate(Yrow):

                if level[Y][X] == seekLocation:
                    if seekLocation == startString:
                        startCoordinate = [X, Y]
                        foundStart = True
                    elif seekLocation == destinationString:
                        foundDestination = True

    if foundStart == False:
        print("!! ERROR - %s was not found to be in the map!" % (startString))
        return
    if foundDestination == False:
        print("!! ERROR - %s was not found to be in the map!" % (destinationString))
        return

    # Set size
    levelWidth = len(level[0])
    levelHeight = len(level)

    # Begin pathfinding
    searchPaths = [[startCoordinate]]       # All "alternate timelines" where each bifurcating path creates a timeline going down that path  
    visitedCoordinates = [startCoordinate]  
    
    while searchPaths != []:
        currentPath = searchPaths.pop(0)
        currentCoordinate = currentPath[-1]
        
        currentX, currentY = currentCoordinate
        

#         if currentCoordinate == endCoordinate:        # Coordinate destination form, if you desire it over string
#             return currentPath                        # Change 'destinationString' argument to endCoordinate, which takes a coordinate [X,Y]
        if level[currentY][currentX]  == destinationString:
            return currentPath
        
        for nextCoordinate in getNextMoves(currentX, currentY):
            nextX, nextY = nextCoordinate
            
            if nextX < 0 or nextX >= levelWidth:    # Do not go out of map boundaries
                continue
            
            if nextY < 0 or nextY >= levelHeight:   # Do not go out of map boundaries
                continue
            
            if nextCoordinate in visitedCoordinates:    # Do not check already visited coordinate
                continue

            if (level[nextY][nextX] == '|' or level[nextY][nextX] == '-' or  # Do not path through walls
                level[nextY][nextX] == '/' or level[nextY][nextX] == '\\' or
                level[nextY][nextX] == '+' or level[nextY][nextX] == '#'):   
                continue
            
            searchPaths.append(currentPath + [nextCoordinate])
            visitedCoordinates += [nextCoordinate]





 
shortestPath = getShortestPath(Kestral3, "O", "X")
 
drawMap(Kestral3, shortestPath)

