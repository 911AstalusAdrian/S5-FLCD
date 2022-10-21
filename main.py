from HashTable import HashTable

if __name__ == "__main__":
    constants_list = [1, 2, 3, "yes", "no", 12, 13, 14]
    constants_st = HashTable(11)
    for constant in constants_list:
        constants_st.insert(constant)

    print(constants_st)
    print(constants_st.get_position("yes"))
    print(constants_st.get_position("maybe"))
