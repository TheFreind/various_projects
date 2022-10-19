with open('transactionHistory.txt', 'r') as f:
    linesList = f.readlines()

with open('transactionHistory.txt', 'w') as f:
   ## #for index, line in enumerate(linesList):
    index = len(linesList) - 1
    for line in range( len(linesList) , 0, -1):
        int(index) 
        if "SCAM" in linesList[index]:
            del linesList[index]
            del linesList[index]  # Delete the additional 'Thank you..' message that has now shifted to previous line
    
        index -= 1

    for line in linesList:
        f.write(line)
