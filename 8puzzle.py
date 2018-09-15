inputFile = "input.txt"
myInput = open(inputFile, 'r')
#oneLine = myInput.readline()   #reads one line at a time
allLines = myInput.readlines()  #reads each line to an array

state = ['b', '1', '2', '3', '4', '5', '6', '7', '8']
print(state)

for x in allLines:
    if "setState" in x:
        x = x.replace(" ", "")
        x = x.replace("\n", "")
        x = x.replace("setState", "")
        state = list(x)
        print(state)
    else:
        print(x)