import bottle
from model import *



@bottle.get("/pravila/")
def pravila():
    return bottle.template("pravila.html")

bottle.run(debug=True, reloader=True)