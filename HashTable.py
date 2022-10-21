class HashTable:
    def __init__(self, size: int):
        self.__index = 0
        self.__items = [[] for _ in range(size)]
        self.__size = size

    def hash(self, key) -> int:
        key_type = type(key).__name__
        if key_type == "int":
            return key % self.__size
        elif key_type == "str":
            sum = 0
            for character in key:
                sum += ord(character) - ord('0')
            return sum % self.__size

    def get_position(self, key):
        for item in self.__items[self.hash(key)]:
            if item[0] == key:
                return item[1]
        return -1

    def insert(self, key):
        if self.contains(key):
            return self.get_position(key)
        self.__items[self.hash(key)].append((key, self.__index))
        self.__index += 1
        return self.get_position(key)

    def delete(self, key) -> None:
        position = self.hash(key)
        for el in self.__items[position]:
            if el[0] == key:
                self.__items[position].remove(el)

    def contains(self, key):
        for element in self.__items[self.hash(key)]:
            if element[0] == key:
                return True
        return False

    def __str__(self) -> str:
        representation = ""
        for i in range(self.__size):
            representation += str(i) + "->" + str(self.__items[i]) + "\n"
        return representation
