from HashTable import HashTable
from SymbolTable import *

if __name__ == "__main__":
    my_st = SymbolTable()
    my_st.read_file("p2.in")
    my_st.parse_file()
    print(my_st)
    # print(my_st.constants.get_items())
    # print(my_st.identifiers.get_items())






