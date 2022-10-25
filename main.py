from SymbolTable import *

if __name__ == "__main__":
    my_st = SymbolTable()
    my_st.read_file("input/p2.in")
    my_st.parse_file()
    print(my_st)
