import sys

from HashTable import HashTable
import re

identifier_regex = "^@[a-zA-Z0-9_]*$"


def is_identifier(name):
    if re.search(identifier_regex, name) is None:
        return False
    else:
        return True


def is_numeric_constant(const):
    if const.isnumeric():
        return True
    elif '-' in const:
        const = const.replace('-', '')
        return const.isnumeric
    else:
        return False


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
        line_nr = 1
        for line in self.lines:
            string_end_index = -1
            tokens = list(filter(None, re.split(';| |: |,|\n', line)))
            for i in range(len(tokens)):
                if i < string_end_index + 1:
                    continue
                token = tokens[i]
                if '<' in token:  # creating the string constant
                    for j in range(i, len(tokens)):
                        token2 = tokens[j]
                        if '>' in tokens[j]:
                            new_list = [s.strip("<>") for s in tokens[i:j + 1]]
                            token = " ".join(new_list)
                            string_end_index = j
                    self.constants.insert(token)
                    continue

                if '[' in token or ']' in token:  # remove the paranthesis from numbers in array
                    token = token.replace("]", "")
                    token = token.replace("[", "")
                if token not in self.tokens_list:
                    if is_identifier(token):
                        self.identifiers.insert(token)
                    elif is_numeric_constant(token):  # check if is a numerical constant
                        self.constants.insert(token)
                    else:
                        print("LEXICAL ERROR ON LINE " + str(line_nr) + " - token " + token + " is the issue")
                        sys.exit()
            line_nr += 1

    def get_token_index(self, searched_token):
        for token, index in self.tokens_indices:
            if searched_token == token:
                return index

    def get_tokens_indices(self):
        return self.tokens_indices

    def get_tokens_list(self):
        return self.tokens_list

    def get_file_lines(self):
        return self.lines

    def check_constant(self, check):
        return self.constants.contains(check)

    def get_constant_position(self, const):
        return self.constants.get_position(const)

    def check_identifier(self, check):
        return self.identifiers.contains(check)

    def get_identifier_position(self, identif):
        return self.identifiers.get_position(identif)

    def __str__(self):
        string = "-----ST-----\n"
        string += "constants\n"
        for const in self.constants.get_items():
            string += str(const[0]) + " --> " + str(const[1]) + "\n"
        string += "\nidentifiers\n"
        for identifier in self.identifiers.get_items():
            string += str(identifier[0]) + " --> " + str(identifier[1]) + "\n"
        return string
