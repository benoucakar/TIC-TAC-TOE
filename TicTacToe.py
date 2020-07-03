import random

class Cell:
    def __init__(self):
        self.cells = dict(enumerate(["."] * 9, 1))

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
    
    def sign_graphic(self, sign):
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
                test.oznaci_polje(space, "X")
                if test.check_win():
                    X_list.append(space)
                test.cells = dict(cell.cells)
                test.oznaci_polje(space, "O")
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

        
def input_promt_fixed(question, input_text, fail_text, choice_list):
    """Poenostva nadzor nad vhodnimi podatki iz konzole. Vprašanje / pričakovani odgovori / opomba, če vnos ni ustrezen / seznam ustreznih vnosov """
    while True:
        print(question)
        choice = input(f"{input_text}: ")
        if choice in choice_list:
            return choice
        else:
            print(fail_text)

def show_field_vanila(cell):
    print(" ------- ")
    print(f"| {cell.cells[7]} {cell.cells[8]} {cell.cells[9]} |")
    print(f"| {cell.cells[4]} {cell.cells[5]} {cell.cells[6]} |")
    print(f"| {cell.cells[1]} {cell.cells[2]} {cell.cells[3]} |")
    print(" ------- ")

def show_field_ultimate(cells_list):
    print(" " + "-" * 23 + " ")
    print(f"| {cells_list[7].cells[7]} {cells_list[7].cells[8]} {cells_list[7].cells[9]} | {cells_list[8].cells[7]} {cells_list[8].cells[8]} {cells_list[8].cells[9]} | {cells_list[9].cells[7]} {cells_list[9].cells[8]} {cells_list[9].cells[9]} |")
    print(f"| {cells_list[7].cells[4]} {cells_list[7].cells[5]} {cells_list[7].cells[6]} | {cells_list[8].cells[4]} {cells_list[8].cells[5]} {cells_list[8].cells[6]} | {cells_list[9].cells[4]} {cells_list[9].cells[5]} {cells_list[9].cells[6]} |")
    print(f"| {cells_list[7].cells[1]} {cells_list[7].cells[2]} {cells_list[7].cells[3]} | {cells_list[8].cells[1]} {cells_list[8].cells[2]} {cells_list[8].cells[3]} | {cells_list[9].cells[1]} {cells_list[9].cells[2]} {cells_list[9].cells[3]} |")
    print(" " + "-" * 23 + " ")
    print(f"| {cells_list[4].cells[7]} {cells_list[4].cells[8]} {cells_list[4].cells[9]} | {cells_list[5].cells[7]} {cells_list[5].cells[8]} {cells_list[5].cells[9]} | {cells_list[6].cells[7]} {cells_list[6].cells[8]} {cells_list[6].cells[9]} |")
    print(f"| {cells_list[4].cells[4]} {cells_list[4].cells[5]} {cells_list[4].cells[6]} | {cells_list[5].cells[4]} {cells_list[5].cells[5]} {cells_list[5].cells[6]} | {cells_list[6].cells[4]} {cells_list[6].cells[5]} {cells_list[6].cells[6]} |")
    print(f"| {cells_list[4].cells[1]} {cells_list[4].cells[2]} {cells_list[4].cells[3]} | {cells_list[5].cells[1]} {cells_list[5].cells[2]} {cells_list[5].cells[3]} | {cells_list[6].cells[1]} {cells_list[6].cells[2]} {cells_list[6].cells[3]} |")
    print(" " + "-" * 23 + " ")
    print(f"| {cells_list[1].cells[7]} {cells_list[1].cells[8]} {cells_list[1].cells[9]} | {cells_list[2].cells[7]} {cells_list[2].cells[8]} {cells_list[2].cells[9]} | {cells_list[3].cells[7]} {cells_list[3].cells[8]} {cells_list[3].cells[9]} |")
    print(f"| {cells_list[1].cells[4]} {cells_list[1].cells[5]} {cells_list[1].cells[6]} | {cells_list[2].cells[4]} {cells_list[2].cells[5]} {cells_list[2].cells[6]} | {cells_list[3].cells[4]} {cells_list[3].cells[5]} {cells_list[3].cells[6]} |")
    print(f"| {cells_list[1].cells[1]} {cells_list[1].cells[2]} {cells_list[1].cells[3]} | {cells_list[2].cells[1]} {cells_list[2].cells[2]} {cells_list[2].cells[3]} | {cells_list[3].cells[1]} {cells_list[3].cells[2]} {cells_list[3].cells[3]} |")
    print(" " + "-" * 23 + " ")

def start_game_2_vanila():
    game = Cell()
    turn = input_promt_fixed("Bi prvi igralec imel križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    num_turns = 0
    bad_choice = False
    print("Polja so številčena kot številčna tipkovnica.")
    while not game.check_win() and num_turns < 9:
        show_field_vanila(game)
        if bad_choice:
            print("To polje je že zasedeno.")
            bad_choice = False
        inp = int(input_promt_fixed(f"Igralec {turn} je na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        if game.oznaci_polje(inp, turn):
            turn = game.sign_switch(turn)
            num_turns += 1
        else:
            bad_choice = True
    show_field_vanila(game)
    if game.check_win():
        print(f"Čestitke {game.sign_switch(turn)}!")
    else:
        print("Igra je neodločena.")

def start_game_2_ultimate():
    master_celica = Cell()
    celica1 = Cell()
    celica2 = Cell()
    celica3 = Cell()
    celica4 = Cell()
    celica5 = Cell()
    celica6 = Cell()
    celica7 = Cell()
    celica8 = Cell()
    celica9 = Cell()
    game = ["&", celica1, celica2, celica3, celica4, celica5, celica6, celica7, celica8, celica9]
    turn = input_promt_fixed("Bi prvi igralec imel križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    num_turns = 0
    bad_choice = False
    print("Celice in polja so številčena kot številčna tipkovnica.")
    show_field_ultimate(game)
    inp_cell = int(input_promt_fixed(f"Za začetek sme {turn} izbrati poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    inp_space = int(input_promt_fixed(f"{turn} naj izbere še polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    game[inp_cell].oznaci_polje(inp_space, turn)
    inp_cell = inp_space
    turn = master_celica.sign_switch(turn)

    while not master_celica.check_win() and num_turns < 9:
        show_field_ultimate(game)
        if bad_choice:
            print("To polje je že zasedeno.")
            bad_choice = False

        current_cell = game[inp_cell]

        if master_celica.cells[inp_cell] == ".":
            inp_space = int(input_promt_fixed(f"{turn} naj izbere polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            if current_cell.oznaci_polje(inp_space, turn):
                if current_cell.check_win():
                    master_celica.oznaci_polje(inp_cell, turn)
                    num_turns += 1
                    current_cell.sign_graphic(turn)
                elif current_cell.check_draw():
                    master_celica.oznaci_polje(inp_cell, "+")
                    num_turns += 1
                    current_cell.Draw_graphic()
                inp_cell = inp_space
                turn = master_celica.sign_switch(turn)
            else:
                bad_choice = True
            
        elif master_celica.cells[inp_cell] != ".":    
            print(f"Ta celica je že zaključeno. {turn} lahko gre kamorkoli.")
            inp_cell = int(input_promt_fixed(f"{turn} naj izbere poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))

    show_field_ultimate(game)
    if master_celica.check_win():
        print(f"Čestitke {master_celica.sign_switch(turn)}!")
        show_field_vanila(master_celica)
    else:
        print("Igra je neodločena.")

def start_game_1_vanila():
    game = Cell()
    num_turns = 0
    player_mark = input_promt_fixed("Želite imeti križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    player_turn = "y" == input_promt_fixed("Želite biti prvi?", "y/n", "Žal je bil vnos neustrezen.", ["y", "n"])
    current_mark = player_mark if player_turn else game.sign_switch(player_mark)

    dif = input_promt_fixed("Izberite težavnostno stopnjo. Večje kot je število, težje bo.", "(1 - 4)", "Žal je bil vnos neustrezen.", ["1", "2", "3", "4"])
    bot = Bot(player_mark, not player_turn)
    if dif == "1":
        bot_generator = bot.vanila_dif_1(game)
    elif dif == "2":
        bot_generator = bot.vanila_dif_2(game)
    elif dif == "3":
        bot_generator = bot.vanila_dif_3(game)
    elif dif == "4":
        bot_generator = bot.vanila_dif_4(game)

    bad_choice = False
    print("Polja so številčena kot številčna tipkovnica.")
    while not game.check_win() and num_turns < 9:
        if bad_choice:
            print("To polje je že zasedeno.")
            bad_choice = False

        if player_turn:
            show_field_vanila(game)
            inp = int(input_promt_fixed(f"Ste na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        else:
            inp = next(bot_generator)

        if game.oznaci_polje(inp, current_mark):
            player_turn = not player_turn
            current_mark = game.sign_switch(current_mark)
            num_turns += 1
        else:
            bad_choice = True

    show_field_vanila(game)
    if game.check_win() and not player_turn:
        print("Čestitke!")
    elif game.check_win() and player_turn:
        print("Žal ste izgubili. Več sreče prihodnjič.")
    else:
        print("Igra je neodločena.")
    
def start_game_1_ultimate():
    master_celica = Cell()
    celica1 = Cell()
    celica2 = Cell()
    celica3 = Cell()
    celica4 = Cell()
    celica5 = Cell()
    celica6 = Cell()
    celica7 = Cell()
    celica8 = Cell()
    celica9 = Cell()
    game = ["&", celica1, celica2, celica3, celica4, celica5, celica6, celica7, celica8, celica9]
    num_master_turns = 0
    player_mark = input_promt_fixed("Želite imeti križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    player_turn = "y" == input_promt_fixed("Želite biti prvi?", "y/n", "Žal je bil vnos neustrezen.", ["y", "n"])
    master_bot = Bot(player_mark, not player_turn)
    bad_choice = False
    print("Celice in polja so številčena kot številčna tipkovnica.")
    current_mark = player_mark if player_turn else master_celica.sign_switch(player_mark)

    if player_turn:
        show_field_ultimate(game)
        inp_cell = int(input_promt_fixed(f"Za začetek smete {player_mark} izbrati poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        inp_space = int(input_promt_fixed(f"Sedaj {player_mark} izberite še polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    else:
        inp_cell = master_celica.random_free()
        inp_space = game[inp_cell].random_free()
    game[inp_cell].oznaci_polje(inp_space, current_mark)
    inp_cell = inp_space
    current_mark = master_celica.sign_switch(current_mark)
    player_turn = not player_turn

    while not master_celica.check_win() and num_master_turns < 9:
        show_field_ultimate(game)

        if bad_choice:
            print("To polje je že zasedeno.")
            bad_choice = False
        
        current_cell = game[inp_cell]

        if master_celica.cells[inp_cell] == ".":
            if player_turn:
                inp_space = int(input_promt_fixed(f"{player_mark} izberite polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            else:
                inp_space = master_bot.ultimate_incell_move(game, inp_cell)

            if current_cell.oznaci_polje(inp_space, current_mark):
                if current_cell.check_win():
                    master_celica.oznaci_polje(inp_cell, current_mark)
                    num_master_turns += 1
                    current_cell.sign_graphic(current_mark)
                elif current_cell.check_draw():
                    master_celica.oznaci_polje(inp_cell, "+")
                    num_master_turns += 1
                    current_cell.Draw_graphic()
                inp_cell = inp_space
                current_mark = master_celica.sign_switch(current_mark)
                player_turn = not player_turn
            else:
                bad_choice = True
            
        elif master_celica.cells[inp_cell] != ".":
            if player_turn:
                print("Lahko greste kamorkoli.")
                inp_cell = int(input_promt_fixed(f"{player_mark} izberite poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            else:
                inp_cell = master_celica.random_free()

    show_field_ultimate(game)
    if master_celica.check_win() and not player_turn:
        print("Čestitke!")
    elif master_celica.check_win() and player_turn:
        print("Žal ste izgubili. Več sreče prihodnjič.")
    else:
        print("Igra je neodločena.")


#start_game_1_vanila()
#start_game_2_vanila()
#start_game_2_ultimate()
#start_game_1_ultimate()

