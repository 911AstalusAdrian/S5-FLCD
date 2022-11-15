import sys
from typing import List, Dict, Tuple


class FiniteAutomaton:
    states = List[str]
    alphabet = List[str]
    initial_state = str
    final_states = List[str]
    transitions = dict()

    def __init__(self, filename):
        self.read_file(filename)

    def __str__(self) -> str:

        string = ""
        string += "states: " + str(self.states) + "\n"
        string += "alphabet: " + str(self.alphabet) + "\n"
        string += "initial state: " + self.initial_state + "\n"
        string += "final states: " + str(self.final_states) + "\n"
        string += "transitions: \n"
        for transition_key in self.transitions.keys():
            string += "\t" + str(transition_key) + " -> " + str(self.transitions.get(transition_key)) + "\n"
        return string

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line_counter, line in enumerate(f, start=1):
                line = line.strip()
                tokens = line.split(" ")
                if tokens[0] == "states":
                    self.states = tokens[2:]
                elif tokens[0] == "alphabet":
                    self.alphabet = tokens[2:]
                elif tokens[0] == "initial_state":
                    self.initial_state = tokens[2]
                elif tokens[0] == "final_states":
                    self.final_states = tokens[2:]
                else:
                    if tokens[0] != "transitions":
                        t1 = tokens[0].strip("(,")
                        t2 = tokens[1].strip(")")
                        transition = (t1, t2)
                        t3 = tokens[3]
                        if not transition in self.transitions.keys():
                            self.transitions[transition] = [t3]
                        else:
                            self.transitions[transition].append(t3)

    def check_sequence(self, sequence):
        # if not self.isDfa():
        #     raise Exception("The Finite Automaton is not a DFA")

        current_state = self.initial_state

        while sequence != "":
            key = (current_state, sequence[0])
            if key in self.transitions.keys():
                current_state = self.transitions[key][0]
                sequence = sequence[1:]
            else:
                return False

        return current_state in self.final_states

    def isDfa(self):
        for k in self.transitions.keys():
            if len(self.transitions[k]) > 1:
                return False
        return True
