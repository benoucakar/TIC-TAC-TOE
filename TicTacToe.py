class Cell:
    def __init__(self):
        self.cells = {1 : ".", 2 : ".", 3 : ".", 4 : ".", 5 : ".", 6 : ".", 7 : ".", 8 : ".", 9 : "."}
        self.winner = ""
    def cross(self, n):
        if self.cells[n] == ".":
            self.cells[n] = "X"
            return True
        else:
            return False
    def nought(self, n):
        if self.cells[n] == ".":
            self.cells[n] = "O"
            return True
        else:
            return False
    def check_win(self):
        if self.cells[1] == self.cells[2] == self.cells[3] and self.cells[1] != ".": #spodnja vrsta
            self.winner = self.cells[1]
            return True
        elif self.cells[4] == self.cells[5] == self.cells[6] and self.cells[4] != ".": #srednja vrsta
            self.winner = self.cells[4]
            return True
        elif self.cells[7] == self.cells[8] == self.cells[9] and self.cells[7] != ".": #zgornja vrsta
            self.winner = self.cells[7]
            return True
        elif self.cells[1] == self.cells[4] == self.cells[7] and self.cells[1] != ".": #levi stolpec
            self.winner = self.cells[1]
            return True
        elif self.cells[2] == self.cells[5] == self.cells[8] and self.cells[2] != ".": #srednji stolpec
            self.winner = self.cells[2]
            return True
        elif self.cells[3] == self.cells[6] == self.cells[9] and self.cells[3] != ".": #desni stolpec
            self.winner = self.cells[3]
            return True
        elif self.cells[3] == self.cells[5] == self.cells[7] and self.cells[3] != ".": #pad diagonala
            self.winner = self.cells[3]
            return True
        elif self.cells[1] == self.cells[5] == self.cells[9] and self.cells[1] != ".": #narašč diagonala
            self.winner = self.cells[1]
            return True
        else:
            return False


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
    while not game.check_win() and num_turns < 9:
        show_field_vanila(game)
        inp = int(input_promt_fixed(f"Igralec {turn} je na potezi!", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        if turn == "X":
            if game.cross(inp):
                turn = "O"
                num_turns += 1
            else:
                None
        elif turn == "O":
            if game.nought(inp):
                turn = "X"
                num_turns += 1
            else:
                None
    show_field_vanila(game)
    if game.check_win():
        print(f"Čestitke {game.winner}!")
    else:
        print("Igra je neodločena.")

def start_game_2_ultimate():
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
    turn = "X"
    print("Polja so številčena kot številčna tipkovnica.")
    show_field_ultimate(game)
    inp_cell = int(input_promt_fixed(f"{turn} sme izbrati poljubno celico", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    inp_space = int(input_promt_fixed(f"{turn} naj izbere še polje v celici {inp_cell}", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
    game[inp_cell].cross(inp_space)
    show_field_ultimate(game)
    turn = "O"
    while True:
        if turn == "X":
            None
        elif turn == "O":
            None
