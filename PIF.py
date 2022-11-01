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
        self.export_st()
        self.export_pif()

    def generate_pif(self):
        line_nr = 1
        all_good = True
        for line in self.st.get_file_lines():
            tokens = list(filter(None, re.split(';| |: |{ | }|,|\n', line)))
            for token in tokens:
                if '[' in token or ']' in token:
                    token = token.replace('[', '')
                    token = token.replace(']', '')
                if token in self.tokens_list:
                    self.pif.append((-1, self.st.get_token_index(token)))
                elif self.is_constant(token):
                    self.pif.append((self.st.get_constant_position(token), self.get_constant_id()))
                elif self.is_identifier(token):
                    self.pif.append((self.st.get_identifier_position(token), self.get_identifier_id()))
                else:
                    # print("LEXICAL ERROR ON LINE " + str(line_nr))
                    all_good = False
            line_nr += 1
        if all_good:
            print("NO LEXICAL ERRORS")



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

    def export_st(self):
        f = open("output/ST.out", "w")
        f.write(self.st.__str__())
        f.close()

    def export_pif(self):
        f = open("output/PIF.out", "w")
        f.write(self.__str__())
        f.close()

    def __str__(self):
        string = "------P.I.F.------\n"
        string += "element type | position in its list\n"
        for pif_elem in self.pif:
            string += str(pif_elem[0]) + " --- " + str(pif_elem[1]) + "\n"
        return string
