import random

ZNAK_NEODLOCEN = "+"

class Cell:
    def __init__(self):
        self.cells = {1 : ".", 2 : ".", 3 : ".", 4 : ".", 5 : ".", 6 : ".", 7 : ".", 8 : ".", 9 : "."}

    def oznaci_polje(self, n, znak):
        if self.cells[n] == ".":
            self.cells[n] = znak
            return True
        else:
            return False

    def X_graphic(self):
        self.cells = {1 : "/", 2 : " ", 3 : "\\", 4 : " ", 5 : "X", 6 : " ", 7 : "\\", 8 : " ", 9 : "/"}

    def O_graphic(self):
        self.cells = {1 : "\\", 2 : "-", 3 : "/", 4 : "|", 5 : " ", 6 : "|", 7 : "/", 8 : "-", 9 : "\\"}

    def Draw_graphic(self):
        self.cells = {1 : "+", 2 : "+", 3 : "+", 4 : "+", 5 : "+", 6 : "+", 7 : "+", 8 : "+", 9 : "+"}

    def check_win(self):
        win_situations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (3, 5, 7), (1, 5, 9)]
        for i, j, k in win_situations:
            if self.cells[i] == self.cells[j] == self.cells[k] != "." and self.cells[i] != ZNAK_NEODLOCEN:
                return True
        return False

    def check_draw(self):
        return not ("." in self.cells.values() or self.check_win())

    @staticmethod
    def sign_switch(a):
        if a == "X":
            return "O"
        elif a == "O":
            return "X"