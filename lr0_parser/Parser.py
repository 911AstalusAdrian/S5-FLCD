def enrich_grammar(grammar):
    grammar.productions['SP'] = [grammar.starting_symbol]
    grammar.starting_symbol = 'SP'
    grammar.non_terminals.append('SP')


def stringify_productions(productions):
    final_productions = []

    for lhs in productions.keys():
        if lhs != "SP":
            for rhs in productions[lhs]:
                final_productions.append(f"{lhs}->{rhs}")
        else:
            final_productions.append(f"{lhs}->.{productions[lhs][0]}")

    return final_productions


def get_enriched_starting_production(productions):
    for production in productions:
        if 'SP' in production:
            return production


def shift_dot(production_rhs, dot_pos):
    dot = production_rhs[dot_pos]
    nxt = production_rhs[dot_pos + 1]
    left = production_rhs[:dot_pos]
    right = production_rhs[dot_pos + 2:]
    shifted = left + nxt + dot + right
    return shifted


def get_productions_for_token(productions, token):
    final_productions = []
    for production in productions:
        lhs, rhs = production.split("->")
        token_pos = rhs.find('.') + 1
        if rhs[token_pos] == token:
            rhs = shift_dot(rhs, token_pos - 1)
            final_productions.append(f"{lhs}->{rhs}")

    return final_productions


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.terminals = grammar.terminals
        self.non_terminals = grammar.non_terminals
        enrich_grammar(self.grammar)
        self.productions = stringify_productions(self.grammar.productions)
        # self.canonical_collection([starting_production])
        print(self.closure(["SP->.S"]))

    def nonterminal_productions_dot(self, terminal):
        res = []
        for production in self.productions:
            lhs, rhs = production.split("->")
            if lhs == terminal:
                res.append(f"{lhs}->.{rhs}")

        return res

    def canonical_collection(self):
        pass

    def go_to(self, state, token):
        productions = get_productions_for_token(state, token)
        self.closure(productions)

    def closure(self, list_of_productions):

        closure_result = list_of_productions

        for production in list_of_productions:
            lhs, rhs = production.split("->")
            dot_position = rhs.find('.')
            if dot_position != len(rhs) - 1:
                if rhs[dot_position + 1] in self.non_terminals:
                    productions_for_nonterminal = self.nonterminal_productions_dot(rhs[dot_position + 1])
                    for p in productions_for_nonterminal:
                        if p not in closure_result:
                            closure_result.append(p)

        return closure_result
