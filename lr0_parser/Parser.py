from collections import deque

from lr0_parser import Grammar
from lr0_parser.Item import Item
from lr0_parser.State import State, Action


class Connection:
    def __init__(self, starting_state: State, final_state: State, symbol: str):
        self.starting_state = starting_state
        self.final_state = final_state
        self.symbol = symbol

    def __str__(self):
        return "Starting state: " + str(self.starting_state) + " " + \
               "Final state: " + str(self.final_state) + " " + \
               "Symbol: " + str(self.symbol)


class Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.canonical_collection = list()
        self.connections = []
        self.parsing_table = {}

    @staticmethod
    def item_in_closure(item, closure):
        for closure_item in closure:
            if item == closure_item:
                return True
            # if item.lhs == closure_item.lhs and \
            #         item.rhs == closure_item.rhs and \
            #         item.dot_pos == closure_item.dot_pos:
            #     return True
        return False

    def closure(self, items: list) -> State:
        current_closure = items.copy()

        done = False
        while not done:
            old_closure = current_closure.copy()
            for closure_item in current_closure:
                if closure_item.dot_pos < len(closure_item.rhs) and \
                        closure_item.rhs[closure_item.dot_pos] in self.grammar.non_terminals:
                    for production in self.grammar.productions[closure_item.rhs[closure_item.dot_pos]]:
                        if not self.is_item_in_closure(Item(closure_item.rhs[closure_item.dot_pos], production[0], 0),
                                                       current_closure):
                            current_closure.append(Item(closure_item.rhs[closure_item.dot_pos], production[0], 0))

            if current_closure == old_closure:
                done = True

        return State(items, current_closure, self.grammar.starting_symbol)

    def go_to(self, state: State, symbol: str) -> State:
        items_for_symbol = []
        for item in state.closure:
            if item.dot_pos < len(item.rhs) \
                    and item.rhs[item.dot_pos] == symbol:
                items_for_symbol.append(Item(item.lhs, item.rhs, item.dot_pos + 1))

        for state in self.canonical_collection:
            if state.closure_items == items_for_symbol:
                return state

        return self.closure(items_for_symbol)

    def create_canonical_collection(self):
        self.canonical_collection = [
            self.closure([Item(self.grammar.starting_symbol, self.grammar.productions[self.grammar.starting_symbol][0], 0)])
        ]

        index = 0
        while index < len(self.canonical_collection):
            state = self.canonical_collection[index]
            symbols = state.get_all_symbols_after_dot()
            for symbol in symbols:
                new_state = self.go_to(state, symbol)
                if new_state not in self.canonical_collection:
                    self.canonical_collection.append(new_state)
                self.connections.append(Connection(state, new_state, symbol))
            index += 1

    def create_parsing_table(self):
        for state in self.canonical_collection:
            state_connections = self.get_state_in_connections(state)
            if len(state_connections) == 0:
                if state.action == Action.ACCEPT:
                    self.parsing_table[state.id] = (Action.ACCEPT, None)
                elif state.action == Action.REDUCE:
                    prod_id = self.get_production_number_from_grammar(state)
                    if prod_id is None:
                        raise Exception("Something went wrong!")
                    self.parsing_table[state.id] = (Action.REDUCE, prod_id)
            elif state.action == Action.SHIFT or state.action == Action.SHIFT_REDUCE_CONFLICT:
                if state.id not in self.parsing_table.keys():
                    self.parsing_table[state.id] = (state.action, {})
                    for conn in state_connections:
                        self.parsing_table[state.id][1][conn.symbol] = conn.final_state.id
            else:
                if state.action == Action.REDUCE_REDUCE_CONFLICT:
                    raise Exception("Reduce reduce conflict!")

    def get_production_number_from_grammar(self, state: State) -> int or None:
        for prod in self.grammar.productions.keys():
            for prod_value in self.grammar.productions[prod]:
                if state.closure[0].lhs == prod and state.closure[0].rhs == prod_value[0]:
                    return prod_value[1]

        return None

    def get_state_in_connections(self, state: State) -> list:
        state_connections = []
        for conn in self.connections:
            if conn.starting_state == state:
                state_connections.append(conn)
        return state_connections

    def get_state_by_id(self, state_id: int) -> State or None:
        for state in self.canonical_collection:
            if state.id == state_id:
                return state
        return None

    def get_item_with_dot_at_end(self, state: State) -> Item or None:
        for item in state.closure:
            if item.dot_pos == len(item.rhs):
                return item
        return None

    def get_production_number_shift_reduce_conflict(self, state_id: int) -> int or None:
        state = self.get_state_by_id(state_id)
        if state is None:
            return None
        item = self.get_item_with_dot_at_end(state)
        if item is None:
            return None
        for prod in self.grammar.productions.keys():
            for prod_value in self.grammar.productions[prod]:
                if item.lhs == prod and item.rhs == prod_value[0]:
                    return prod_value[1]
        return None

    def parse_sequence(self, words: list) -> list:
        END_SIGN = "$"
        output_band = []

        work_stack = deque()
        work_stack.append(END_SIGN)
        work_stack.append(0)

        input_stack = deque()
        input_stack.append(END_SIGN)
        for word in reversed(words):
            input_stack.append(word)

        idx = 0
        while work_stack[-1] != END_SIGN or input_stack[-1] != END_SIGN:
            if self.parsing_table[work_stack[-1]][0] == Action.ACCEPT:
                while work_stack[-1] != END_SIGN:
                    work_stack.pop()
            elif self.parsing_table[work_stack[-1]][0] == Action.SHIFT:
                idx += 1
                top_state = work_stack[-1]
                symbol = input_stack.pop()
                work_stack.append(symbol)

                if symbol not in self.parsing_table[top_state][1].keys():
                    raise Exception(f"Index {idx} -> Invalid symbol: {symbol} for goto of state {top_state}")

                new_top_state = self.parsing_table[top_state][1][symbol]
                work_stack.append(new_top_state)
            elif self.parsing_table[work_stack[-1]][0] == Action.SHIFT_REDUCE_CONFLICT:
                possible_symbol = input_stack[-1]
                if (len(input_stack) == 1 and input_stack[-1] == END_SIGN) or \
                    possible_symbol not in self.parsing_table[work_stack[-1]][1].keys():
                    prod_id = self.get_production_number_shift_reduce_conflict(work_stack[-1])
                    prod = self.grammar.get_production_by_id(prod_id)
                    output_band.append(prod_id)
                    index = 0
                    while index < len(prod[1]):
                        work_stack.pop()
                        work_stack.pop()
                        index += 1
                    top_state = work_stack[-1]
                    work_stack.append(prod[0])
                    new_top_state = self.parsing_table[top_state][1][prod[0]]
                    work_stack.append(new_top_state)
                else:
                    idx += 1
                    top_state = work_stack[-1]
                    symbol = input_stack.pop()
                    work_stack.append(symbol)

                    if symbol not in self.parsing_table[top_state][1].keys():
                        raise Exception(f"Index {idx} -> Invalid symbol: {symbol} for goto of state {top_state}")

                    new_top_state = self.parsing_table[top_state][1][symbol]
                    work_stack.append(new_top_state)
            elif self.parsing_table[work_stack[-1]][0] == Action.REDUCE:
                prod = self.grammar.get_production_by_id(self.parsing_table[work_stack[-1]][1])
                output_band.append(self.parsing_table[work_stack[-1]][1])
                index = 0
                while index < len(prod[1]):
                    work_stack.pop()
                    work_stack.pop()
                    index += 1
                top_state = work_stack[-1]
                work_stack.append(prod[0])
                new_top_state = self.parsing_table[top_state][1][prod[0]]
                work_stack.append(new_top_state)

        output_band.reverse()
        return output_band

#
# def stringify_productions(productions):
#     final_productions = []
#
#     for lhs in productions.keys():
#         if lhs != "SP":
#             for rhs in productions[lhs]:
#                 final_productions.append(f"{lhs}->{rhs}")
#         else:
#             final_productions.append(f"{lhs}->.{productions[lhs][0]}")
#
#     return final_productions
#
#
# def get_enriched_starting_production(productions):
#     for production in productions:
#         if 'SP' in production:
#             return production
#
#
# def shift_dot(production_rhs, dot_pos):
#     dot = production_rhs[dot_pos]
#     nxt = production_rhs[dot_pos + 1]
#     left = production_rhs[:dot_pos]
#     right = production_rhs[dot_pos + 2:]
#     shifted = left + nxt + dot + right
#     return shifted
#
#
# def get_productions_for_token(productions, token):
#     final_productions = []
#     for production in productions:
#         lhs, rhs = production.split("->")
#         token_pos = rhs.find('.') + 1
#         if rhs[token_pos] == token:
#             rhs = shift_dot(rhs, token_pos - 1)
#             final_productions.append(f"{lhs}->{rhs}")
#
#     return final_productions
#
#
# class Parser:
#     def __init__(self, grammar):
#         self.grammar = grammar
#         self.terminals = grammar.terminals
#         self.non_terminals = grammar.non_terminals
#         if not self.grammar.check_if_enhanced():
#             self.grammar.enhance_grammar()
#         self.productions = stringify_productions(self.grammar.productions)
#         # self.canonical_collection([starting_production])
#         print(self.closure(["SP->.S"]))
#
#     def nonterminal_productions_dot(self, terminal):
#         res = []
#         for production in self.productions:
#             lhs, rhs = production.split("->")
#             if lhs == terminal:
#                 res.append(f"{lhs}->.{rhs}")
#
#         return res
#
#     def canonical_collection(self):
#         pass
#
#     def go_to(self, state, token):
#         productions = get_productions_for_token(state, token)
#         self.closure(productions)
#
#     def closure(self, list_of_productions):
#
#         closure_result = list_of_productions
#
#         for production in list_of_productions:
#             lhs, rhs = production.split("->")
#             dot_position = rhs.find('.')
#             if dot_position != len(rhs) - 1:
#                 if rhs[dot_position + 1] in self.non_terminals:
#                     productions_for_nonterminal = self.nonterminal_productions_dot(rhs[dot_position + 1])
#                     for p in productions_for_nonterminal:
#                         if p not in closure_result:
#                             closure_result.append(p)
#
#         return closure_result
