import time
 
levelWidth = 20
levelHeight = 7
 
level = [
    list('####################'),
    list('#X    #####  #   ###'),
    list('## ##       #### ###'),
    list('## #### # #####   ##'),
    list('##   ## #   ##  # ##'),
    list('####    ###    ## X#'),
    list('####################'),
]
 
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
 
shortestPath = getShortestPath(level, [1, 1], [18, 5])
 
for coordinate in shortestPath:
    x, y = coordinate
    level[y][x] = '.'
    
    for row in level:
        print( ''.join(row))
    
    print('')
    time.sleep(0.25)