import bottle
from model import *

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

bottle.run(debug=True, reloader=True)