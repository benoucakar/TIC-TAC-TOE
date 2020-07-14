import bottle
from model import *

COOKIE = "user_id"
SECRET = "Zemlja je torus."

user_tracker = User_tracker()
data_manager = Data_manager(DATOTEKA_STANJA)

# Prva stran in dodelitev piškotkov.

@bottle.get("/")
def index():
    """Preusmeri na index.html"""
    return bottle.template("index.html")

@bottle.post("/")
def new_user():
    """Novemu uporabniku določi indeks, ga shrani v piškotek in preusmerin na domov.html"""
    user_id = user_tracker.new_user()
    bottle.response.set_cookie(COOKIE, str(user_id), path='/', secret=SECRET)
    bottle.redirect("/domov/")

# Klicanje in prikaz statičnih strani.

@bottle.get("/domov/")
def domov():
    """Preusmeri na index.html"""
    return bottle.template("domov.html")

@bottle.get("/igre/")
def igra():
    """Preusmeri na igre.html"""
    return bottle.template("igre.html")

@bottle.get("/pravila/")
def pravila():
    """Preusmeri na pravila.html"""
    return bottle.template("pravila.html")

@bottle.get("/statistika/")
def statistika():
    """Posodobi podatke in preusmeri na statistika.html"""
    data_manager.load_data_from_file()
    data_manager.data_for_stats()
    return bottle.template("statistika.html", data_manager=data_manager)

# Vanila_1

@bottle.post("/igre/vanila_1/")
def vanila_1_post():
    """Igre običajnih križcev in krožcev za enega igralca."""
    # Poiščemo igro trenutnega igralca.
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    vanila_1 = user_tracker.users[user_id][0]

    if vanila_1.state == "P":
        # Določimo začetne parametre.
        player_mark = bottle.request.forms.getunicode('player_mark')
        player_turn = bool(bottle.request.forms.getunicode('player_turn'))
        difficulty = bottle.request.forms.getunicode('difficulty')
        vanila_1.choose_parameters(player_mark, player_turn, difficulty)
        vanila_1.state = "M"
        if not player_turn:
             vanila_1.make_move(next(vanila_1.bot_generator))
        bottle.redirect("/igre/vanila_1/")

    elif vanila_1.state == "M":
        # Naredimo potezo.
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        if vanila_1.make_move(inp_space):
            if not vanila_1.cell.check_win() and vanila_1.num_turns < 9:
                vanila_1.make_move(next(vanila_1.bot_generator))
                if not vanila_1.cell.check_win() and vanila_1.num_turns < 9:
                    None
                else:
                    vanila_1.state = "E"
            else:
                vanila_1.state = "E"                
        bottle.redirect("/igre/vanila_1/")

    elif vanila_1.state == "E":
        # Posodobimo statistične podatke in ponastavimo igro.
        data_manager.data["ended_V1"] += 1
        if vanila_1.cell.check_win() and not vanila_1.player_turn:
            data_manager.data["player_beat_bot"] += 1
            if vanila_1.player_mark == "X":
                data_manager.data["player_win_X"] += 1
            elif vanila_1.player_mark == "O":
                data_manager.data["player_win_O"] += 1
        elif not vanila_1.cell.check_win():
            data_manager.data["ended_draw"] += 1
        data_manager.dump_data_to_file()
        vanila_1.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/vanila_1/")
def vanila_1_get():
    """Preusmeri na vanila_1.html"""
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    vanila_1 = user_tracker.users[user_id][0]
    return bottle.template("vanila_1.html", game=vanila_1)

# Vanila_2

@bottle.post("/igre/vanila_2/")
def vanila_2_post():
    """Igre običajnih križcev in krožcev za dva igralca."""
    # Poiščemo igro trenutnega igralca.
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    vanila_2 = user_tracker.users[user_id][1]
    
    if vanila_2.state == "P":
        # Določimo začetne parametre.
        vanila_2.choose_parameters(bottle.request.forms.getunicode('player_mark'))
        vanila_2.state = "M"
        bottle.redirect("/igre/vanila_2/")
    elif vanila_2.state == "M":
        # Naredimo potezo.
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        vanila_2.make_move(inp_space)
        if not vanila_2.cell.check_win() and vanila_2.num_turns < 9:
            None
        else:
            vanila_2.state = "E"
        bottle.redirect("/igre/vanila_2/")
    elif vanila_2.state == "E":
        # Posodobimo statistične podatke in ponastavimo igro.
        data_manager.data["ended_V2"] += 1
        if vanila_2.cell.check_win():
            if vanila_2.mark == "X":
                data_manager.data["player_win_O"] += 1
            elif vanila_2.mark == "O":
                data_manager.data["player_win_X"] += 1
        else:
            data_manager.data["ended_draw"] += 1
        data_manager.dump_data_to_file()
        vanila_2.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/vanila_2/")
def vanila_2_get():
    """Preusmeri na vanila_2.html"""
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    vanila_2 = user_tracker.users[user_id][1]
    return bottle.template("vanila_2.html", game=vanila_2)

# Ultimate_1

@bottle.post("/igre/ultimate_1/")
def ultimate_1_post():
    """Igre ultimativnih križcev in krožcev za enega igralca."""
    # Poiščemo igro trenutnega igralca.
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    ultimate_1 = user_tracker.users[user_id][2]
    if ultimate_1.state == "P":
        # Določimo začetne parametre.
        player_mark = bottle.request.forms.getunicode('player_mark')
        player_turn = bool(bottle.request.forms.getunicode('player_turn'))
        ultimate_1.choose_parameters(player_mark, player_turn)
        if player_turn:
            ultimate_1.state = "I"
        else:
            inp_cell = ultimate_1.master_cell.random_free()
            inp_space = ultimate_1.cell_list[inp_cell].random_free()
            ultimate_1.initial_move(inp_cell, inp_space)
            ultimate_1.state = "M"
        bottle.redirect("/igre/ultimate_1/")
    
    elif ultimate_1.state == "I":
        # Naredimo prvo potezo.
        inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        ultimate_1.initial_move(inp_cell, inp_space)

        current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
        ultimate_1.inp_space = ultimate_1.master_bot.ultimate_incell_move(ultimate_1.cell_list, ultimate_1.inp_cell)
        ultimate_1.move_in_small_cell(current_cell)
        ultimate_1.state = "M"
        bottle.redirect("/igre/ultimate_1/")

    elif ultimate_1.state == "M":
        # Naredimo potezo.
        # Igralec.
        while ultimate_1.player_turn:
            current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
            if not ultimate_1.move_in_big_cell:
                inp_space_kand = int(bottle.request.forms.getunicode('inp_space'))
                if ultimate_1.cell_list[ultimate_1.inp_cell].spaces[inp_space_kand] == ".":
                    ultimate_1.inp_space = inp_space_kand
                    ultimate_1.move_in_small_cell(current_cell)
                else:
                    bottle.redirect("/igre/ultimate_1/")
            else:
                inp_cell_kand = int(bottle.request.forms.getunicode('inp_cell'))
                if ultimate_1.master_cell.spaces[inp_cell_kand] == ".":
                    ultimate_1.inp_cell = inp_cell_kand
                    ultimate_1.move_in_big_cell = False
                    # Da se ne pokaže zadnja poteza robota.
                    ultimate_1.last_inp_cell = 0
                    bottle.redirect("/igre/ultimate_1/")
                else:
                    bottle.redirect("/igre/ultimate_1/")

        if ultimate_1.master_cell.spaces[ultimate_1.inp_cell] == ".":
            None
        else:
            ultimate_1.move_in_big_cell = True

        if not ultimate_1.master_cell.check_win() and ultimate_1.num_master_turns < 9:
            # Bot.
            while not ultimate_1.player_turn:
                current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
                if not ultimate_1.move_in_big_cell:
                    ultimate_1.inp_space = ultimate_1.master_bot.ultimate_incell_move(ultimate_1.cell_list, ultimate_1.inp_cell)
                    ultimate_1.move_in_small_cell(current_cell)
                else:
                    ultimate_1.inp_cell = ultimate_1.master_cell.random_free()
                    ultimate_1.move_in_big_cell = False
                
            if ultimate_1.master_cell.spaces[ultimate_1.inp_cell] == ".":
                None
            else:
                ultimate_1.move_in_big_cell = True
            
            if not ultimate_1.master_cell.check_win() and ultimate_1.num_master_turns < 9:
                None
            else:
                ultimate_1.state = "E"

        else:
            ultimate_1.state = "E"
        bottle.redirect("/igre/ultimate_1/")

    elif ultimate_1.state == "E":
        # Posodobimo statistične podatke in ponastavimo igro.
        data_manager.data["ended_U1"] += 1
        if ultimate_1.master_cell.check_win() and not ultimate_1.player_turn:
            data_manager.data["player_beat_bot"] += 1
            if ultimate_1.player_mark == "X":
                data_manager.data["player_win_X"] += 1
            elif ultimate_1.player_mark == "O":
                data_manager.data["player_win_O"] += 1
        elif not ultimate_1.master_cell.check_win():
            data_manager.data["ended_draw"] += 1
        data_manager.dump_data_to_file()

        ultimate_1.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/ultimate_1/")
def ultimate_1_get():
    """Preusmeri na ultimate_1.html"""
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    ultimate_1 = user_tracker.users[user_id][2]
    return bottle.template("ultimate_1.html", game=ultimate_1)

# Ultimate_2

@bottle.post("/igre/ultimate_2/")
def ultimate_2_post():
    """Igre ultimativnih križcev in krožcev za dva igralca."""
    # Poiščemo igro trenutnega igralca.
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    ultimate_2 = user_tracker.users[user_id][3]

    if ultimate_2.state == "P":
        # Določimo začetne parametre.
        first_player_mark = bottle.request.forms.getunicode('first_player_mark')
        ultimate_2.choose_parameters(first_player_mark)
        ultimate_2.state = "I"
        bottle.redirect("/igre/ultimate_2/")

    elif ultimate_2.state == "I":
        # Naredimo prvo potezo.
        inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        ultimate_2.initial_move(inp_cell, inp_space)
        ultimate_2.state = "M"
        bottle.redirect("/igre/ultimate_2/")
    
    elif ultimate_2.state == "M":
        # Naredimo potezo.
        current_cell = ultimate_2.cell_list[ultimate_2.inp_cell]
        if not ultimate_2.move_in_big_cell:
            ultimate_2.inp_space = int(bottle.request.forms.getunicode('inp_space'))
            ultimate_2.move_in_small_cell(current_cell)
        if ultimate_2.move_in_big_cell:
            ultimate_2.inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
            ultimate_2.move_in_big_cell = False

        if ultimate_2.master_cell.spaces[ultimate_2.inp_cell] == ".":
            None
        else:
            ultimate_2.move_in_big_cell = True

        if not ultimate_2.master_cell.check_win() and ultimate_2.num_master_turns < 9:
            None
        else:
            ultimate_2.state = "E"
        bottle.redirect("/igre/ultimate_2/")

    elif ultimate_2.state == "E":
        # Posodobimo statistične podatke in ponastavimo igro.
        data_manager.data["ended_U2"] += 1
        if ultimate_2.master_cell.check_win():
            if ultimate_2.mark == "X":
                data_manager.data["player_win_O"] += 1
            elif ultimate_2.mark == "O":
                data_manager.data["player_win_X"] += 1
        else:
            data_manager.data["ended_draw"] += 1
        data_manager.dump_data_to_file()
        ultimate_2.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/ultimate_2/")
def ultimate_2_get():
    """Preusmeri na ultimate_2.html"""
    user_id = int(bottle.request.get_cookie(COOKIE, secret=SECRET))
    ultimate_2 = user_tracker.users[user_id][3]
    return bottle.template("ultimate_2.html", game=ultimate_2)

bottle.run(debug=True, reloader=True)