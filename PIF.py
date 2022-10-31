import re

from SymbolTable import SymbolTable


class PIF:
    def __init__(self, filename):
        self.filename = filename
        self.st = SymbolTable()
        self.pif = []
        self.st.read_file(self.filename)
        self.st.parse_file()
        self.tokens_list = self.st.get_tokens_list()
        self.tokens_indices = self.st.get_tokens_indices()
        self.generate_pif()

    def generate_pif(self):
        for line in self.st.get_file_lines():
            tokens = list(filter(None, re.split(';| |: |{ | }|,|\n', line)))
            for token in tokens:
                if token in self.tokens_list:
                    self.pif.append((-1, self.st.get_token_index(token)))
                elif self.is_constant(token):
                    self.pif.append((self.get_constant_id(), self.st.get_constant_position(token)))
                elif self.is_identifier(token):
                    self.pif.append((self.get_identifier_id(), self.st.get_identifier_position(token)))
                else:
                    continue

    def is_constant(self, token_to_check):
        return self.st.check_constant(token_to_check)

    def is_identifier(self, token_to_check):
        return self.st.check_identifier(token_to_check)

    def get_constant_id(self):
        for token, pos in self.tokens_indices:
            if token == "const":
                return pos

    def get_identifier_id(self):
        for token, pos in self.tokens_indices:
            if token == "identif":
                return pos

    def __str__(self):
        string = "------P.I.F.------\n"
        string += "element type | position in its list\n"
        for pif_elem in self.pif:
            string += str(pif_elem[0]) + " --- " + str(pif_elem[1]) + "\n"
        return string
