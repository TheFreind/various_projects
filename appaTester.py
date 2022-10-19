APPA = 12


def findAppa(APPA):
    
    index = 1
    appaLocation = ["", ""]
    appaIndex = 0

    for row in range(1, 7):

        if (row % 2) == 1: # Go left if odd row
            for column in range(0, 5):
                if (5-column) + (row-1)*5 == APPA: # column logic
                    appaLocation[0] = column 
                    appaLocation[1] = row-1
                    appaIndex = (5-column) + (row-1)*5
                            
                index += 1


        elif (row % 2) == 0: # Go right if even row
            for column in range(0, 5):
                if index == APPA:
                    appaLocation[0] = column
                    appaLocation[1] = row-1
                    appaIndex = index
   
                index += 1

    #print("Appa is at #" + str(appaIndex) + ", which is location" , str(appaLocation) )
    return appaLocation


def findLocationIndex(location):
    index = 1
    for row in range(1, 7):

        if (row % 2) == 1: # Go left if odd row
            for column in range(0, 5):
                if column == location[0][0] and (row-1) == location[0][1]:
                    locationIndex = (5-column) + (row-1)*5
                    
                index += 1
                

        elif (row % 2) == 0: # Go right if even row
            for column in range(0, 5):
                if column == location[0][0] and (row-1) == location[0][1]:
                    locationIndex = index
                    
                index += 1

    return locationIndex

findAppa(APPA)
findLocationIndex( [[3, 5], 1, "Re", "Whatever", 0, 3, 0] )
