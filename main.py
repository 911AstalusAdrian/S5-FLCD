# my_pif = PIF("input/p1.in")
from PIF import PIF
from automata.FA import *
from SymbolTable import *


def print_menu():
    print("1. Show FA")
    print("2. Check sequence")
    print("0. Exit")


if __name__ == "__main__":
    fa = FiniteAutomaton("input/test_fa.in")
    go = True
    while go:
        print_menu()
        value = input(">")
        if value == "0":
            go = False
            continue
        elif value == "1":
            print(fa)
        elif value == "2":
            user_input = input("Give sequence:")
            print("For the input '" + user_input + "' the check is " + str(fa.check_sequence(user_input)))
        else:
            print("Invalid choice")
