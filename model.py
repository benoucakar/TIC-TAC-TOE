import random
import json

DATOTEKA_STANJA = 'stanje.json'

class Cell:
    """Definiramo 3 x 3 mrežo v obliki slovarja na kateri bomo igrali križce in krožce."""
    def __init__(self):
        self.spaces = dict(enumerate(["."] * 9, 1))

    def mark_field(self, n, znak):
        """Če je mogoče označi polje in vrne potrdilo."""
        if self.spaces[n] == ".":
            self.spaces[n] = znak
            return True
        else:
            return False

    def X_graphic(self):
        """Izriše X v celici."""
        self.spaces = {1 : "/", 2 : " ", 3 : "\\", 4 : " ", 5 : "X", 6 : " ", 7 : "\\", 8 : " ", 9 : "/"}

    def O_graphic(self):
        """Izriše O v celici."""
        self.spaces = {1 : "\\", 2 : "―", 3 : "/", 4 : "|", 5 : " ", 6 : "|", 7 : "/", 8 : "―", 9 : "\\"}
    
    def print_sign_graphic(self, sign):
        """Pomožna metoda za označevanje polja."""
        if sign == "X":
            self.X_graphic()
        elif sign == "O":
            self.O_graphic()

    def Draw_graphic(self):
        """Pobarva polje kar označuje neodločen izzid."""
        self.spaces = dict(enumerate(["+"] * 9, 1))

    def check_win(self):
        """Preveri, če je celica v zmagovalnem stanju."""
        win_situations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (3, 5, 7), (1, 5, 9)]
        for i, j, k in win_situations:
            if self.spaces[i] == self.spaces[j] == self.spaces[k] != "." and self.spaces[i] != "+":
                return True
        return False

    def check_draw(self):
        """Preveri, če je celica neodločena."""
        return not ("." in self.spaces.values() or self.check_win())
    
    def count_empty_space(self):
        """Prešteje koliko je praznih polj v celici."""
        count = 0
        for i in self.spaces.items():
            if i != ".":
                count += 1
        return count
    
    def random_free(self):
        """Vrne indeks za poljubno prazno polje."""
        return random.choice([key for key, value in self.spaces.items() if value == "."])

    @staticmethod
    def sign_switch(a):
        """Zamenja "X" in "O"."""
        if a == "X":
            return "O"
        elif a == "O":
            return "X"

class Bot:
    """Program, ki bo igral proti igralcu."""
    def __init__(self, player_mark, bot_first):
        self.player_mark = player_mark
        self.bot_first = bot_first

    def win_block(self, cell):
        """Če lahko zmaga celico, vrne ustrezen indeks. 
        Sicer, če lahko prepreči zmago, vrne ustrezen indeks. 
        Sicer vrne 0."""
        X_list = []
        O_list = []
        for space, sign in cell.spaces.items():
            test = Cell()
            if sign == ".":
                test.spaces = dict(cell.spaces)
                test.mark_field(space, "X")
                if test.check_win():
                    X_list.append(space)
                test.spaces = dict(cell.spaces)
                test.mark_field(space, "O")
                if test.check_win():
                    O_list.append(space)
        if self.player_mark == "O":
            return (X_list + O_list + [0])[0]
        elif self.player_mark == "X":
            return (O_list + X_list + [0])[0]
    
    def vanila_optimal(self, cell):
        """Generator za case-work za optimalno strategijo pri običajnih križcih in krožcih. Če ni optimalne poteze, vrne 0."""
        if self.bot_first: # Bot je prvi.
            yield 1 # Prazno igro začne v kotu.
            if cell.spaces[5] == self.player_mark: # Igralec da na sredino.
                yield 9
            else: # Igralec ne da na sredino.
                if self.player_mark == cell.spaces[9]:
                    yield 3
                    yield 7
                elif self.player_mark == cell.spaces[2] or self.player_mark == cell.spaces[8]:
                    yield 7
                    yield 5
                elif self.player_mark == cell.spaces[4] or self.player_mark == cell.spaces[6]:
                    yield 3
                    yield 5
                elif self.player_mark == cell.spaces[7]:
                    yield 9
                    yield 3
                elif self.player_mark == cell.spaces[3]:
                    yield 9
                    yield 7        
        else: # Bot je drugi.
            if cell.spaces[5] == self.player_mark: # Igralec da na sredino.
                yield 1
                yield 3
            elif self.player_mark in [cell.spaces[i] for i in [1, 3, 7, 9]]: # Igralec da v kot.
                yield 5 
                if self.player_mark == cell.spaces[1] == cell.spaces[9] or self.player_mark == cell.spaces[3] == cell.spaces[7]: # Igralec igra diagonalno.
                    yield 2
                elif self.player_mark == cell.spaces[1]:
                    yield 9
                elif self.player_mark == cell.spaces[3]:
                    yield 7
                elif self.player_mark == cell.spaces[7]:
                    yield 3
                elif self.player_mark == cell.spaces[9]:
                    yield 1
        # Če da igralec na rob, je vseeno.
        while True: # Če ni optimalne poteze, vrne 0.
            yield 0

    def vanila_dif_1(self, cell):
        """Nastavi generator bota težavnosti 1. Igra naključno."""
        while True:
            yield cell.random_free()
    
    def vanila_dif_2(self, cell):
        """Nastavi generator bota težavnosti 2. Včasih naredi optimalno potezo in kdaj ne zmaga ali prepreči zmage."""
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
        """Nastavi generator težavnosti 3. Načeloma igra optimalno. Redko se zmoti, da ne zmaga ali prepreči zmage."""
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
        """Nastavi generator bota težavnosti 4. Igra optimalno."""
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
        """Vrne indeks celice, ki ima največ praznih polj. Če jih je več takih, vrne naključnega."""
        scores = []
        for i in range(1, 9):
            scores.append((i, cell_list[i].count_empty_space()))
        random.shuffle(scores)
        return max(scores, key=lambda par: par[1])[0]

    def ultimate_incell_move(self, cell_list, inp_cell):
        """Skuša zmagati, nato preprečiti zmago. Sicer vrne indeks, ki vodi v najbolj prazno celico."""
        if self.win_block(cell_list[inp_cell]) != 0:
            return self.win_block(cell_list[inp_cell])
        else:
            flag = True
            while flag:
                kand = self.ultimate_density(cell_list)
                if cell_list[inp_cell].spaces[kand] == ".":
                    flag = False
            return kand

class Vanila_2:
    """Običajni križci in krožci za dva igralca.
    "P" - začetek igra, "M" - glavni del igre, "E" - konec igre."""
    def __init__(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

    def choose_parameters(self, first_player_mark):
        """Določi parametre, ki si jih izbere igralec."""
        self.mark = first_player_mark
    
    def make_move(self, inp_space):
        """Naredi potezo."""
        if self.cell.mark_field(inp_space, self.mark):
            self.mark = self.cell.sign_switch(self.mark)
            self.num_turns += 1

    def reset(self):
        """Ponastavi parametre."""
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

class Vanila_1:
    """Običajni križci in krožci za enega igralca.
    "P" - začetek igra, "M" - glavni del igre, "E" - konec igre."""
    def __init__(self):
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"
        
    def choose_parameters(self, player_mark, player_turn, difficulty):
        """Določi parametre, ki si jih izbere igralec."""
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
        """Naredi potezo."""
        if self.cell.mark_field(inp_space, self.current_mark):
            self.player_turn = not self.player_turn
            self.current_mark = self.cell.sign_switch(self.current_mark)
            self.num_turns += 1
            return True
        else:
            return False

    def reset(self):
        """Ponastavi parametre."""
        self.cell = Cell()
        self.num_turns = 0
        self.state = "P"

class Ultimate_2:
    """Ultimativni križci in krožci za dva igralca.
    "P" - začetek igra, "M" - glavni del igre, "E" - konec igre."""
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
        self.move_in_big_cell = True
        self.inp_cell = 0
        self.inp_space = 0

    def choose_parameters(self, first_player_mark):
        """Določi parametre, ki si jih izbere igralec."""
        self.mark = first_player_mark
    
    def move_in_small_cell(self, current_cell):
        """Naredi potezo v celici."""
        if current_cell.mark_field(self.inp_space, self.mark):
            if current_cell.check_win():
                self.master_cell.mark_field(self.inp_cell, self.mark)
                self.num_master_turns += 1
                current_cell.print_sign_graphic(self.mark)
            elif current_cell.check_draw():
                self.master_cell.mark_field(self.inp_cell, "+")
                self.num_master_turns += 1
                current_cell.Draw_graphic()
            self.inp_cell = self.inp_space
            self.mark = self.master_cell.sign_switch(self.mark)

    def reset(self):
        """Ponastavi parametre."""
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
        self.move_in_big_cell = True
        self.inp_cell = 0
        self.inp_space = 0

class Ultimate_1:
    """Ultimativni križci in krožci za enega igralca.
    "P" - začetek igra, "M" - glavni del igre, "E" - konec igre."""
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
        self.move_in_big_cell = True
        self.inp_cell = 0
        self.inp_space = 0
        self.last_inp_cell = 0

    def choose_parameters(self, player_mark, player_turn):
        """Določi parametre, ki si jih izbere igralec."""
        self.player_mark = player_mark
        self.player_turn = player_turn
        self.master_bot = Bot(self.player_mark, not self.player_turn)
        self.current_mark = self.player_mark if self.player_turn else self.master_cell.sign_switch(self.player_mark)

    def move_in_small_cell(self, current_cell):
        """Naredi potezo v celici."""
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

    def reset(self):
        """Ponastavi parametre."""
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
        self.move_in_big_cell = True
        self.inp_cell = 0
        self.inp_space = 0
        self.last_inp_cell = 0

class User_tracker:
    """Funkcije, ki sledijo uporabnikom."""
    def __init__(self):
        self.users = {}
    
    def free_id(self):
        """Vrne prost id."""
        if len(self.users) == 0:
            return 0
        else:
            return max(self.users.keys()) + 1
    
    def new_user(self):
        """Novemu uporabniku dodeli id in vse 4 igre. Nato vrne id."""
        user_id = self.free_id()
        vanila_1 = Vanila_1()
        vanila_2 = Vanila_2()
        ultimate_1 = Ultimate_1()
        ultimate_2 = Ultimate_2()
        self.users[user_id] = (vanila_1, vanila_2, ultimate_1, ultimate_2)
        return user_id

class Data_manager:
    """Funkcije, ki skrbijo za podatke."""
    def __init__(self, file):
        self.file = file
        self.load_data_from_file()

    def load_data_from_file(self): 
        """Naloži slovar iz datoteke."""
        with open(self.file, 'r', encoding='utf-8') as f: 
            self.data = json.load(f)

    def dump_data_to_file(self):
        """Zapiše slovar v datoteko."""
        with open(self.file, 'w', encoding='utf-8') as f: 
            json.dump(self.data, f)
    
    def data_for_stats(self):
        """Določi vrednosti za statistiko."""
        self.ended_V1 = self.data["ended_V1"]
        self.ended_V2 = self.data["ended_V2"]
        self.ended_U1 = self.data["ended_U1"]
        self.ended_U2 = self.data["ended_U2"]
        self.ended_games = self.ended_V1 + self.ended_V2 + self.ended_U1 + self.ended_U2
        self.ended_draw = self.data["ended_draw"]
        self.player_win_X = self.data["player_win_X"]
        self.player_win_O = self.data["player_win_O"]
        self.player_beat_bot = self.data["player_beat_bot"]