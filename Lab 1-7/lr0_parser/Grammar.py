from typing import List
import numpy as np


class Grammar:

    S_PRIME = "SP"
    non_terminals = List[str]
    terminals = List[str]
    starting_symbol = str
    productions = dict()

    def __init__(self, filename):
        self.read_file(filename)
        self.initial_starting_symbol = self.starting_symbol

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

    def check_if_enhanced(self):
        # Grammar is not enhanced if the Starting Symbol has more than one Production
        if len(self.productions[self.starting_symbol]) != 1:
            return False

        # we check that the Starting Symbol does not appear in any Production rhs
        for production_rhs in self.productions.values():
            for each_rhs in production_rhs:
                if self.starting_symbol in each_rhs:
                    return False

        return True  # otherwise, we have an enhanced Grammar

    def enhance_grammar(self):
        if not self.check_if_enhanced():
            self.non_terminals.append(Grammar.S_PRIME)  # add a new Starting Symbol, S'
            self.productions[Grammar.S_PRIME] = [self.starting_symbol]
            self.starting_symbol = Grammar.S_PRIME
            # self.is_enhanced = True

    def get_production_by_id(self, prod_id: int) -> tuple or None:
        for prod in self.productions.keys():
            for prod_value in self.productions[prod]:
                if isinstance(prod_value[1], int) and prod_value[1] == prod_id:
                    return prod, prod_value[0]
        return None

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
