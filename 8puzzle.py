import sys
from random import randint
from random import seed
from queue import PriorityQueue

seed(98765)
#inputFile = "input.txt"
inputFile = sys.argv[1]
myInput = open(inputFile, 'r')
#oneLine = myInput.readline()   #reads one line at a time
allLines = myInput.readlines()  #reads each line to an array

state = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
goal = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
maxNodes = -1

def move(st, direction):
    x = st.index('0')
    if direction == "up":
        if x < 3:
            #print("Invalid move")
            return -1
        else:
            temp = list(st)
            temp[x],temp[x-3] = temp[x-3],temp[x]
            new = tuple(temp)
            #print(new)
            return new
    elif direction == "down":
        if x > 5:
            #print("Invalid move")
            return -1
        else:
            temp = list(st)
            temp[x],temp[x+3] = temp[x+3],temp[x]
            new = tuple(temp)
            #print(new)
            return new
    elif direction == "left":
        if x == 0 or x == 3 or x == 6:
            #print("Invalid move")
            return -1
        else:
            temp = list(st)
            temp[x],temp[x-1] = temp[x-1],temp[x]
            new = tuple(temp)
            #print(new)
            return new
    elif direction == "right":
        if x == 2 or x == 5 or x == 8:
            #print("Invalid move")
            return -1
        else:
            temp = list(st)
            temp[x],temp[x+1] = temp[x+1],temp[x]
            new = tuple(temp)
            #print(new)
            return new
    else:
        #print("Invalid move")
        return -1

def printState():
    strState = "".join(state)
    strState = strState[:3] + " " + strState[3:6] + " " + strState[6:]
    strState = strState.replace("0", "b")
    print(strState)

def goalDist(st):
    count = 0
    for x in st:
        if int(x) != 0:
            if (int(x) < 3 and st.index(x) < 3) or (int(x) >= 3 and int(x) < 6 and st.index(x) >= 3 and st.index(x) < 6) or (int(x) >= 6 and st.index(x) >= 6):
                count = count + abs((int(x) % 3) - (st.index(x)%3))
            elif (int(x) < 3 and st.index(x) >= 3 and st.index(x) < 6) or (int(x) >= 3 and int(x) < 6 and (st.index(x) < 3 or st.index(x) >= 6)) or (int(x) >= 6 and st.index(x) < 6 and st.index(x) >= 3):
                count = count + abs((int(x) % 3) - (st.index(x)%3)) + 1
            else:
                count = count + abs((int(x) % 3) - (st.index(x)%3)) + 2
    return count

def numWrong(st):
    count = 0
    for x in st:
        if int(x) != st.index(x) and int(x) != 0:
            count = count + 1
    return count

def availableMoves(st):
    aMoves = []
    u = move(st, "up")
    if u != -1:
        aMoves.append("up")
    d = move(st, "down")
    if d != -1:
        aMoves.append("down")
    l = move(st, "left")
    if l != -1:
        aMoves.append("left")
    r = move(st, "right")
    if r != -1:
        aMoves.append("right")
    return aMoves

def Astar(st, h):
    gl = goal
    goalReached = 0
    n = maxNodes
    prio = PriorityQueue()
    if h == 'h1':
        currDist = numWrong(st)
    elif h == 'h2':
        currDist = goalDist(st)
    prio.put((currDist, st))
    weight = {}
    weight[st] = 0
    previous = {}
    previous[st] = None
    moveList = {}
    moveList[st] = "Start"
    curr = None
    while not prio.empty():
        if n == 0:
            break
        n = n - 1
        curr = prio.get()
        curr = curr[1]
        if curr == gl:
            goalReached = 1
            break
        aMoves = availableMoves(curr)
        for x in aMoves:
            newMove = move(curr, x)
            myWeight = 1 + weight[curr]
            if ((newMove not in weight) or (myWeight < weight[newMove])):
                weight[newMove] = myWeight
                previous[newMove] = curr
                moveList[newMove] = x
                if h == 'h1':
                    myDist = numWrong(newMove)
                elif h == 'h2':
                    myDist = goalDist(newMove)
                prio.put(((myWeight + myDist), newMove))
    if goalReached == 0:
        print("Node limit reached, did not find goal")
    else:
        print("Number of moves: " + str(weight[curr]))
        print("Moves:")
        m = moveList[curr]
        moves = []
        while m != None:
            #print(curr)
            moves.append(m)
            curr = previous[curr]
            if curr == None:
                break
            m = moveList[curr]
        moves.reverse()
        print(moves)

for x in allLines:
    if "setState" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("setState", "")
        x = x.replace("b", "0")
        state = tuple(x)
    elif "move" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("move", "")
        move(state, x)
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
                k = move(state, direction)
            state = k
    elif "maxNodes" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("maxNodes", "")
        n = int(x)
        maxNodes = n
    elif "solve A-star" in x:
        x = x.replace("solve A-star", "")
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        Astar(state, x)
    else:
        print("Invalid command:" + x)