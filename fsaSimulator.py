#TRENTON MORGAN
#fsaSimulator.py

#This program takes in a valid .fsa file and processes it, determining the
#necessary parameters to simulate a finite state machine. Using these
#parameters, a simulation is ran with each given input string, calculating the
#final state of the machine. If the final state is an accepted state, the .fsa
#file is edited with "accept" on the output line corresponding to the given
#input. Otherwise, the output line is updated with "reject".

#Used for formatting output
import pprint as pp

#Get file input, then process if valid
def getFile():
    file = input("Input the FSA file:")
    if file[-4:] != ".fsa" :
        print("Not a valid FSA file.")
    else:
        try:
            processFile(file)
        except FileNotFoundError:
            print("File not found.")
        
#Process the file line-by-line, determining the necessary parameters to define
#an FSA, then run a simulation with the given input strings
def processFile(file):
    print("Valid FSA file. Processing...")
    
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
        
    #Iterate over every line and process it based on its identifier
    for line in data:
        #Remove unused '\n' character from the line
        if '\n' in line:
            line = line[:-1]
        
        #print(line)

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
                        
                        #Update the list of possible states with the new one and
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
                    if connection[1] not in alphabet:
                        print("Invalid format: State connections must use",
                              "machine alphabet.")
                        return
                    
                    #Check for duplicate delta functions
                    if connection in deltaFunction:
                        print("Invalid format: Duplicate connection found.")
                        print("Duplicate is:", connection)
                        return
                        
                    #Add connection to list of all delta functions
                    deltaFunction.append(connection)

            if foundD == True:   #Current line is not first 'D' line
                print("Updated delta function:")
                pp.pprint(deltaFunction)
                print()
            else:
                print("Found delta function:")
                pp.pprint(deltaFunction)
                print()
                foundD = True

        #Lines starting with 'T' give the input string to be tested in machine 
        elif line[0] == 'T':
            #'A', 'S', 'B', and 'D' lines must come before 'T' line
            if foundA == False:
                print("Invalid format: 'A' line must come before 'T' line.")
                return
            if foundS == False:
                print("Invalid format: 'S' line must come before 'T' line.")
                return
            if foundB == False:
                print("Invalid format: 'B' line must come before 'T' line.")
                return
            if foundD == False:
                print("Invalid format: 'D' line must come before 'T' line.")
                return

            #Remove 'T' line identifier
            line = line[2:]

            #print(line)

            #Check if all characters in input are part of the alphabet
            for char in line:
                if char not in alphabet:
                    print("Invalid tape: All characters must be part of the",
                          "machine's alphabet.")

            #Run the input string through a simulation of the machine with the
            #given alphabet, states, start state, and delta function
            output = runMachine(line, alphabet, machineStates,
                                startState, deltaFunction)
            
            expectOutput = True     #Ensures the next line is an 'O' line

        #Lines starting with 'O' hold the output of the previous 'T' input
        elif line[0] == 'O':
            #Make sure the previous line was a 'T' line 
            if expectOutput == False:
                print("Invalid format: Output line must follow a 'T' line.")
                return

            #Make sure 'O' line is blank before processing
            if len(line[2:]) > 1:
                print("Invaid format: Output line must be blank initially.")
                return

            #Update output on current line
            data[lineNum] = "O " + output + '\n'

            expectOutput = False    #Next line will not be an output

        #Increment lineNum for next iteration
        lineNum += 1

    #Overwrite file with updated data
    with open(file, 'w') as writeFile:
        writeFile.writelines(data)

    #Close files
    readFile.close()
    writeFile.close()

#Run the input tape through a machine with the given parameters and return the
#accept/reject output 
def runMachine(tape, alphabet, states, start, delta):
    print("Processing string:", tape)
    
    #Initialize current machine state as start state
    currState = start
    #print("Starting state is", currState)

    #Iterate over each character in input and update state based on delta
    for char in tape:
        stateChanged = False    #Ensures state is only updated once per char
        #Search through delta for matching currState and char, then update
        #currState to be the new state
        for element in delta:
            if stateChanged == False:
                if element[0] == currState and element[1] == char:
                    currState = element[2]
                    stateChanged = True

                    #print("State is now", currState)        

    #print("Ending state is", currState)
    #Determine if ending state is accepted or rejected
    if states[currState] == '0':
        output = "reject"
    else:
        output = "accept"

    print(output, '\n')

    return output
    

#Run program
getFile()
