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
state = ('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23')
goal = ('0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23')
maxNodes = -1
seed(98765)

# function to rotate in a given direction
# instead of moving just one tile we have to rotate multiple cubies
def move(st, direction):
    if direction == "F": # rotate front face clockwise
        F = ('6','7','8','0','1','2','9','10','11','3','4','5','12','13','14','15','16','17','18','19','20','21','22','23')
        temp = []
        for i in F:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new
    elif direction == "F!": # rotate front face counterclockwise
        F1 = ('3','4','5','9','10','11','0','1','2','6','7','8','12','13','14','15','16','17','18','19','20','21','22','23')
        temp = []
        for i in F1:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new
    elif direction == "L": # rotate left face clockwise
        L = ('13','14','12','3','4','5','2','0','1','9','10','11','20','18','19','15','16','17','7','8','6','21','22','23')
        temp = []
        for i in L:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new
    elif direction == "L!": # rotate left face counterclockwise
        L1 = ('7','8','6','3','4','5','20','18','19','9','10','11','2','0','1','15','16','17','13','14','12','21','22','23')
        temp = []
        for i in L1:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new
    elif direction == "U": # rotate upper face clockwise
        U = ('5','3','4','16','17','15','6','7','8','9','10','11','1','2','0','14','12','13','18','19','20','21','22','23')
        temp = []
        for i in U:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new
    elif direction == "U!": # rotate upper face counterclockwise
        U1 = ('14','12','13','1','2','0','6','7','8','9','10','11','16','17','15','5','3','4','18','19','20','21','22','23')
        temp = []
        for i in U1:
            temp.append(st[int(i)])
        new = tuple(temp)
        return new

# function to print the state
def printState():
    colorArr = ['r','g','w','r','w','b','r','y','g','r','b','y','o','w','g','o','b','w','o','g','y','o','y','b']
    print("front: " + colorArr[int(state[0])] + ", " + colorArr[int(state[3])] + ", " + colorArr[int(state[6])] + ", " + colorArr[int(state[9])])
    print("left: " + colorArr[int(state[14])] + ", " + colorArr[int(state[1])] + ", " + colorArr[int(state[19])] + ", " + colorArr[int(state[8])])
    print("right: " + colorArr[int(state[5])] + ", " + colorArr[int(state[16])] + ", " + colorArr[int(state[10])] + ", " + colorArr[int(state[23])])
    print("up: " + colorArr[int(state[13])] + ", " + colorArr[int(state[17])] + ", " + colorArr[int(state[2])] + ", " + colorArr[int(state[4])])
    print("back: " + colorArr[int(state[15])] + ", " + colorArr[int(state[12])] + ", " + colorArr[int(state[21])] + ", " + colorArr[int(state[18])])
    print("down: " + colorArr[int(state[7])] + ", " + colorArr[int(state[11])] + ", " + colorArr[int(state[20])] + ", " + colorArr[int(state[22])])

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
        if int(x) != st.index(x):
            count = count + 1
    return count/3 # since each cubie is 3 numbers in the state

# function to get all available moves from the given state and return them
# changed as the cube always has all 6 moves available
def availableMoves(st):
    aMoves = ["F","F!","L","L!","U","U!"]
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
    if "setState" in command: #setState won't work reasonably as some indexes are 2-digit
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        command = command.replace("setState", "")
        state = tuple(command)
    elif "move" in command:
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        command = command.replace("move", "")
        state = move(state, command)
    elif "printState" in command:
        printState()
    elif "randomizeState" in command:  # much easier since there are no invalid moves
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        command = command.replace("randomizeState", "")
        n = int(command)
        for i in range(n):
            moveArr = ["F","F!","L","L!","U","U!"]
            j = randint(0,5)
            print(moveArr[j])
            state = move(state, moveArr[j])
    elif "maxNodes" in command:
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        command = command.replace("maxNodes", "")
        n = int(command)
        maxNodes = n
    elif "solve A-star" in command:
        command = command.replace("solve A-star", "")
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        Astar(state, command)
    elif "solve beam" in command:
        command = command.replace("solve beam", "")
        command = command.replace(" ", "")
        command = command.replace("\n", "")
        k = int(command)
        beam(state, k)
    else:
        print("Invalid command:" + command)