import sys
from random import randint
from queue import PriorityQueue

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

def Astar(st, h):
    gl = goal
    n = maxNodes
    fail = 0
    prio = PriorityQueue()
    if h == 'h1':
        currDist = numWrong(st)
    elif h == 'h2':
        currDist = goalDist(st)
    prio.put(st, currDist)
    weight = {}
    weight[st] = 0
    previous = {}
    previous[st] = None
    moveList = {}
    moveList[st] = "Start"
    curr = None
    while not prio.empty():
        if n == 0:
            fail = -1
            break
        else:
            n = n - 1
            curr = prio.get()
            if curr == gl:
                break
            u = move(curr, "up")
            if u != -1:
                myWeight = 1 + weight[curr]
                if (u not in weight) or (myWeight < weight[u]):
                    weight[u] = myWeight
                    previous[u] = curr
                    moveList[u] = "up"
                    if h == 'h1':
                        myDist = numWrong(u)
                    elif h == 'h2':
                        myDist = goalDist(u)
                    prio.put(u, myWeight + myDist)
            d = move(curr, "down")
            if d != -1:
                myWeight = 1 + weight[curr]
                if (d not in weight) or (myWeight < weight[d]):
                    weight[d] = myWeight
                    previous[d] = curr
                    moveList[d] = "down"
                    if h == 'h1':
                        myDist = numWrong(d)
                    elif h == 'h2':
                        myDist = goalDist(d)
                    prio.put(d, myWeight + myDist)
            l = move(curr, "left")
            if l != -1:
                myWeight = 1 + weight[curr]
                if (l not in weight) or (myWeight < weight[l]):
                    weight[l] = myWeight
                    previous[l] = curr
                    moveList[l] = "left"
                    if h == 'h1':
                        myDist = numWrong(l)
                    elif h == 'h2':
                        myDist = goalDist(l)
                    prio.put(l, myWeight + myDist)
            r = move(curr, "right")
            if r != -1:
                myWeight = 1 + weight[curr]
                if (r not in weight) or (myWeight < weight[r]):
                    weight[r] = myWeight
                    previous[r] = curr
                    moveList[r] = "right"
                    if h == 'h1':
                        myDist = numWrong(r)
                    elif h == 'h2':
                        myDist = goalDist(r)
                    prio.put(r, myWeight + myDist)
    if fail == -1:
        print("Node limit reached, did not find goal")
    else:
        print("Number of moves: " + str(weight[curr]))
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