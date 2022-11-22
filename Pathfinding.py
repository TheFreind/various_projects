
# Check each neighboring cell. 
# -If cell is a untraversible wall, skip it.
#
# -If it doesn't have a count:
#       add it to the open list and increment its count by 1.
# -elif it already has a count:
#       continue
# 
# 
# If at some point the current cell IS THE DESTINATION:
#   path = [destinationCell]
#   while path[-1] == WeFoundOurStartCell:  # While cell we're checking is not the start is false, loop.
#       Check each neighboring cell. Choose the lowest count cell. 
#       Add that cell to the path list.
#       If the cell IsOurStartCell, we can end the loop.


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
    list('      |     }     |  |     }     |\             '),
    list('  /-------==----==---+     |     +---------+\   '),
    list('  }   }     ||||     }     |     }     |   |]\  '),
    list('  |   |     ||||     |-----|==---|-----|   |]]  '),
    list('  }   }     ||||     }     |     }     }   |]/  '),
    list('  \-------==----==---+     |     +---------+/   '),
    list('      |     }     |  |     }     |/             '),
    list('      \-----------/  |---==+-----/              '),
    list('                     |     |/                   '),
    list('                     \==-==/                    '),
]



import time
 
level = [
    list('####################'),
    list('#X    #####  #   ###'),
    list('## ##       #### ###'),
    list('## #### # #####   ##'),
    list('##   ##X#   ##  # ##'),
    list('####    ###    ##  #'),
    list('####################'),
]

levelWidth = len(level[0])
levelHeight = len(level)

print(len(level[0]))
 
def getNextMoves(x, y):
    return {
        'left':  [x-1, y], 
        'right': [x+1, y],
        'up':  [x, y-1],
        'down':  [x, y+1]
    }.values()
 
# You must inform the pathFindingFunction: Map in list form, starting[X,Y], ending[X,Y] (from topleft to bottomright).
def getShortestPath(level, startCoordinate, endCoordinate):
    searchPaths = [[startCoordinate]]
    visitedCoordinates = [startCoordinate]
    
    while searchPaths != []:
        currentPath = searchPaths.pop(0)
        currentCoordinate = currentPath[-1]
        
        currentX, currentY = currentCoordinate
        
        if currentCoordinate == endCoordinate:
            return currentPath
        
        for nextCoordinate in getNextMoves(currentX, currentY):
            nextX, nextY = nextCoordinate
            
            if nextX < 0 or nextX >= levelWidth:
                continue
            
            if nextY < 0 or nextY >= levelHeight:
                continue
            
            if nextCoordinate in visitedCoordinates:
                continue
            
            if level[nextY][nextX] == '#':
                continue
            
            searchPaths.append(currentPath + [nextCoordinate])
            visitedCoordinates += [nextCoordinate]
 
shortestPath = getShortestPath(level, [1, 1], [7, 4])
 
for coordinate in shortestPath:
    x, y = coordinate
    level[y][x] = '.'
    
    for row in level:
        print( ''.join(row))
    
    print('')
    time.sleep(0.25)