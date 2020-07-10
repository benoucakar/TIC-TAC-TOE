import random

class Cell:
    def __init__(self):
        self.cells = dict(enumerate(["."] * 9, 1))

    def mark_field(self, n, znak):
        if self.cells[n] == ".":
            self.cells[n] = znak
            return True
        else:
            return False

    def X_graphic(self):
        self.cells = {1 : "/", 2 : " ", 3 : "\\", 4 : " ", 5 : "X", 6 : " ", 7 : "\\", 8 : " ", 9 : "/"}

    def O_graphic(self):
        self.cells = {1 : "\\", 2 : "-", 3 : "/", 4 : "|", 5 : " ", 6 : "|", 7 : "/", 8 : "-", 9 : "\\"}
    
    def print_sign_graphic(self, sign):
        if sign == "X":
            self.X_graphic()
        elif sign == "O":
            self.O_graphic()

    def Draw_graphic(self):
        self.cells = {1 : "+", 2 : "+", 3 : "+", 4 : "+", 5 : "+", 6 : "+", 7 : "+", 8 : "+", 9 : "+"}

    def check_win(self):
        win_situations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (3, 5, 7), (1, 5, 9)]
        for i, j, k in win_situations:
            if self.cells[i] == self.cells[j] == self.cells[k] != "." and self.cells[i] != "+":
                return True
        return False

    def check_draw(self):
        return not ("." in self.cells.values() or self.check_win())
    
    def count_empty_space(self):
        count = 0
        for i in self.cells.items():
            if i != ".":
                count += 1
        return count
    
    def random_free(self):
        return random.choice([key for key, value in self.cells.items() if value == "."])

    @staticmethod
    def sign_switch(a):
        if a == "X":
            return "O"
        elif a == "O":
            return "X"

class Bot:
    def __init__(self, player_mark, bot_first):
        self.bot_first = bot_first
        self.player_mark = player_mark

    def win_block(self, cell):
        X_list = []
        O_list = []
        for space, sign in cell.cells.items():
            test = Cell()
            if sign == ".":
                test.cells = dict(cell.cells)
                test.mark_field(space, "X")
                if test.check_win():
                    X_list.append(space)
                test.cells = dict(cell.cells)
                test.mark_field(space, "O")
                if test.check_win():
                    O_list.append(space)
        if self.player_mark == "O":
            return (X_list + O_list + [0])[0]
        elif self.player_mark == "X":
            return (O_list + X_list + [0])[0]
    
    def vanila_optimal(self, cell):
        # bot je prvi
        if self.bot_first:
            yield 1 # prazno igro začne v kotu
            if cell.cells[5] == self.player_mark: #igralec da na sredo
                yield 9 # Če da igralec v prost kot, DONE, sicer blokiranje do konca
            else: # igralec ne da na sredo
                if self.player_mark == cell.cells[9]:
                    yield 3
                    yield 7
                elif self.player_mark == cell.cells[2] or self.player_mark == cell.cells[8]:
                    yield 7
                    yield 5
                elif self.player_mark == cell.cells[4] or self.player_mark == cell.cells[6]:
                    yield 3
                    yield 5
                elif self.player_mark == cell.cells[7]:
                    yield 9
                    yield 3
                elif self.player_mark == cell.cells[3]:
                    yield 9
                    yield 7
        # bot je drugi
        else:
            if cell.cells[5] == self.player_mark: # igralec da na sredo
                yield 1 # bot da v kot sledi blokiranja do konca ali
                yield 3 # če ne naredi grožnje za blok
            elif self.player_mark in [cell.cells[i] for i in [1, 3, 7, 9]]: # igralec da v kot
                yield 5 # da na sredo
                if self.player_mark == cell.cells[1] == cell.cells[9] or self.player_mark == cell.cells[3] == cell.cells[7]: # igra diagonalo
                    yield 2 # da ne padeš v past
                # prepreči slabo situacijo
                elif self.player_mark == cell.cells[1]:
                    yield 9
                elif self.player_mark == cell.cells[3]:
                    yield 7
                elif self.player_mark == cell.cells[7]:
                    yield 3
                elif self.player_mark == cell.cells[9]:
                    yield 1
        # če da igralec na rob je vseeno
        # konec algoritma
        while True:
            yield 0

    def vanila_dif_1(self, cell):
        while True:
            yield cell.random_free()
    
    def vanila_dif_2(self, cell):
        bot_optimal_generator = self.vanila_optimal(cell)
        inp = 0
        while True:
            if self.win_block(cell) != 0 and random.randrange(100) < 50:
                inp = self.win_block(cell)
            else:
                temp = next(bot_optimal_generator)
                if temp != 0 and random.randrange(100) < 75:
                    inp = temp
                else:
                    inp = cell.random_free()
            yield inp
        
    def vanila_dif_3(self, cell):
        bot_optimal_generator = self.vanila_optimal(cell)
        inp = 0
        while True:
            if self.win_block(cell) != 0 and random.randrange(100) < 75:
                inp = self.win_block(cell)
            else:
                temp = next(bot_optimal_generator)
                if temp != 0 and random.randrange(100) < 85:
                    inp = temp
                else:
                    inp = cell.random_free()
            yield inp
        
    def vanila_dif_4(self, cell):
        bot_optimal_generator = self.vanila_optimal(cell)
        inp = 0
        while True:
            if self.win_block(cell) != 0:
                inp = self.win_block(cell)
            else:
                temp = next(bot_optimal_generator)
                if temp != 0:
                    inp = temp
                else:
                    inp = cell.random_free()
            yield inp
    
    def ultimate_density(self, game):
        scores = []
        for i in range(1, 9):
            scores.append((i, game[i].count_empty_space()))
        random.shuffle(scores)
        return max(scores, key=lambda par: par[1])[0]

    def ultimate_incell_move(self, game, inp_cell):
        if self.win_block(game[inp_cell]) != 0:
            return self.win_block(game[inp_cell])
        else:
            return self.ultimate_density(game)

class Vanila_2:
    # P - pre game, M - main game, E - end game
    def __init__(self):
        self.cell = Cell()
        self.num_turns = 0
        self.turn = ""
        self.bad_choice = False
        self.state = "P"
        
    def choose_parameters(self, first_player_mark):
        self.turn = first_player_mark

    def check_bad_move(self):
        if self.bad_choice:
            self.bad_choice = False
    
    def make_move(self, inp_space):
        if self.cell.mark_field(inp_space, self.turn):
            self.turn = self.cell.sign_switch(self.turn)
            self.num_turns += 1
        else:
            self.bad_choice = True

    def reset(self):
        self.cell = Cell()
        self.num_turns = 0
        self.turn = ""
        self.bad_choice = False
        self.state = "P"

