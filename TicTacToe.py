class Cell:
    def __init__(self):
        self.cells = {1 : ".", 2 : ".", 3 : ".", 4 : ".", 5 : ".", 6 : ".", 7 : ".", 8 : ".", 9 : "."}
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
            return True
        elif self.cells[4] == self.cells[5] == self.cells[6] and self.cells[4] != ".": #srednja vrsta
            return True
        elif self.cells[7] == self.cells[8] == self.cells[9] and self.cells[7] != ".": #zgornja vrsta
            return True
        elif self.cells[1] == self.cells[4] == self.cells[7] and self.cells[1] != ".": #levi stolpec
            return True
        elif self.cells[2] == self.cells[5] == self.cells[8] and self.cells[2] != ".": #srednji stolpec
            return True
        elif self.cells[3] == self.cells[6] == self.cells[9] and self.cells[3] != ".": #desni stolpec
            return True
        elif self.cells[3] == self.cells[5] == self.cells[7] and self.cells[3] != ".": #pad diagonala
            return True
        elif self.cells[1] == self.cells[5] == self.cells[9] and self.cells[1] != ".": #narašč diagonala
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


def start_game_2_vanila():
    game = Cell()
    turn = input_promt_fixed("Bi prvi igralec imel križce ali krožce?", "X/O", "Žal je bil vnos neustrezen.", ["X", "O"])
    win = ""
    num_turns = 0
    while not game.check_win() and num_turns < 9:
        show_field_vanila(game)
        inp = int(input_promt_fixed(f"Igralec {turn} je na potezi!", "(1 - 9)", "Žal je bil vnos neustrezen.", [str(i) for i in range(1, 10)]))
        if turn == "X":
            if game.cross(inp):
                turn = "O"
                win = "X"
                num_turns += 1
            else:
                None
        elif turn == "O":
            if game.nought(inp):
                turn = "X"
                win = "O"
                num_turns += 1
            else:
                None
    show_field_vanila(game)
    if game.check_win():
         print(f"Čestitke {win}!")
    else:
        print("Igra je neodločena.")


start_game_2_vanila()