class Field:
    def __init__(self, row, col, probabs, r, v, action, type):
        self.row = row
        self.col = col
        self.probabs = probabs
        self.r = r
        self.v = v
        self.action = action
        self.type = type


class Action:
    def __init__(self, move, value):
        self.move = move
        self.value = value
