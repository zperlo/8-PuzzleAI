# Zach Perlo (zip5)
import sys
from random import randint
from random import seed
from queue import PriorityQueue

# reading input
inputFile = sys.argv[1]
myInput = open(inputFile, 'r')
allLines = myInput.readlines()  #reads each line to an array

# setting global variables and the random seed
state = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
goal = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
maxNodes = -1
seed(98765)

# function to move in a given direction
def move(st, direction):
    x = st.index('0')
    if direction == "up":
        if x < 3:
            return -1
        else:
            temp = list(st)
            temp[x],temp[x-3] = temp[x-3],temp[x]
            new = tuple(temp)
            return new
    elif direction == "down":
        if x > 5:
            return -1
        else:
            temp = list(st)
            temp[x],temp[x+3] = temp[x+3],temp[x]
            new = tuple(temp)
            return new
    elif direction == "left":
        if x == 0 or x == 3 or x == 6:
            return -1
        else:
            temp = list(st)
            temp[x],temp[x-1] = temp[x-1],temp[x]
            new = tuple(temp)
            return new
    elif direction == "right":
        if x == 2 or x == 5 or x == 8:
            return -1
        else:
            temp = list(st)
            temp[x],temp[x+1] = temp[x+1],temp[x]
            new = tuple(temp)
            return new
    else:
        return -1

# function to print the state
def printState():
    strState = "".join(state)
    strState = strState[:3] + " " + strState[3:6] + " " + strState[6:]
    strState = strState.replace("0", "b")
    print(strState)

# function to get the manhattan didstance, ie h2
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

# function to get the linear distance, ie h1
def numWrong(st):
    count = 0
    for x in st:
        if int(x) != st.index(x) and int(x) != 0:
            count = count + 1
    return count

# function to get all available moves from the given state and return them
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

# function to solve via A* with given start state and heuristic
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
    numMoves = {}
    numMoves[st] = 0
    previous = {}
    previous[st] = None
    moveList = {}
    moveList[st] = "Start"
    curr = None
    #numStates = 0    #only for experiments
    while not prio.empty():
        #numStates = numStates + 1
        if n == 0:
            break
        n = n - 1
        curr = prio.get()
        curr = curr[1]
        if curr == gl:
            goalReached = 1
            break
        aMoves = availableMoves(curr)
        for direction in aMoves:
            newMove = move(curr, direction)
            myNumMoves = 1 + numMoves[curr]
            if ((newMove not in numMoves) or (myNumMoves < numMoves[newMove])):
                numMoves[newMove] = myNumMoves
                previous[newMove] = curr
                moveList[newMove] = direction
                if h == 'h1':
                    myDist = numWrong(newMove)
                elif h == 'h2':
                    myDist = goalDist(newMove)
                prio.put(((myNumMoves + myDist), newMove))
    if goalReached == 0:
        print("Node limit reached, did not find goal")
    else:
        print("Number of moves: " + str(numMoves[curr]))
        #print("Number of states: " + str(numStates))
        print("Moves:")
        m = moveList[curr]
        moves = []
        while m != None:
            moves.append(m)
            curr = previous[curr]
            if curr == None:
                break
            m = moveList[curr]
        moves.reverse()
        print(moves)

# function to solve via local beam sort with given start state and k value
def beam(st, k):
    gl = goal
    goalReached = 0
    successors = PriorityQueue()
    currDist = numWrong(st) + goalDist(st)
    successors.put((currDist, st))
    numMoves = {}
    numMoves[st] = 0
    previous = {}
    previous[st] = None
    moveList = {}
    moveList[st] = "Start"
    curr = None
    #numStates = 0  #only for experiments
    while goalReached == 0:
        j = 0
        kStates = []
        while (not successors.empty()) and j < k:
            tempState = successors.get()
            tempState = tempState[1]
            kStates.insert(j, tempState)
            j = j + 1
        for myState in kStates:
            #numStates = numStates + 1
            if goalReached == 1:
                break
            aMoves = availableMoves(myState)
            for direction in aMoves:
                newMove = move(myState, direction)
                myNumMoves = 1 + numMoves[myState]
                if ((newMove not in numMoves) or (myNumMoves < numMoves[newMove])):
                    numMoves[newMove] = myNumMoves
                    previous[newMove] = myState
                    moveList[newMove] = direction
                    myDist = numWrong(newMove) + goalDist(newMove)
                    successors.put((myDist, newMove))
                    if newMove == gl:
                        goalReached = 1
                        curr = newMove
                        break
    print("Number of moves: " + str(numMoves[curr]))
    #print("Number of states: " + str(numStates))
    print("Moves:")
    m = moveList[curr]
    moves = []
    while m != None:
        moves.append(m)
        curr = previous[curr]
        if curr == None:
            break
        m = moveList[curr]
    moves.reverse()
    print(moves)

# section for interpreting all the text file commands
for command in allLines:
    command = command.replace("\n", "")
    print(command)
    if "setState" in command:
        command = command.replace(" ", "")
        command = command.replace("setState", "")
        command = command.replace("b", "0")
        state = tuple(command)
    elif "move" in command:
        command = command.replace(" ", "")
        command = command.replace("move", "")
        state = move(state, command)
    elif "printState" in command:
        printState()
    elif "randomizeState" in command:
        command = command.replace(" ", "")
        command = command.replace("randomizeState", "")
        n = int(command)
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
    elif "maxNodes" in command:
        command = command.replace(" ", "")
        command = command.replace("maxNodes", "")
        n = int(command)
        maxNodes = n
    elif "solve A-star" in command:
        command = command.replace("solve A-star", "")
        command = command.replace(" ", "")
        Astar(state, command)
    elif "solve beam" in command:
        command = command.replace("solve beam", "")
        command = command.replace(" ", "")
        k = int(command)
        beam(state, k)
    elif "test" in command:
        command = command.replace("test", "")
        command = command.replace(" ", "")
        n = int(command)
        for z in range(n):
            x = randint(1,3)
            print("randomize times: " + str(x))
            for i in range(x):
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
                print(str(state))
            Astar(state, "h1")
            Astar(state, "h2")
            beam(state, 5)
            beam(state, 10)
    else:
        print("Invalid command:" + command)