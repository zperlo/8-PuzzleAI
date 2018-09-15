from random import randint
import sys

#inputFile = "input.txt"
inputFile = sys.argv[1]
myInput = open(inputFile, 'r')
#oneLine = myInput.readline()   #reads one line at a time
allLines = myInput.readlines()  #reads each line to an array

state = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
maxNodes = -1

def move(direction):
    x = state.index('0')
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
    strState = strState.replace("0", "b")
    print(strState)

def goalDist(st): #takes in a state as a list
    count = 0
    for x in st:
        if (int(x) < 3 and st.index(x) < 3) or (int(x) >= 3 and int(x) < 6 and st.index(x) >= 3 and st.index(x) < 6) or (int(x) >= 6 and st.index(x) >= 6):
            count = count + abs((int(x) % 3) - (st.index(x)%3))
            print("if1 count = " + str(count))
        elif (int(x) < 3 and st.index(x) >= 3 and st.index(x) < 6) or (int(x) >= 3 and int(x) < 6 and (st.index(x) < 3 or st.index(x) >= 6)) or (int(x) >= 6 and st.index(x) < 6 and st.index(x) >= 3):
            count = count + abs((int(x) % 3) - (st.index(x)%3)) + 1
            print("if2 count = " + str(count))
        else:
            count = count + abs((int(x) % 3) - (st.index(x)%3)) + 2
            print("if3 count = " + str(count))
    return count

#def A-star(n = maxNodes):

for x in allLines:
    if "setState" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("setState", "")
        x = x.replace("b", "0")
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
    elif "maxNodes" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("maxNodes", "")
        n = int(x)
        maxNodes = n
    else:
        print(x)