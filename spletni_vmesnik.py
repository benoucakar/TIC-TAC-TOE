import bottle

@bottle.get("/")
def index():
    return "Hello world!"

bottle.run(debug=True, reloader=True)