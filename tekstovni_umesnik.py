from model import *

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

class vanila_2:
    def __init__(self):
        self.game = Cell()
        self.num_turns = 0
        self.turn = input_promt_fixed("Bi prvi igralec imel križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
        self.bad_choice = False
    
    def check_bad_move(self):
        if self.bad_choice:
            print("To polje je že zasedeno.")
            self.bad_choice = False
    
    def make_move(self):
        inp = int(input_promt_fixed(f"Igralec {self.turn} je na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        if self.game.mark_field(inp, self.turn):
            self.turn = self.game.sign_switch(self.turn)
            self.num_turns += 1
        else:
            self.bad_choice = True

    def main_game(self):
        print("Polja so številčena kot številčna tipkovnica.")
        while not self.game.check_win() and self.num_turns < 9:
            show_field_vanila(self.game)
            self.check_bad_move()
            self.make_move()
            
    def end_game(self):
        show_field_vanila(self.game)
        if self.game.check_win():
            print(f"Čestitke {self.game.sign_switch(self.turn)}!")
        else:
            print("Igra je neodločena.")
        input("Ko željite zaključiti, pritisnite ENTER.")

def start_vanila_2():
    game = vanila_2()
    game.main_game()
    game.end_game()

class vanila_1:
    def __init__(self):
        self.game = Cell()
        self.num_turns = 0
        self.player_mark = input_promt_fixed("Želite imeti križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
        self.player_turn = "y" == input_promt_fixed("Želite biti prvi?", "y/n", "Žal je bil vnos neustrezen.", ["y", "n"])
        self.current_mark = self.player_mark if self.player_turn else self.game.sign_switch(self.player_mark)
        self.bad_choice = False
        self.dif = input_promt_fixed("Izberite težavnostno stopnjo. Večje kot je število, težje bo.", "(1 - 4)", "Žal je bil vnos neustrezen.", ["1", "2", "3", "4"])
        self.bot = Bot(self.player_mark, not self.player_turn)
        if self.dif == "1":
            self.bot_generator = self.bot.vanila_dif_1(self.game)
        elif self.dif == "2":
            self.bot_generator = self.bot.vanila_dif_2(self.game)
        elif self.dif == "3":
            self.bot_generator = self.bot.vanila_dif_3(self.game)
        elif self.dif == "4":
            self.bot_generator = self.bot.vanila_dif_4(self.game)
    
    def check_bad_move(self):
        if self.bad_choice:
            print("To polje je že zasedeno.")
            self.bad_choice = False
    
    def make_move(self):
        if self.player_turn:
            show_field_vanila(self.game)
            inp = int(input_promt_fixed(f"Ste na potezi.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        else:
            inp = next(self.bot_generator)

        if self.game.mark_field(inp, self.current_mark):
            self.player_turn = not self.player_turn
            self.current_mark = self.game.sign_switch(self.current_mark)
            self.num_turns += 1
        else:
            self.bad_choice = True

    def main_game(self):
        print("Polja so številčena kot številčna tipkovnica.")
        while not self.game.check_win() and self.num_turns < 9:
            self.check_bad_move()
            self.make_move()
    
    def end_game(self):
        show_field_vanila(self.game)
        if self.game.check_win() and not self.player_turn:
            print("Čestitke!")
        elif self.game.check_win() and self.player_turn:
            print("Žal ste izgubili. Več sreče prihodnjič.")
        else:
            print("Igra je neodločena.")
        input("Ko željite zaključiti, pritisnite ENTER.")

def start_vanila_1():
    game = vanila_1()
    game.main_game()
    game.end_game()

def start_game_2_ultimate():
    master_cell = Cell()
    cell1 = Cell()
    cell2 = Cell()
    cell3 = Cell()
    cell4 = Cell()
    cell5 = Cell()
    cell6 = Cell()
    cell7 = Cell()
    cell8 = Cell()
    cell9 = Cell()
    game = ["&", cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]
    turn = input_promt_fixed("Bi prvi igralec imel križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    num_turns = 0
    bad_choice = False
    print("Celice in polja so številčena kot številčna tipkovnica.")

    show_field_ultimate(game)
    inp_cell = int(input_promt_fixed(f"Za začetek sme {turn} izbrati poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    inp_space = int(input_promt_fixed(f"{turn} naj izbere še polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    game[inp_cell].mark_field(inp_space, turn)
    inp_cell = inp_space
    turn = master_cell.sign_switch(turn)

    while not master_cell.check_win() and num_turns < 9:
        show_field_ultimate(game)
        
        if bad_choice:
            print("To polje je že zasedeno.")
            bad_choice = False

        current_cell = game[inp_cell]

        if master_cell.cells[inp_cell] == ".":
            inp_space = int(input_promt_fixed(f"{turn} naj izbere polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            if current_cell.mark_field(inp_space, turn):
                if current_cell.check_win():
                    master_cell.mark_field(inp_cell, turn)
                    num_turns += 1
                    current_cell.print_sign_graphic(turn)
                elif current_cell.check_draw():
                    master_cell.mark_field(inp_cell, "+")
                    num_turns += 1
                    current_cell.Draw_graphic()
                inp_cell = inp_space
                turn = master_cell.sign_switch(turn)
            else:
                bad_choice = True
            
        elif master_cell.cells[inp_cell] != ".":    
            print(f"Ta cell je že zaključeno. {turn} lahko gre kamorkoli.")
            inp_cell = int(input_promt_fixed(f"{turn} naj izbere poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))

    show_field_ultimate(game)
    if master_cell.check_win():
        print(f"Čestitke {master_cell.sign_switch(turn)}!")
        show_field_vanila(master_cell)
    else:
        print("Igra je neodločena.")
    input("Ko željite zaključiti, pritisnite ENTER.")

def start_game_1_ultimate():
    master_cell = Cell()
    cell1 = Cell()
    cell2 = Cell()
    cell3 = Cell()
    cell4 = Cell()
    cell5 = Cell()
    cell6 = Cell()
    cell7 = Cell()
    cell8 = Cell()
    cell9 = Cell()
    game = ["&", cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]
    num_master_turns = 0
    player_mark = input_promt_fixed("Želite imeti križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    player_turn = "y" == input_promt_fixed("Želite biti prvi?", "y/n", "Žal je bil vnos neustrezen.", ["y", "n"])
    master_bot = Bot(player_mark, not player_turn)
    bad_choice = False
    current_mark = player_mark if player_turn else master_cell.sign_switch(player_mark)
    print("Celice in polja so številčena kot številčna tipkovnica.")

    if player_turn:
        show_field_ultimate(game)
        inp_cell = int(input_promt_fixed(f"Za začetek smete {player_mark} izbrati poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        inp_space = int(input_promt_fixed(f"Sedaj {player_mark} izberite še polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    else:
        inp_cell = master_cell.random_free()
        inp_space = game[inp_cell].random_free()
    game[inp_cell].mark_field(inp_space, current_mark)
    last_inp_cell = inp_cell
    inp_cell = inp_space
    current_mark = master_cell.sign_switch(current_mark)
    player_turn = not player_turn

    while not master_cell.check_win() and num_master_turns < 9:
        if player_turn:
            print(f"Računalnik je v celici {last_inp_cell} izbral polje {inp_cell}.")
            show_field_ultimate(game)

        if bad_choice:
            if player_turn:
                print("To polje je že zasedeno.")
            bad_choice = False
        
        current_cell = game[inp_cell]

        if master_cell.cells[inp_cell] == ".":
            if player_turn:
                inp_space = int(input_promt_fixed(f"{player_mark} izberite polje v celici {inp_cell}.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            else:
                inp_space = master_bot.ultimate_incell_move(game, inp_cell)

            if current_cell.mark_field(inp_space, current_mark):
                if current_cell.check_win():
                    master_cell.mark_field(inp_cell, current_mark)
                    num_master_turns += 1
                    current_cell.print_sign_graphic(current_mark)
                elif current_cell.check_draw():
                    master_cell.mark_field(inp_cell, "+")
                    num_master_turns += 1
                    current_cell.Draw_graphic()
                last_inp_cell = inp_cell
                inp_cell = inp_space
                current_mark = master_cell.sign_switch(current_mark)
                player_turn = not player_turn
            else:
                bad_choice = True
            
        elif master_cell.cells[inp_cell] != ".":
            if player_turn:
                print("Lahko greste kamorkoli.")
                inp_cell = int(input_promt_fixed(f"{player_mark} izberite poljubno celico.", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
            else:
                inp_cell = master_cell.random_free()

    print(f"Računalnik je v celici {last_inp_cell} izbral polje {inp_cell}.")
    show_field_ultimate(game)
    if master_cell.check_win() and not player_turn:
        print("Čestitke!")
    elif master_cell.check_win() and player_turn:
        print("Žal ste izgubili. Več sreče prihodnjič.")
    else:
        print("Igra je neodločena.")
    input("Ko željite zaključiti, pritisnite ENTER.")