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
game = Vanila_2()

@bottle.post("/vanila_2/")
def vanila_2_post():
    if game.state == "P":
        game.choose_parameters(bottle.request.forms.getunicode('player_mark'))
        game.state = "M"
        bottle.redirect("/vanila_2/")
    elif game.state == "M":
        inp_space = int(bottle.request.forms.getunicode('inp_space'))
        game.check_bad_move()
        game.make_move(inp_space)
        if not game.cell.check_win() and game.num_turns <= 9:
            None
        else:
            game.state = "E"
        bottle.redirect("/vanila_2/")
    elif game.state == "E":
        game.reset()
        bottle.redirect("/igre/")

@bottle.get("/vanila_2/")
def vanila_2_get():
    return bottle.template("vanila_2.html", game=game)



bottle.run(debug=True, reloader=True)