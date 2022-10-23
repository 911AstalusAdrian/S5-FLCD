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
        with open("tokens.txt") as f:
            self.tokens = [x.strip() for x in f.readlines()]

    def read_file(self, filename):
        with open(filename) as f:
            self.lines = [x.strip() for x in f.readlines()]

    def parse_file(self):
        for line in self.lines:
            tokens = line.split(" ")
            for token in tokens:
                if token not in self.tokens:
                    if is_identifier(token):
                        self.identifiers.insert(token)
                    else:
                        self.constants.insert(token)

    def __str__(self):
        string = "-----ST-----\n\n"
        string += "constants\n"
        for const in self.constants.get_items():
            string += str(const[0]) + " --> " + str(const[1]) + "\n"
        string += "\nidentifiers\n"
        for identifier in self.identifiers.get_items():
            string += str(identifier[0]) + " --> " + str(identifier[1]) + "\n"
        return string

# TODO
#   ask about cases where you have delimiters, such as ";" or ":"
#   ex 'cond: @nr > 2;' -> the cond: and the 2;
#   should we remove the ';' and ':' as well, or workaround putting space in between them
