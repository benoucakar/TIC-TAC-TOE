import random

class Cell:
    def __init__(self):
        self.cells = {1 : ".", 2 : ".", 3 : ".", 4 : ".", 5 : ".", 6 : ".", 7 : ".", 8 : ".", 9 : "."}
    def cross(self, n):
        if self.cells[n] == ".":
            self.cells[n] = "X"
            return True
        else:
            print("To polje je že zasedeno.")
            return False
    def nought(self, n):
        if self.cells[n] == ".":
            self.cells[n] = "O"
            return True
        else:
            print("To polje je že zasedeno.")
            return False
    def draw(self, n):
        if self.cells[n] == ".":
            self.cells[n] = "+"
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
        if self.cells[1] == self.cells[2] == self.cells[3] != ".": #spodnja vrsta
            return (True, self.cells[1])
        elif self.cells[4] == self.cells[5] == self.cells[6] != ".": #srednja vrsta
            return (True, self.cells[4])
        elif self.cells[7] == self.cells[8] == self.cells[9] != ".": #zgornja vrsta
            return (True, self.cells[7])
        elif self.cells[1] == self.cells[4] == self.cells[7] != ".": #levi stolpec
            return (True, self.cells[1])
        elif self.cells[2] == self.cells[5] == self.cells[8] != ".": #srednji stolpec
            return (True, self.cells[2])
        elif self.cells[3] == self.cells[6] == self.cells[9] != ".": #desni stolpec
            return (True, self.cells[3])
        elif self.cells[3] == self.cells[5] == self.cells[7] != ".": #pad diagonala
            return (True, self.cells[3])
        elif self.cells[1] == self.cells[5] == self.cells[9] != ".": #narašč diagonala
            return (True, self.cells[1])
        else:
            return (False, None)
    def check_draw(self):
        return not ("." in self.cells.values() or self.check_win()[0])

def sign_switch(a):
    if a == "X":
        return "O"
    elif a == "O":
        return "X"

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
    print("Polja so številčena kot številčna tipkovnica.")
    while not game.check_win()[0] and num_turns < 9:
        show_field_vanila(game)
        inp = int(input_promt_fixed(f"Igralec {turn} je na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        if turn == "X":
            if game.cross(inp):
                turn = sign_switch(turn)
                num_turns += 1
        elif turn == "O":
            if game.nought(inp):
                turn = sign_switch(turn)
                num_turns += 1
    show_field_vanila(game)
    if game.check_win()[0]:
        print(f"Čestitke {sign_switch(turn)}!")
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
    print("Celice in polja so številčena kot številčna tipkovnica.")
    show_field_ultimate(game)
    inp_cell = int(input_promt_fixed(f"Za začetek sme {turn} izbrati poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    inp_space = int(input_promt_fixed(f"{turn} naj izbere še polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    if turn == "X":
        game[inp_cell].cross(inp_space)
    elif turn == "O":
        game[inp_cell].nought(inp_space)
    inp_cell = inp_space
    turn = sign_switch(turn)

    while not master_celica.check_win()[0] and num_turns < 9:
        show_field_ultimate(game)
        current_cell = game[inp_cell]        
        if master_celica.cells[inp_cell] == ".":
            inp_space = int(input_promt_fixed(f"{turn} naj izbere polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            if turn == "X":
                if current_cell.cross(inp_space):
                    turn = sign_switch(turn)
                    if current_cell.check_win()[0]:
                        master_celica.cross(inp_cell)
                        num_turns += 1
                        current_cell.X_graphic()
                    elif current_cell.check_draw():
                        master_celica.draw(inp_cell)
                        num_turns += 1
                        current_cell.Draw_graphic()
                    inp_cell = inp_space
            elif turn == "O":
                if current_cell.nought(inp_space):
                    turn = sign_switch(turn)
                    if current_cell.check_win()[0]:
                        master_celica.nought(inp_cell)
                        num_turns += 1
                        current_cell.O_graphic()
                    elif current_cell.check_draw():
                        master_celica.draw(inp_cell)
                        num_turns += 1
                        current_cell.Draw_graphic()
                    inp_cell = inp_space
        elif master_celica.cells[inp_cell] != ".":    
            print(f"Ta celica je že zaključeno. {turn} lahko gre kamorkoli.")
            inp_cell = int(input_promt_fixed(f"{turn} naj izbere poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))

    show_field_ultimate(game)
    if master_celica.check_win()[0]:
        print(f"Čestitke {sign_switch(turn)}!")
    else:
        print("Igra je neodločena.")

def bot_win_block(cell, mark):
    X_list = []
    O_list = []
    for space, sign in cell.cells.items():
        test = Cell()
        if sign == ".":
            test.cells = dict(cell.cells)
            test.cross(space)
            if test.check_win()[0]:
                X_list.append(space)
            test.cells = dict(cell.cells)
            test.nought(space)
            if test.check_win()[0]:
                O_list.append(space)
    if mark == "X":
        return (X_list + O_list + [0])[0]
    elif mark == "O":
        return (O_list + X_list + [0])[0]

def start_game_1_vanila():
#   mark = input_promt_fixed("Želite imeti križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    mark = "X"
#   player_first = input_promt_fixed("Želite biti prvi?", "y/n", "Žal je bil vnos neustrezen.", ["y", "n"])
#   igralec prvi
#   tezavnost = input_promt_fixed("Izberite težavnostno stopnjo. Večje kot je število, težje bo.", "(1 - 4)", "Žal je bil vnos neustrezen.", ["1", "2", "3", "4"])
#    player_turn = player_first == "y"
    player_turn = True
    bot_memory = [i for i in range(1, 10)]
    game = Cell()
    num_turns = 0
    print("Polja so številčena kot številčna tipkovnica.")
    while not game.check_win()[0] and num_turns < 9:
        if player_turn:
            show_field_vanila(game)
            inp = int(input_promt_fixed(f"Ste na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        else:
            if bot_win_block(game, "O") == 0:
                None
            else:
                inp = bot_win_block(game, "O")
        
        if player_turn:
            if game.cross(inp):
                player_turn = not player_turn
                num_turns += 1
        else:
            if game.nought(inp):
                player_turn = not player_turn
                num_turns += 1
    show_field_vanila(game)
    if game.check_win()[0] and not player_turn:
        print("Čestitke!")
    elif game.check_win()[0] and player_turn:
        print("Žal ste izgubili. Več sreče prihodnjič.")
    else:
        print("Igra je neodločena.")
        


# bot_win_block(test, "O")
#start_game_2_vanila()
#start_game_2_ultimate()
test = Cell()