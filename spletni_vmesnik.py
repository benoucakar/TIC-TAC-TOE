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
        vanila_2.check_bad_move()
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
        player_turn = bottle.request.forms.getunicode('player_turn')
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



bottle.run(debug=True, reloader=True)