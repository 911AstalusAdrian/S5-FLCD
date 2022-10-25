from HashTable import HashTable
import re

identifier_regex = "^@[a-zA-Z0-9]*$"


def is_identifier(name):
    if re.search(identifier_regex, name) is None:
        return False
    else:
        return True


class SymbolTable:
    def __init__(self):
        self.constants = HashTable(41)
        self.identifiers = HashTable(41)
        self.lines = []
        self.tokens_indices = []
        self.tokens_list = []
        self.add_tokens()

    def add_tokens(self):
        count = 0
        with open("input/tokens.in") as f:
            for x in f.readlines():
                self.tokens_indices.append((x.strip(), count))
                self.tokens_list.append(x.strip())
                count += 1

    def read_file(self, filename):
        with open(filename) as f:
            self.lines = [x.strip() for x in f.readlines()]

    def parse_file(self):
        for line in self.lines:
            idx = -1
            tokens = list(filter(None, re.split(';| |: |{ | }|\n', line)))
            for i in range(len(tokens)):
                if i < idx + 1:
                    continue
                token = tokens[i]
                if '<' in token:
                    for j in range(i, len(tokens)):
                        token2 = tokens[j]
                        if '>' in tokens[j]:
                            new_list = [s.strip("<>") for s in tokens[i:j+1]]
                            token = " ".join(new_list)
                            idx = j
                if token not in self.tokens_list:
                    if is_identifier(token):
                        self.identifiers.insert(token)
                    else:
                        self.constants.insert(token)

    def __str__(self):
        string = "-----ST-----\n"
        string += "constants\n"
        for const in self.constants.get_items():
            string += str(const[0]) + " --> " + str(const[1]) + "\n"
        string += "\nidentifiers\n"
        for identifier in self.identifiers.get_items():
            string += str(identifier[0]) + " --> " + str(identifier[1]) + "\n"
        return string
