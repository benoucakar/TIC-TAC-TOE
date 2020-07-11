import bottle
from model import *



#Klicanje spletnih strani

@bottle.get("/")
def index():
    bottle.redirect("/domov/")

@bottle.get("/domov/")
def domov():
    return bottle.template("domov.html")

@bottle.get("/igre/")
def igra():
    return bottle.template("igre.html")

@bottle.get("/pravila/")
def pravila():
    return bottle.template("pravila.html")

@bottle.get("/info/")
def info():
    return bottle.template("info.html")

# Vanila_2
vanila_2 = Vanila_2()

@bottle.post("/igre/vanila_2/")
def vanila_2_post():
    if vanila_2.state == "P":
        vanila_2.choose_parameters(bottle.request.forms.getunicode('player_mark'))
        vanila_2.state = "M"
        bottle.redirect("/igre/vanila_2/")
    elif vanila_2.state == "M":
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        vanila_2.make_move(inp_space)
        if not vanila_2.cell.check_win() and vanila_2.num_turns < 9:
            None
        else:
            vanila_2.state = "E"
        bottle.redirect("/igre/vanila_2/")
    elif vanila_2.state == "E":
        vanila_2.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/vanila_2/")
def vanila_2_get():
    return bottle.template("vanila_2.html", game=vanila_2)

# Vanila_1
vanila_1 = Vanila_1()

@bottle.post("/igre/vanila_1/")
def vanila_1_post():
    if vanila_1.state == "P":
        player_mark = bottle.request.forms.getunicode('player_mark')
        player_turn = bool(bottle.request.forms.getunicode('player_turn'))
        difficulty = bottle.request.forms.getunicode('difficulty')
        vanila_1.choose_parameters(player_mark, player_turn, difficulty)
        vanila_1.state = "M"
        if not player_turn:
             vanila_1.make_move(next(vanila_1.bot_generator))
        bottle.redirect("/igre/vanila_1/")

    elif vanila_1.state == "M":
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
        vanila_1.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/vanila_1/")
def vanila_1_get():
    return bottle.template("vanila_1.html", game=vanila_1)

# Ultimate_2
ultimate_2 = Ultimate_2()

@bottle.post("/igre/ultimate_2/")
def ultimate_2_post():
    if ultimate_2.state == "P":
        first_player_mark = bottle.request.forms.getunicode('first_player_mark')
        ultimate_2.choose_parameters(first_player_mark)
        ultimate_2.state = "I"
        bottle.redirect("/igre/ultimate_2/")

    elif ultimate_2.state == "I":
        inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        ultimate_2.initial_move(inp_cell, inp_space)
        ultimate_2.state = "M"
        bottle.redirect("/igre/ultimate_2/")
    
    elif ultimate_2.state == "M":
        current_cell = ultimate_2.cell_list[ultimate_2.inp_cell]
        if not ultimate_2.move_in_big_cell:
            ultimate_2.inp_space = int(bottle.request.forms.getunicode('inp_space'))
            ultimate_2.move_in_small_cell(current_cell)
        if ultimate_2.move_in_big_cell:
            ultimate_2.inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
            ultimate_2.move_in_big_cell = False

        if ultimate_2.master_cell.cells[ultimate_2.inp_cell] == ".":
            None
        else:
            ultimate_2.move_in_big_cell = True

        if not ultimate_2.master_cell.check_win() and ultimate_2.num_master_turns < 9:
            None
        else:
            ultimate_2.state = "E"
        bottle.redirect("/igre/ultimate_2/")

    elif ultimate_2.state == "E":
        ultimate_2.reset()
        bottle.redirect("/igre/")


@bottle.get("/igre/ultimate_2/")
def ultimate_2_get():
    return bottle.template("ultimate_2.html", game=ultimate_2)

# Ultimate_1
ultimate_1 = Ultimate_1()

@bottle.post("/igre/ultimate_1/")
def ultimate_1_post():
    if ultimate_1.state == "P":
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
        inp_cell = int(bottle.request.forms.getunicode('inp_cell'))
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        ultimate_1.initial_move(inp_cell, inp_space)

        current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
        ultimate_1.inp_space = ultimate_1.master_bot.ultimate_incell_move(ultimate_1.cell_list, ultimate_1.inp_cell)
        ultimate_1.move_in_small_cell(current_cell)
        ultimate_1.state = "M"
        bottle.redirect("/igre/ultimate_1/")

    elif ultimate_1.state == "M":
        
        #Igralec
        while ultimate_1.player_turn:
            current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
            if not ultimate_1.move_in_big_cell:
                inp_space_kand = int(bottle.request.forms.getunicode('inp_space'))
                if ultimate_1.cell_list[ultimate_1.inp_cell].cells[inp_space_kand] == ".":
                    ultimate_1.inp_space = inp_space_kand
                    ultimate_1.move_in_small_cell(current_cell)
                else:
                    bottle.redirect("/igre/ultimate_1/")
            else:
                inp_cell_kand = int(bottle.request.forms.getunicode('inp_cell'))
                if ultimate_1.master_cell.cells[inp_cell_kand] == ".":
                    ultimate_1.inp_cell = inp_cell_kand
                    ultimate_1.move_in_big_cell = False
                    # Da se ne pokaže zadnja poteza robota
                    ultimate_1.last_inp_cell = 0
                    bottle.redirect("/igre/ultimate_1/")
                else:
                    bottle.redirect("/igre/ultimate_1/")

        if ultimate_1.master_cell.cells[ultimate_1.inp_cell] == ".":
            None
        else:
            ultimate_1.move_in_big_cell = True

        if not ultimate_1.master_cell.check_win() and ultimate_1.num_master_turns < 9:
            #Bot
            while not ultimate_1.player_turn:
                current_cell = ultimate_1.cell_list[ultimate_1.inp_cell]
                if not ultimate_1.move_in_big_cell:
                    ultimate_1.inp_space = ultimate_1.master_bot.ultimate_incell_move(ultimate_1.cell_list, ultimate_1.inp_cell)
                    ultimate_1.move_in_small_cell(current_cell)
                else:
                    ultimate_1.inp_cell = ultimate_1.master_cell.random_free()
                    ultimate_1.move_in_big_cell = False
                
            if ultimate_1.master_cell.cells[ultimate_1.inp_cell] == ".":
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
        ultimate_1.reset()
        bottle.redirect("/igre/")

@bottle.get("/igre/ultimate_1/")
def ultimate_1_get():
    return bottle.template("ultimate_1.html", game=ultimate_1)

bottle.run(debug=True, reloader=True)