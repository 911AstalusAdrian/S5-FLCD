from typing import List
import numpy as np


class Grammar:
    non_terminals = List[str]
    terminals = List[str]
    starting_symbol = str
    productions = dict()

    def __init__(self, filename):
        self.read_file(filename)

    def __str__(self):
        string = ""
        string += "non-terminals: " + str(self.non_terminals)[1:-1].replace("'", "") + "\n"
        string += "terminals: " + str(self.terminals)[1:-1].replace("'", "") + "\n"
        string += "starting symbol: " + self.starting_symbol + "\n"
        string += "productions: \n"
        for production_key in self.productions.keys():
            string += "\t" + production_key + " -> "
            for idx, rhs in enumerate(self.productions[production_key], start=1):
                if idx != len(self.productions[production_key]):
                    string += str(rhs) + " | "
                else:
                    string += str(rhs)
            string += "\n"
        return string

    def read_file(self, filename):
        with open(filename, 'r') as f:
            for line_counter, line in enumerate(f, start=1):
                line = line.strip()
                if line_counter >= 5:
                    tokens = line.split(" -> ")
                else:
                    tokens = line.split(" ")
                if tokens[0] == "non_terminals":
                    self.non_terminals = tokens[2:]
                elif tokens[0] == "terminals":
                    self.terminals = tokens[2:]
                elif tokens[0] == "starting_symbol":
                    self.starting_symbol = tokens[2]
                else:
                    if tokens[0] != "productions":
                        lhs = tokens[0]
                        # rhs = []
                        rhs = tokens[1].split(" | ")
                        if lhs not in self.productions.keys():
                            self.productions[lhs] = rhs
                        else:
                            self.productions[lhs].extend(rhs)

    def find_productions(self, nonterminal) -> str:
        if nonterminal in self.productions.keys():
            return nonterminal + " -> " + str(self.productions[nonterminal])[1:-1].replace("'", "").replace(",", " |")
        else:
            return "This Non-terminal does not appear in the set of Productions!"

    def ifCFG(self) -> str:
        for lhs in self.productions.keys():
            if lhs not in self.non_terminals:
                return "This Grammar is not a CFG"
        return "This Grammar is a CFG"