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
    
    def ultimate_density(self, cell_list):
        scores = []
        for i in range(1, 9):
            scores.append((i, cell_list[i].count_empty_space()))
        random.shuffle(scores)
        return max(scores, key=lambda par: par[1])[0]

    def ultimate_incell_move(self, cell_list, inp_cell):
        if self.win_block(cell_list[inp_cell]) != 0:
            return self.win_block(cell_list[inp_cell])
        else:
            flag = True
            while flag:
                kand = self.ultimate_density(cell_list)
                if cell_list[inp_cell].cells[kand] == ".":
                    flag = False
            return kand

class Vanila_2:
    # P - pre game, M - main game, E - end game
    def __init__(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

    def choose_parameters(self, first_player_mark):
        self.turn = first_player_mark
    
    def make_move(self, inp_space):
        if self.cell.mark_field(inp_space, self.turn):
            self.turn = self.cell.sign_switch(self.turn)
            self.num_turns += 1

    def reset(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

class Vanila_1:
    # P - pre game, M - main game, E - end game
    def __init__(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"
        
    def choose_parameters(self, player_mark, player_turn, difficulty):
        self.player_mark = player_mark
        self.player_turn = player_turn
        self.current_mark = self.player_mark if self.player_turn else self.cell.sign_switch(self.player_mark)
        self.dif = difficulty
        self.bot = Bot(self.player_mark, not self.player_turn)
        if self.dif == "1":
            self.bot_generator = self.bot.vanila_dif_1(self.cell)
        elif self.dif == "2":
            self.bot_generator = self.bot.vanila_dif_2(self.cell)
        elif self.dif == "3":
            self.bot_generator = self.bot.vanila_dif_3(self.cell)
        elif self.dif == "4":
            self.bot_generator = self.bot.vanila_dif_4(self.cell)

    def make_move(self, inp_space):
        if self.cell.mark_field(inp_space, self.current_mark):
            self.player_turn = not self.player_turn
            self.current_mark = self.cell.sign_switch(self.current_mark)
            self.num_turns += 1
            return True
        else:
            return False

    def reset(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

class Ultimate_2:
    # P - pre game, I - initial move, M - main game, E - end game
    def __init__(self):
        self.master_cell = Cell()
        self.cell1 = Cell()
        self.cell2 = Cell()
        self.cell3 = Cell()
        self.cell4 = Cell()
        self.cell5 = Cell()
        self.cell6 = Cell()
        self.cell7 = Cell()
        self.cell8 = Cell()
        self.cell9 = Cell()
        self.cell_list = ["&", self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8, self.cell9]
        self.num_master_turns = 0
        self.state = "P"
        self.move_in_big_cell = False

    def choose_parameters(self, first_player_mark):
        self.turn = first_player_mark

    def initial_move(self, inp_cell, inp_space):
        self.inp_cell = inp_cell
        self.inp_space = inp_space
        self.cell_list[self.inp_cell].mark_field(self.inp_space, self.turn)
        self.inp_cell = self.inp_space
        self.turn = self.master_cell.sign_switch(self.turn)
    
    def reset(self):
        self.master_cell = Cell()
        self.cell1 = Cell()
        self.cell2 = Cell()
        self.cell3 = Cell()
        self.cell4 = Cell()
        self.cell5 = Cell()
        self.cell6 = Cell()
        self.cell7 = Cell()
        self.cell8 = Cell()
        self.cell9 = Cell()
        self.cell_list = ["&", self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8, self.cell9]
        self.num_master_turns = 0
        self.state = "P"
        self.move_in_big_cell = False

    def move_in_small_cell(self, current_cell):
        if current_cell.mark_field(self.inp_space, self.turn):
            if current_cell.check_win():
                self.master_cell.mark_field(self.inp_cell, self.turn)
                self.num_master_turns += 1
                current_cell.print_sign_graphic(self.turn)
            elif current_cell.check_draw():
                self.master_cell.mark_field(self.inp_cell, "+")
                self.num_master_turns += 1
                current_cell.Draw_graphic()
            self.inp_cell = self.inp_space
            self.turn = self.master_cell.sign_switch(self.turn)

class Ultimate_1:
    # P - pre game, I - initial move, M - main game, E - end game
    def __init__(self):
        self.master_cell = Cell()
        self.cell1 = Cell()
        self.cell2 = Cell()
        self.cell3 = Cell()
        self.cell4 = Cell()
        self.cell5 = Cell()
        self.cell6 = Cell()
        self.cell7 = Cell()
        self.cell8 = Cell()
        self.cell9 = Cell()
        self.cell_list = ["&", self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8, self.cell9]
        self.num_master_turns = 0
        self.state = "P"
        self.move_in_big_cell = False

    def choose_parameters(self, player_mark, player_turn):
        self.player_mark = player_mark
        self.player_turn = player_turn
        self.master_bot = Bot(self.player_mark, not self.player_turn)
        self.current_mark = self.player_mark if self.player_turn else self.master_cell.sign_switch(self.player_mark)

    def initial_move(self, inp_cell, inp_space):
        self.inp_cell = inp_cell
        self.inp_space = inp_space
        self.cell_list[self.inp_cell].mark_field(self.inp_space, self.current_mark)
        self.last_inp_cell = self.inp_cell
        self.inp_cell = self.inp_space
        self.current_mark = self.master_cell.sign_switch(self.current_mark)
        self.player_turn = not self.player_turn

    def reset(self):
        self.master_cell = Cell()
        self.cell1 = Cell()
        self.cell2 = Cell()
        self.cell3 = Cell()
        self.cell4 = Cell()
        self.cell5 = Cell()
        self.cell6 = Cell()
        self.cell7 = Cell()
        self.cell8 = Cell()
        self.cell9 = Cell()
        self.cell_list = ["&", self.cell1, self.cell2, self.cell3, self.cell4, self.cell5, self.cell6, self.cell7, self.cell8, self.cell9]
        self.num_master_turns = 0
        self.state = "P"
        self.move_in_big_cell = False

    def move_in_small_cell(self, current_cell):
        if current_cell.mark_field(self.inp_space, self.current_mark):
            if current_cell.check_win():
                self.master_cell.mark_field(self.inp_cell, self.current_mark)
                self.num_master_turns += 1
                current_cell.print_sign_graphic(self.current_mark)
            elif current_cell.check_draw():
                self.master_cell.mark_field(self.inp_cell, "+")
                self.num_master_turns += 1
                current_cell.Draw_graphic()
            self.last_inp_cell = self.inp_cell
            self.inp_cell = self.inp_space
            self.current_mark = self.master_cell.sign_switch(self.current_mark)
            self.player_turn = not self.player_turn

class User_tracker:
    def __init__(self):
        self.users = {}
    
    def free_id(self):
        if len(self.users) == 0:
            return 0
        else:
            return max(self.users.keys()) + 1
    
    def new_user(self):
        user_id = self.free_id()
        vanila_1 = Vanila_1()
        vanila_2 = Vanila_2()
        ultimate_1 = Ultimate_1()
        ultimate_2 = Ultimate_2()
        self.users[user_id] = (vanila_1, vanila_2, ultimate_1, ultimate_2)
        return user_id
