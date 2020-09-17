# FSASimulator
This python program simulates the functionality of a [Finite State Automaton](https://en.wikipedia.org/wiki/Finite-state_machine).

# Description
This program takes in a validly formatted .fsa file and processes it, determining the necessary parameters to simulate a finite state machine. Using these parameters, a simulation is ran with each given input string, calculating the final state of the machine. If the final state is an accepted state, the .fsa input file is edited with "accept" on the output line corresponding to the given input. Otherwise, the output line is updated with "reject".

# FSA Files
An FSA M is defined as `M = (A, S, B, D)` where A is the machine's alphabet, S is the set of machine states, B is the start state, and D is the set of delta functions. Files with the .fsa extension are formatted in such a way that they can be parsed to determine the values of these parameters. Included in this repository are several example .fsa files for reference, and I will explain the format in detail below.

Within an .fsa file, the first three lines are reserved to define the machine's alphabet A, states S, and start state B, respectively. Machine states have an extra value attached to indicate whether they are accepting states (1) or rejecting states (0). What follows is an example format for the first three parameter definitions:

`A xyz123`

`S state_x,0,state_y,1,state_z,0`

`B state_x`

Here we have defined our machine's alphabet to be "xyz123". Similarly, the machines states are given as "state_x" (rejecting), "state_y" (accepting), and "state_z" (rejecting). Lastly, the start state of the machine is specified to be "state_x".

Next in the .fsa file, lines beginning with D define the machine's delta functions. Each transition is formatted as `start_state,alphabet_char,end_state`, and each line may contain an arbitrary number of delta functions. There may be any number of D lines in an .fsa file. For example:

`D state_x,1,state_y,state_x,z,state_z`

Here we define the transitions from state_x. While in state_x, if an input "1" is read, the machine transitions to state_y. If a "z" is read, it moves to state_z.

`D state_y,y,state_x,state_y,3,state_z,state_y,1,state_y`

This line defines the transtitions from state_y. While in state_y, if an input "y" is received, we move to state_x. Similarly, if we get a "3" as input while in state_y, the machine moves to state_z. Lastly, if we read in a "1", we simply stay in state_y.

Following these D lines, the next lines come in pairs of T and O for input and output. A T line defines a string to be used as input for the FSA. Each character in the string is read one at a time, and machine transitions occur based on the delta functions defined above. Immediately following each T line must be an O line, which must be left blank, as it is reserved for writing the output reached from the given input string (either "accepted" or "rejected"). Ex:

`T 112233xxyyzz`

`O `

`T zyx321`

`O `

After running the FSA simulator with the parameters and inputs defined in the .fsa file, each O line is updated to reflect whether or not its corresponding input string caused the machine to end up in an accepted or rejected state. These changes overwrite the original .fsa file.

# GraphViz
The program GraphViz is used to generate a graphical representation of finite state machines, as seen in the .jpg files within the repository. The graphVizGenerator.py program takes in a valid FSA file and outputs a .gv file which can be utilized within GraphViz to draw the machine. GraphViz is available at https://graphviz.org.
