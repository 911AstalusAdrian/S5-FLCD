class Item:
    def __init__(self, lhs: str, rhs: list, dot_pos: int):
        self.lhs = lhs
        self.rhs = rhs
        self.dot_pos = dot_pos

    def __eq__(self, other):
        return self.rhs == other.rhs and \
               self.lhs == other.lhs and \
               self.dot_pos == other.dot_pos

    def __str__(self):
        result = "[" + self.lhs + " -> "
        for i in range(len(self.rhs)):
            if i == self.dot_pos:
                result += ". "
            result += self.rhs[i] + " "
        if self.dot_pos == len(self.rhs):
            result += "."
        return result.strip() + "]"
