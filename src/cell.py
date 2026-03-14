class Cord:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Cell:
    def __init__(self, left:'Cell', right:'Cell', up:'Cell', down:'Cell'):
        self.val = "E"
        self._left = left
        self._right = right
        self._up = up
        self._down = down

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_up(self):
        return self._up

    def get_down(self):
        return self._down   
    
    def set_left(self, cell:'Cell'):
        self._left = cell

    def set_right(self, cell:'Cell'):
        self._right = cell

    def set_up(self, cell:'Cell'):
        self._up = cell

    def set_down(self, cell:'Cell'):
        self._down = cell

    def __str__(self):
        return self.val