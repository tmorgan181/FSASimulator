#TRENTON MORGAN
#graphVizGenerator.py

#This program takes in a valid .ndfsa or .fsa file and processes it, determining
#the necessary parameters to generate the equivalent GraphViz (.gv) file.

#Used for formatting output
import pprint as pp

#Constant for the epsilon character '@'
EPS = '@'


#Get input and output files, then process if valid
def getFile():
    file = input("Input the Autonoma file: ")
    if file[-6:] != ".ndfsa" and file[-4:] != ".fsa":
        print("Not a valid NDFSA or FSA file.")
        return

    #Output file keeps input's name and changes .ndfsa/.fsa to .gv extension
    if file[-6:] == ".ndfsa":
        newFile = file[:-6] + ".gv"
    else:
        newFile = file[:-4] + ".gv"

    #Process machine file
    try:
        processFile(file, newFile)
    except FileNotFoundError:
        print("File not found.")

    return


#Process the file line-by-line, determining the necessary parameters to define
#an NDFSA or FSA, then generate the code necessary to implement the machine in
#GraphViz
def processFile(file, newFile):
    print("Valid file. Processing...")
    
    lineNum = 0     #Track which line we're on
    foundA = False  #An 'A' line has been found and successfully processed
    foundS = False  #An 'S' line has been processed
    foundB = False  #A 'B' line has been processed
    foundD = False  #A 'D' line has been processed
    validLetters = ['A', 'B', 'D', 'O', 'S', 'T']   #Valid line identifiers
    alphabet = []       #List of machine's alphabet characters
    machineStates = {}  #Dictionary of valid machine states and their
                        #accept/reject value
    startState = ""     #String for the start state of the machine
    deltaFunction = []  #List of tuples defining the machine's delta function

    #Open file and read lines as a list
    with open(file, 'r') as readFile:
        data = readFile.readlines()

    #pp.pprint(data)
        
    #Iterate over every line and process it based on its identifier
    for line in data:
        #Remove unused '\n' character from the line
        if '\n' in line:
            line = line[:-1]

        if line[0] != 'T' and line[0] != 'O':
            print(line)

        #Every line must start with a valid FSA letter
        if line[0] not in validLetters:
            print("Invalid format: Each line must begin with valid identifier.")
            return

        #Line starting with 'A' gives the FSA's alphabet
        if line[0] == 'A':
            #There can only be one 'A' line per file
            if foundA:
                print("Invalid format: There is already an A line.")
                return

            #Discard 'A' line identifier
            line = line[2:]

            #Set the machine's alphabet to the remaining characters
            alphabet = list(line)

            #Check for repeat characters
            for char in alphabet:
                if alphabet.count(char) > 1:
                    print("Invalid alphabet, found repeated character.")
                    return

            #Make sure '@' isn't in the alphabet
            if EPS in alphabet:
                print("Invalid alphabet, cannot contain the epsilon character.")
                return

            #Valid alphabet has been found and saved
            print("Found alphabet:" , alphabet, '\n')
            foundA = True

        #Lines starting with 'S' give all possible states of the machine
        elif line[0] == 'S':
            #Make sure an 'A' line has been processed first
            if foundA == False:
                print("Invalid file: 'A' line must come before 'S' line.")
                return
            
            #Remove the 'S' line identifier and convert the line to a list in
            #order to work with the states more easily
            line = line[2:].split(',')

            #print(line)

            expectState = True  #Ensures line is formatted as
                                #[State,Value,State,Value,...]
            for i in range(len(line)):
                if expectState == True:     #Current element should be a state
                    #Check for a valid accept/reject value in the next index
                    if line[i+1] == '0' or line[i+1] == '1':
                        #Check for duplicate machine states
                        if line[i] in machineStates.keys():
                            print("Invalid format: Duplicate state found.")
                            return
                        
                        #Update the dict of possible states with the new one and
                        #its accept/reject value
                        machineStates.update({line[i] : line[i+1]})
                        expectState = False     #Next element will be a value
                    else:
                        print("Invalid format: 'S' line must be formatted",
                              "as [State,Value,State,Value,...].")
                        return
                    
                elif line[i] == '0' or line[i] == '1':
                        expectState = True      #Next element will be a state

                else:   #Element is neither a state or a value
                    print("Invalid format: 'S' line must be formatted as",
                          "[State,Value,State,Value,...].")

            #Valid machine states have been found and saved
            print("Found machine states:")
            pp.pprint(machineStates)
            print('\n')
            foundS = True

        #Line starting with 'B' gives the start state of the machine
        elif line[0] == 'B':
            #Both an 'A' and 'S' line must come before 'B' line
            if foundA == False:
                print("Invalid format: 'A' line must come before 'B' line.")
                return
            if foundS == False:
                print("Invalid format: 'S' line must come before 'B' line.")
                return

            #Remove 'B' line identifier
            line = line[2:]

            #print(line)
            
            #Check if there are the correct number of elements in the line
            if len(line.split()) != 1:
                print("Invalid format: 'B' line must have exactly 1 state.")
                return
            
            #Check if the given start state is a valid machine state
            validStart = False
            for state in machineStates.keys():
                if line == state:
                    validStart = True
            if validStart == False:
                print("Invalid format: Start state must be a valid machine",
                      "state.")
                return
            else:
                startState = line;

            #Valid start state has been found and saved
            print("Found start state:", startState, '\n')
            foundB = True

        #Lines starting with 'D' define the delta function for the machine
        elif line[0] == 'D':
            #'A','S', and 'B' lines must come before 'D' line
            if foundA == False:
                print("Invalid format: 'A' line must come before 'D' line.")
                return
            if foundS == False:
                print("Invalid format: 'S' line must come before 'D' line.")
                return
            if foundB == False:
                print("Invalid format: 'B' line must come before 'D' line.")
                return

            #Remove 'D' line identifier
            line = line[2:]
            
            #Split the line into list of tuples (State,Char,State)
            line = line.split(',')
            line = [tuple(line[0+i:3+i]) for i in range(0, len(line), 3)]

            #print(line)

            #Verify all connections are valid
            for connection in line:
                #Check that connection is not empty
                if len(connection) > 1:
                    #print(connection)
                    #print("Current delta:", deltaFunction)

                    #Verify connection is formatted as (State,Char,State)
                    if len(connection) != 3:
                        print("Invalid format: Each delta connection must be",
                              "formatted as (State,Char,State).")
                        return
                    
                    #Make sure all states and characters are valid
                    if (connection[0] not in machineStates or
                        connection[2] not in machineStates):
                        print("Invalid format: Delta connections must contain",
                              "valid machine states.")
                        return
                    if (connection[1] not in alphabet and
                        connection[1] != EPS):
                        print("Invalid format: State connections must use",
                              "machine alphabet or epsilon.")
                        return
                    
                    #Check for duplicate delta functions
                    if connection in deltaFunction:
                        print("Invalid format: Duplicate connection found.")
                        print("Duplicate is:", connection)
                        return
                        
                    #Add connection to list of all delta functions
                    deltaFunction.append(connection)

            if foundD == True:   #Current line is not first 'D' line
                #Delta function updated with new connections
                print("Updated delta function:")
                pp.pprint(deltaFunction)
                print()
            else:
                #Valid delta function has been found and saved
                print("Found delta function:")
                pp.pprint(deltaFunction)
                print()
                foundD = True

        #Increment lineNum for next iteration
        lineNum += 1

    #After we've processed all necessary lines of the input file, use the states
    #and delta functions to generate the equivalent GraphViz code
    graph = generateGraph(machineStates, startState, deltaFunction)

    #Write graph code to new file
    with open(newFile, 'w+') as writeFile:
        writeFile.writelines(graph)

    #Close files
    readFile.close()
    writeFile.close()

    return
    

#Using the given parameters, generate and return the GraphViz code for
#the specified machine 
def generateGraph(states, start, delta):
    print('\n')     #Screen output formatting

    #This header is present in all .gv files
    header1 = "digraph cs2200m1 {\n\n"
    header2 = "rankdir=LR;\n"
    header3 = "eize=\"8,5\"\n\n"

    #Initialize output, in which the generated code will be stored. One line
    #in the code file will be one string item in the list
    output = [header1, header2, header3]

    #print("Current output:")
    #pp.pprint(output)

    #Create code for each state
    for i in states:
        print("Adding {", i, ":", states[i], "} to .gv")
        if states[i] == '0':
            shape = "circle"
        else:
            shape = "doublecircle"

        nodeCode = ("node [shape = " + shape + "]; " + i + '\n')
        print("State added as: ", nodeCode)
        output.append(nodeCode)

    #Create code for starting point
    point1 = "node [shape = point]; x\n\n"
    point2 = "x -> " + start + '\n'
    output.append(point1)
    output.append(point2)

    #Create code for delta connections
    index = 0       #Keep track of the connection index
    merged = []     #Keep track of which connections we have merged
    for connection in delta:
        label = connection[1]       #Label for this connection
        index += 1                  #Increment index

        #print(connection)
        #print("Label: ", label)

        #Check for other connections between the same two states
        for element in delta[index:]:
            #Merge the connection labels if needed (no repeat merges)
            if (element[0] == connection[0] and element[2] == connection[2]
                and element not in merged):
                merged.append(element)
                label += (", " + element[1])

        #Only add non-merged connections
        if connection not in merged:
            connectCode = (connection[0] + " -> " + connection[2] +
                           " [label = \"" + label + "\"];\n")
            print("Connection added as: ", connectCode[:-2], "\\n")
            output.append(connectCode)
        else:
            print("Connection already merged; not added")

    #Add closing bracket
    footer = '}'
    output.append(footer)

    return output


#Run program
getFile()
