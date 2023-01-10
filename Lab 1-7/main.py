from lr0_parser.Parser import Parser
from lr0_parser.Grammar import Grammar
from lr0_parser.ParserOutput import ParserOutput


def print_menu_fa():
    print("1. Show FA")
    print("2. Check sequence")
    print("0. Exit")


def print_menu_grammar():
    print("1. Show Grammar")
    print("2. Show Productions for a Non-terminal")
    print("3. Check CFG")
    print("0. Exit")


def fa_menu(automata):
    go = True
    while go:
        print_menu_fa()
        value = input(">")
        if value == "0":
            go = False
            continue
        elif value == "1":
            print(automata)
        elif value == "2":
            user_input = input("Give sequence:")
            print("For the input '" + user_input + "' the check is " + str(automata.check_sequence(user_input)))
        else:
            print("Invalid choice")


def grammar_menu(grammar):
    go = True
    while go:
        print_menu_grammar()
        value = input(">")
        if value == "0":
            go = False
            continue
        elif value == "1":
            print(grammar)
        elif value == "2":
            non_terminal = input("non-terminal: ")
            print(grammar.find_productions(non_terminal))
        elif value == "3":
            print(grammar.ifCFG())
        else:
            print("Invalid choice")


if __name__ == "__main__":

    g = Grammar("grammar/g1.txt")
    g.enhance_grammar()
    print(g)

    p = Parser(g)
    p.create_canonical_collection()
    for state in p.canonical_collection:
        print(state)


    # p.create_parsing_table()
    # # print(p.parsing_table)
    #
    # print("Enter a sequence: ")
    # # sequence = input()
    # # output_band = p.parse_sequence(sequence.split(" "))
    #
    # output_band = p.parse_sequence(['a', 'b', 'c', 'b'])
    # print(output_band)
    #
    # parserOutput = ParserOutput(output_band, g)
    # parserOutput.compute_parsing_tree()
    # for item in parserOutput.parsing_tree:
    #     print(item)
    #
    # parserOutput.print_to_file("out1.txt")
