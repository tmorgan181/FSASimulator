# FSASimulator
This program takes in a valid .fsa file and processes it, determining the necessary parameters to simulate a finite state machine. Using these parameters, a simulation is ran with each given input string, calculating the final state of the machine. If the final state is an accepted state, the .fsa file is edited with "accept" on the output line corresponding to the given input. Otherwise, the output line is updated with "reject".

#FSA Files
Included are several example FSA files, used as input to the simulator. An FSA is defined as M = (A, S, B, D) where A is the machine's alphabet, S is the set of machine states, B is the start state, and D is the delta function. Machine states with attached value 1 denote final states. T lines denote the input "tape" to be evaluated by the simulator. O lines are left blank during input, then filled with "Accepted" or "Rejected" based on whether the machine halts on a final state or not.
