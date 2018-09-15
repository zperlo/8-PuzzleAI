from random import randint

inputFile = "input.txt"
myInput = open(inputFile, 'r')
#oneLine = myInput.readline()   #reads one line at a time
allLines = myInput.readlines()  #reads each line to an array

state = ['b', '1', '2', '3', '4', '5', '6', '7', '8']

def move(direction):
    x = state.index('b')
    if direction == "up":
        if x < 3:
            print("Invalid move")
            return -1
        else:
            state[x],state[x-3] = state[x-3],state[x]
            print(state)
            return 0
    elif direction == "down":
        if x > 5:
            print("Invalid move")
            return -1
        else:
            state[x],state[x+3] = state[x+3],state[x]
            print(state)
            return 0
    elif direction == "left":
        if x == 0 or x == 3 or x == 6:
            print("Invalid move")
            return -1
        else:
            state[x],state[x-1] = state[x-1],state[x]
            print(state)
            return 0
    elif direction == "right":
        if x == 2 or x == 5 or x == 8:
            print("Invalid move")
            return -1
        else:
            state[x],state[x+1] = state[x+1],state[x]
            print(state)
            return 0
    else:
        print("Invalid move")
        return -1

def printState():
    strState = "".join(state)
    strState = strState[:3] + " " + strState[3:6] + " " + strState[6:]
    print(strState)

for x in allLines:
    if "setState" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("setState", "")
        state = list(x)
        print(state)
    elif "move" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("move", "")
        i = move(x)
    elif "printState" in x:
        printState()
    elif "randomizeState" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("randomizeState", "")
        n = int(x)
        for i in range(n):
            k = -1
            while k == -1:
                j = randint(1,4)
                if j == 1:
                    direction = "up"
                elif j == 2:
                    direction = "down"
                elif j == 3:
                    direction = "left"
                else:
                    direction = "right"
                k = move(direction)
    else:
        print(x)